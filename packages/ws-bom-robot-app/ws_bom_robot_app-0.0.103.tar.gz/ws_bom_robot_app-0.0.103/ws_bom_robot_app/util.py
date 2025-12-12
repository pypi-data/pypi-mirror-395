import logging.handlers
import os, logging, json
from typing import Callable, TypeVar, Generic
from functools import wraps
from .config import config

T= TypeVar('T')

#region logging
class logger_path_filter(logging.Filter):
    def filter(self, record):
        record.pathname = record.pathname.replace(os.getcwd(),"")
        return True
def logger_instance(name: str) -> logging.Logger:
    logging.basicConfig(
        format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(pathname)s:%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S',
        level=logging.INFO)
    logger = logging.getLogger(name)
    logger.addFilter(logger_path_filter())
    return logger
_log: logging.Logger = locals().get("_loc", logger_instance(__name__))
#endregion

#region task
def is_app_subprocess():
    """Check if we're running a task in a subprocess."""
    return os.environ.get('IS_ROBOT_APP_SUBPROCESS', '').lower() == 'true'
#endregion

#region cache
_cache = {}
_cache_timestamps = {}

def cache_with_ttl(ttl_seconds: int):
    """
    Decorator for caching async function results with TTL (Time To Live)

    Args:
        ttl_seconds: Cache expiration time in seconds
    """
    import time
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"

            current_time = time.time()

            # Check if cached result exists and is still valid
            if (cache_key in _cache and
                cache_key in _cache_timestamps and
                current_time - _cache_timestamps[cache_key] < ttl_seconds):
                return _cache[cache_key]

            # Call the original function and cache the result
            result = await func(*args, **kwargs)
            _cache[cache_key] = result
            _cache_timestamps[cache_key] = current_time

            return result
        return wrapper
    return decorator

def clear_cache(id: str = None):
    """Clear the cache by id function"""
    cache_key_prefix = f"{id}:"
    keys_to_remove = [key for key in _cache.keys() if key.startswith(cache_key_prefix)]
    for key in keys_to_remove:
        _cache.pop(key, None)
        _cache_timestamps.pop(key, None)

def get_cache_info(id: str) -> dict:
    """Get information about current cache status"""
    import time
    current_time = time.time()
    cache_info = {}

    for key, timestamp in _cache_timestamps.items():
        if key.startswith(f"{id}:"):
            remaining_ttl = 600 - (current_time - timestamp)
            cache_info[key] = {
                "cached_at": timestamp,
                "remaining_ttl": max(0, remaining_ttl),
                "is_expired": remaining_ttl <= 0
            }

    return cache_info
#endregion

def _get_timer_wrapper(is_async=False):
    import time, sys
    def log_execution(start_time, func, args):
        end = time.time()
        _log.info("'%s -> %s' exec in %s sec\n%s\n---\n",
                  sys._getframe(2).f_code.co_qualname,
                  func.__name__,
                  end - start_time,
                  str(args[:1])[:100])
    if not config.runtime_options().debug:
        return lambda f: f
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            log_execution(start, func, args)
            return result
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            log_execution(start, func, args)
            return result
        return async_wrapper if is_async else sync_wrapper
    return decorator

def timer(func):
    return _get_timer_wrapper(is_async=False)(func)
def atimer(func):
    return _get_timer_wrapper(is_async=True)(func)

#profiler
def memory_leak_detector(func):
    import tracemalloc, gc, sys
    async def wrapper(*args, **kwargs):
        # start tracking
        tracemalloc.start()
        initial_snapshot = tracemalloc.take_snapshot()
        # run
        result = await func(*args, **kwargs)
        # take final snapshot
        final_snapshot = tracemalloc.take_snapshot()
        # compare snapshots
        top_stats = final_snapshot.compare_to(initial_snapshot, 'lineno')
        print(f"\nMemory Leak Analysis for {func.__name__}:")
        for stat in top_stats[:10]:
            print(stat)
        # uncollectable objects
        print("\n[ Uncollectable Objects ]")
        print(gc.garbage)
        print("\nGarbage Collector Stats:")
        print(gc.get_stats())
        # stop tracking
        tracemalloc.stop()
        return result
    return wrapper






