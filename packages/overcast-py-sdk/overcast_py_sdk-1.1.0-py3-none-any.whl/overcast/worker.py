
import threading
import queue
import time
import atexit
from typing import List, Dict, Any, Optional
import logging

class LogDispatcher:
    def __init__(
        self, 
        send_func, 
        batch_size: int = 100, 
        flush_interval: float = 5.0,
        max_queue_size: int = 10000
    ):
        self.send_func = send_func
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self._queue = queue.Queue(maxsize=max_queue_size)
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._worker_loop, daemon=True, name="Overcast-Dispatcher")
        self._lock = threading.Lock()
        
        self._thread.start()
        atexit.register(self.shutdown)

    def enqueue(self, log_entry: Dict[str, Any]):
        try:
            self._queue.put_nowait(log_entry)
        except queue.Full:
            # Drop logs if queue is full to avoid blocking application
            pass

    def _worker_loop(self):
        batch = []
        last_flush = time.time()

        while not self._stop_event.is_set():
            try:
                # Wait for new item with timeout (for flush interval)
                timeout = max(0.1, self.flush_interval - (time.time() - last_flush))
                try:
                    item = self._queue.get(timeout=timeout)
                    batch.append(item)
                except queue.Empty:
                    pass

                # Check if we should flush
                current_time = time.time()
                is_batch_full = len(batch) >= self.batch_size
                is_time_to_flush = (current_time - last_flush) >= self.flush_interval
                
                if (batch and (is_batch_full or is_time_to_flush)) or self._stop_event.is_set():
                    self._flush_batch(batch)
                    batch = []
                    last_flush = current_time

            except Exception:
                # Prevent thread from dying
                pass

        # Final flush
        if batch:
            self._flush_batch(batch)
            
        # Drain queue
        final_batch = []
        while not self._queue.empty():
            try:
                final_batch.append(self._queue.get_nowait())
            except queue.Empty:
                break
        
        if final_batch:
            self._flush_batch(final_batch)

    def _flush_batch(self, batch: List[Dict[str, Any]]):
        if not batch:
            return
            
        try:
            self.send_func(batch)
        except Exception:
            # We can't do much if sending fails here, maybe log to stderr
            pass

    def shutdown(self):
        self._stop_event.set()
        if self._thread.is_alive():
            self._thread.join(timeout=2.0)

