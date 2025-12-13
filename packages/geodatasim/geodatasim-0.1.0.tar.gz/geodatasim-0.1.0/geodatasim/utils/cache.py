"""Caching system for API responses."""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Callable, Optional
from functools import wraps


def cache_response(ttl_days: int = 90):
    """
    Decorator to cache API responses to disk.

    Args:
        ttl_days: Time-to-live in days (default: 90 days)

    Examples:
        >>> @cache_response(ttl_days=30)
        ... def get_data(city: str):
        ...     return api.fetch(city)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            from ..core.config import get_config
            config = get_config()

            # Check if caching is enabled
            if not config.get('cache_enabled', True):
                return func(*args, **kwargs)

            # Create cache key from function name and arguments
            cache_key = _create_cache_key(func.__name__, args, kwargs)

            # Get cache directory
            cache_dir = Path(config.get('cache_dir', Path.home() / '.geodatasim' / 'cache'))
            cache_dir.mkdir(parents=True, exist_ok=True)

            cache_file = cache_dir / f"{cache_key}.json"

            # Check if cached version exists and is still valid
            if cache_file.exists():
                try:
                    with open(cache_file, 'r') as f:
                        cached_data = json.load(f)

                    # Check expiry
                    cached_time = datetime.fromisoformat(cached_data['timestamp'])
                    expiry_time = cached_time + timedelta(days=ttl_days)

                    if datetime.now() < expiry_time:
                        if config.get('verbose', False):
                            print(f"Cache hit: {func.__name__}")
                        return cached_data['data']
                    else:
                        if config.get('verbose', False):
                            print(f"Cache expired: {func.__name__}")
                except Exception as e:
                    if config.get('show_warnings', True):
                        print(f"Warning: Cache read error: {e}")

            # Cache miss or expired - call the actual function
            if config.get('verbose', False):
                print(f"Cache miss: {func.__name__}")

            result = func(*args, **kwargs)

            # Save to cache
            try:
                cache_data = {
                    'timestamp': datetime.now().isoformat(),
                    'ttl_days': ttl_days,
                    'function': func.__name__,
                    'data': result,
                }

                with open(cache_file, 'w') as f:
                    json.dump(cache_data, f, indent=2)

            except Exception as e:
                if config.get('show_warnings', True):
                    print(f"Warning: Cache write error: {e}")

            return result

        return wrapper
    return decorator


def _create_cache_key(func_name: str, args: tuple, kwargs: dict) -> str:
    """
    Create a unique cache key from function name and arguments.

    Args:
        func_name: Function name
        args: Positional arguments
        kwargs: Keyword arguments

    Returns:
        MD5 hash as cache key
    """
    # Create a string representation of function call
    key_parts = [func_name]

    # Add positional arguments
    for arg in args:
        if isinstance(arg, (str, int, float, bool)):
            key_parts.append(str(arg))
        else:
            # For complex objects, use their string representation
            key_parts.append(repr(arg))

    # Add keyword arguments (sorted for consistency)
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}={v}")

    # Create MD5 hash
    key_string = '|'.join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()


def clear_cache(func_name: Optional[str] = None):
    """
    Clear cached data.

    Args:
        func_name: Function name to clear cache for, or None to clear all

    Examples:
        >>> from geodatasim.utils import clear_cache
        >>> clear_cache()  # Clear all
        >>> clear_cache('get_country_data')  # Clear specific function
    """
    from ..core.config import get_config
    config = get_config()

    cache_dir = Path(config.get('cache_dir', Path.home() / '.geodatasim' / 'cache'))

    if not cache_dir.exists():
        return

    deleted_count = 0

    for cache_file in cache_dir.glob('*.json'):
        try:
            if func_name is None:
                # Delete all cache files
                cache_file.unlink()
                deleted_count += 1
            else:
                # Check if this cache file is for the specified function
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    if data.get('function') == func_name:
                        cache_file.unlink()
                        deleted_count += 1
        except Exception as e:
            if config.get('show_warnings', True):
                print(f"Warning: Error deleting cache file {cache_file}: {e}")

    if config.get('verbose', False):
        print(f"Cleared {deleted_count} cache files")


def get_cache_stats() -> dict:
    """
    Get cache statistics.

    Returns:
        Dictionary with cache stats (total files, total size, etc.)
    """
    from ..core.config import get_config
    config = get_config()

    cache_dir = Path(config.get('cache_dir', Path.home() / '.geodatasim' / 'cache'))

    if not cache_dir.exists():
        return {
            'total_files': 0,
            'total_size_mb': 0,
            'cache_dir': str(cache_dir),
        }

    cache_files = list(cache_dir.glob('*.json'))
    total_size = sum(f.stat().st_size for f in cache_files)

    return {
        'total_files': len(cache_files),
        'total_size_mb': round(total_size / (1024 * 1024), 2),
        'cache_dir': str(cache_dir),
        'files': [f.name for f in cache_files[:10]],  # First 10 files
    }
