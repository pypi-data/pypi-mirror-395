
import logging
from typing import Optional, Dict, Any
from .client import OvercastClient

class OvercastHandler(logging.Handler):
    """
    Standard Python Logging Handler for Overcast.
    
    Usage:
        import logging
        from overcast.logging import OvercastHandler
        
        logger = logging.getLogger()
        logger.addHandler(OvercastHandler(api_key="..."))
        
        logger.error("Something went wrong")
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        client: Optional[OvercastClient] = None, 
        service: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the handler.
        
        Args:
            api_key: Overcast API key (required if client is not provided)
            client: Existing OvercastClient instance
            service: Default service name
            **kwargs: Additional arguments passed to OvercastClient constructor
        """
        super().__init__()
        
        if client:
            self.client = client
            self.owns_client = False
        elif api_key:
            self.client = OvercastClient(api_key=api_key, service=service, **kwargs)
            self.owns_client = True
        else:
            raise ValueError("Must provide either api_key or client instance")
            
    def emit(self, record: logging.LogRecord):
        try:
            msg = self.format(record)
            
            # Extract exception info if present
            exception = None
            if record.exc_info:
                # record.exc_info is (type, value, traceback)
                _, exception, _ = record.exc_info
                
            # Filter standard attributes to get extra metadata
            # These are attributes added via extra={...}
            standard_attrs = {
                "args", "asctime", "created", "exc_info", "exc_text", "filename", 
                "funcName", "levelname", "levelno", "lineno", "module", 
                "msecs", "message", "msg", "name", "pathname", "process", 
                "processName", "relativeCreated", "stack_info", "thread", "threadName"
            }
            
            metadata = {
                k: v for k, v in record.__dict__.items() 
                if k not in standard_attrs and not k.startswith("_")
            }
            
            # Add location info as metadata
            metadata["logger_name"] = record.name
            metadata["file_path"] = record.pathname
            metadata["line_number"] = record.lineno
            metadata["function_name"] = record.funcName
            
            if exception:
                self.client.exception(msg, exception=exception, **metadata)
            else:
                # Use _log directly to pass the string level name
                self.client._log(record.levelname, msg, **metadata)
                
        except Exception:
            self.handleError(record)

    def close(self):
        """Clean up the client if we own it."""
        if self.owns_client:
            self.client.close()
        super().close()

