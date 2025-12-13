"""
Overcast Client
Core SDK functionality for sending logs to Overcast incident detection.
"""

import json
import traceback
import sys
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Union, List
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

from .exceptions import OvercastError, OvercastAuthError, OvercastConnectionError, OvercastValidationError
from .worker import LogDispatcher


class OvercastClient:
    """
    Overcast SDK Client
    
    Simple client for sending logs to Overcast for automated incident detection.
    Supports automatic stack trace extraction, structured logging, and background batching.
    
    Example:
        overcast = OvercastClient(api_key="your_key")
        overcast.error("Database timeout occurred")
        
        # With metadata
        overcast.error("Payment failed", service="billing", user_id=12345)
        
        # Automatic exception capture
        try:
            risky_operation()
        except Exception as e:
            overcast.exception("Operation failed", exception=e)
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://platform.overcastsre.com",
        service: Optional[str] = None,
        timeout: int = 30,
        debug: bool = False,
        enable_batching: bool = True,
        max_batch_size: int = 100,
        flush_interval: float = 5.0
    ):
        """
        Initialize Overcast client.
        
        Args:
            api_key: Your Overcast API key
            base_url: Overcast API base URL (defaults to production)
            service: Default service name for all logs (can be overridden per log)
            timeout: Request timeout in seconds
            debug: Enable debug logging
            enable_batching: Send logs in background batches (default: True)
            max_batch_size: Maximum number of logs per batch
            flush_interval: Maximum time to wait before sending a batch
        """
        if not api_key or not api_key.strip():
            raise OvercastValidationError("API key is required")
            
        self.api_key = api_key.strip()
        self.base_url = base_url.rstrip('/')
        self.default_service = service
        self.timeout = timeout
        self.debug = debug
        self.enable_batching = enable_batching
        self._session = requests.Session()
        
        # Set default headers
        self._session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': f'overcast-python-sdk/1.0.0'
        })

        self.dispatcher = None
        if enable_batching:
            self.dispatcher = LogDispatcher(
                send_func=self._send_batch,
                batch_size=max_batch_size,
                flush_interval=flush_interval
            )

    def _send_batch(self, logs: List[Dict[str, Any]]):
        """
        Internal method to send a batch of logs to Overcast.
        """
        if not logs:
            return

        try:
            # Build request payload
            # We use a generic description for batched logs
            source_desc = f"Application logs - {self.default_service or 'batch'}"
            
            payload = {
                "api_key": self.api_key,
                "source_type": "application",
                "source_description": source_desc,
                "logs": logs
            }
            
            if self.debug:
                print(f"[Overcast SDK] Sending batch of {len(logs)} logs")
                
            # Send to Overcast
            response = self._session.post(
                f"{self.base_url}/api/v1/ingest/logs",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 401:
                if self.debug:
                    print("[Overcast SDK] Error: Invalid API key")
            elif not response.ok:
                if self.debug:
                    print(f"[Overcast SDK] Error sending batch: {response.status_code} {response.text}")
                
            if self.debug and response.ok:
                result = response.json()
                print(f"[Overcast SDK] Batch success: {result.get('incidents_detected', 0)} incidents detected")
                
        except Exception as e:
            if self.debug:
                print(f"[Overcast SDK] Unexpected error sending batch: {e}")

    def _log(self, level: str, message: str, **kwargs) -> bool:
        """
        Internal method to send log to Overcast.
        
        Args:
            level: Log level (ERROR, WARNING, INFO, DEBUG)
            message: Log message
            **kwargs: Additional metadata (service, user_id, etc.)
            
        Returns:
            bool: True if enqueued/sent successful, False otherwise
        """
        try:
            # Extract service name
            service = kwargs.pop('service', None) or self.default_service
            
            # Handle exception parameter for automatic stack trace
            exception = kwargs.pop('exception', None)
            if self.debug and exception:
                print(f"[DEBUG] Exception parameter: {exception}")
                print(f"[DEBUG] Exception type: {type(exception)}")
            
            if exception and isinstance(exception, BaseException):
                # Extract stack trace
                tb_str = ''.join(traceback.format_exception(
                    type(exception), exception, exception.__traceback__
                ))
                if self.debug:
                    print(f"[DEBUG] Original message: {message}")
                    print(f"[DEBUG] Stack trace: {tb_str}")
                message = f"{message}\n\nStack trace:\n{tb_str}"
                kwargs['exception_type'] = type(exception).__name__
                kwargs['exception_message'] = str(exception)
                if self.debug:
                    print(f"[DEBUG] Final message with stack trace: {message}")

            # Build log entry
            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": level.upper(),
                "message": message,
                "service": service,
                "raw_log": message,
                "metadata": {
                    **kwargs
                }
            }
            
            if self.enable_batching and self.dispatcher:
                self.dispatcher.enqueue(log_entry)
                return True
            else:
                # Send immediately (legacy mode)
                self._send_batch([log_entry])
                return True
            
        except Exception as e:
            if self.debug:
                print(f"[Overcast SDK] Error processing log: {e}")
            # If not using batching, we might want to raise, but for now we catch to be safe
            if not self.enable_batching:
                raise OvercastError(f"Failed to send log: {e}")
            return False

    def error(self, message: str, **kwargs) -> bool:
        """
        Log an ERROR level message.
        
        Args:
            message: Error message
            **kwargs: Additional metadata (service, user_id, request_id, etc.)
            
        Returns:
            bool: True if enqueued/sent successfully
            
        Example:
            overcast.error("Database connection failed", service="auth", user_id=123)
        """
        return self._log("ERROR", message, **kwargs)

    def warning(self, message: str, **kwargs) -> bool:
        """
        Log a WARNING level message.
        
        Args:
            message: Warning message
            **kwargs: Additional metadata
            
        Returns:
            bool: True if enqueued/sent successfully
        """
        return self._log("WARNING", message, **kwargs)

    def info(self, message: str, **kwargs) -> bool:
        """
        Log an INFO level message.
        
        Args:
            message: Info message
            **kwargs: Additional metadata
            
        Returns:
            bool: True if enqueued/sent successfully
        """
        return self._log("INFO", message, **kwargs)

    def debug(self, message: str, **kwargs) -> bool:
        """
        Log a DEBUG level message.
        
        Args:
            message: Debug message
            **kwargs: Additional metadata
            
        Returns:
            bool: True if enqueued/sent successfully
        """
        return self._log("DEBUG", message, **kwargs)

    def exception(self, message: str, exception: Optional[BaseException] = None, **kwargs) -> bool:
        """
        Log an exception with automatic stack trace capture.
        
        Args:
            message: Error message
            exception: Exception object (if None, captures current exception)
            **kwargs: Additional metadata
            
        Returns:
            bool: True if enqueued/sent successfully
            
        Example:
            try:
                dangerous_operation()
            except Exception as e:
                overcast.exception("Operation failed", exception=e, user_id=123)
                
            # Or capture current exception automatically
            try:
                dangerous_operation()
            except Exception:
                overcast.exception("Operation failed", user_id=123)
        """
        if exception is None:
            # Capture current exception from sys.exc_info()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            if exc_value:
                exception = exc_value
                
        return self._log("ERROR", message, exception=exception, **kwargs)

    def close(self):
        """Close the underlying HTTP session and shutdown worker."""
        if self.dispatcher:
            self.dispatcher.shutdown()
        if self._session:
            self._session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
