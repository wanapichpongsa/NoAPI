import logging
from functools import wraps
import time
import psutil
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Performance monitoring decorator
def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss / 1024 / 1024  # Memory in MB
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_memory = process.memory_info().rss / 1024 / 1024
        execution_time = end_time - start_time
        memory_used = end_memory - start_memory
        
        logging.info(f"Performance - Function: {func.__name__}")
        logging.info(f"Execution time: {execution_time:.2f} seconds")
        logging.info(f"Memory usage: {memory_used:.2f} MB")
        
        return result
    return wrapper

# File system monitoring
class PerformanceMonitor(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            process = psutil.Process(os.getpid())
            memory_usage = process.memory_info().rss / 1024 / 1024
            cpu_usage = process.cpu_percent()
            logging.info(f"System Stats - Memory: {memory_usage:.2f}MB, CPU: {cpu_usage}%")

def init_performance_monitoring():
    observer = Observer()
    event_handler = PerformanceMonitor()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    return observer 