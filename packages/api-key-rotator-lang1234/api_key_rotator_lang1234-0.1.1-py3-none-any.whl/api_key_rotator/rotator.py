"""API Key Rotator - Main module for rotating API keys with automatic expiration handling."""

import threading
import time
from typing import List, Optional, Callable, Dict, Any
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class KeyRotator:
    """
    Thread-safe API key rotator with automatic expiration handling.
    
    Manages a pool of API keys with round-robin rotation, expiration tracking,
    TTL support, and dynamic key fetching capabilities.
    
    Args:
        keys: Initial list of API keys
        ttl_seconds: Optional time-to-live for each key in seconds
        key_fetcher: Optional callback function to fetch new keys when needed
        auto_remove_expired: If True, automatically remove expired keys from rotation
    
    Examples:
        Basic usage:
            >>> rotator = KeyRotator(['key1', 'key2', 'key3'])
            >>> api_key = rotator.get_key()
            >>> rotator.mark_expired(api_key)
        
        With TTL:
            >>> rotator = KeyRotator(['key1', 'key2'], ttl_seconds=3600)
        
        With dynamic fetcher:
            >>> def fetch_new_key():
            ...     return "new_key_from_api"
            >>> rotator = KeyRotator(['key1'], key_fetcher=fetch_new_key)
    """
    
    def __init__(
        self,
        keys: List[str],
        ttl_seconds: Optional[int] = None,
        key_fetcher: Optional[Callable[[], str]] = None,
        auto_remove_expired: bool = False
    ):
        """Initialize the KeyRotator with given parameters."""
        if not keys:
            raise ValueError("At least one API key must be provided")
        
        self._lock = threading.RLock()
        self._keys: List[str] = list(keys)
        self._expired_keys: set = set()
        self._key_metadata: Dict[str, Dict[str, Any]] = {}
        self._current_index = 0
        self._ttl_seconds = ttl_seconds
        self._key_fetcher = key_fetcher
        self._auto_remove_expired = auto_remove_expired
        
        # Initialize metadata for each key
        for key in self._keys:
            self._key_metadata[key] = {
                'added_at': time.time(),
                'last_used': None,
                'use_count': 0,
                'expired_at': None
            }
    
    def get_key(self) -> str:
        """
        Get the next available API key using round-robin rotation.
        
        Automatically skips expired keys and fetches new keys if needed.
        
        Returns:
            str: An available API key
        
        Raises:
            RuntimeError: If no valid keys are available and no key_fetcher is configured
        """
        with self._lock:
            # Clean up expired keys based on TTL
            if self._ttl_seconds:
                self._check_ttl_expiration()
            
            available_keys = [k for k in self._keys if k not in self._expired_keys]
            
            # If no keys available, try to fetch a new one
            if not available_keys:
                if self._key_fetcher:
                    logger.info("No available keys, fetching new key...")
                    new_key = self._key_fetcher()
                    self.add_key(new_key)
                    return new_key
                else:
                    raise RuntimeError("No valid API keys available and no key_fetcher configured")
            
            # Find next available key using round-robin
            attempts = 0
            max_attempts = len(self._keys)
            
            while attempts < max_attempts:
                current_key = self._keys[self._current_index]
                self._current_index = (self._current_index + 1) % len(self._keys)
                
                if current_key not in self._expired_keys:
                    # Update metadata
                    self._key_metadata[current_key]['last_used'] = time.time()
                    self._key_metadata[current_key]['use_count'] += 1
                    return current_key
                
                attempts += 1
            
            # Should not reach here, but as a fallback
            raise RuntimeError("Failed to get available key")
    
    def mark_expired(self, key: str) -> None:
        """
        Mark a key as expired, removing it from rotation.
        
        Args:
            key: The API key to mark as expired
        
        Raises:
            ValueError: If the key is not in the rotator
        """
        with self._lock:
            if key not in self._key_metadata:
                raise ValueError(f"Key not found in rotator: {key}")
            
            self._expired_keys.add(key)
            self._key_metadata[key]['expired_at'] = time.time()
            logger.info(f"Key marked as expired: {key[:8]}...")
            
            # Auto-remove if configured
            if self._auto_remove_expired:
                self._remove_key(key)
    
    def mark_valid(self, key: str) -> None:
        """
        Restore an expired key back to the rotation pool.
        
        Args:
            key: The API key to restore
        
        Raises:
            ValueError: If the key is not in the rotator
        """
        with self._lock:
            if key not in self._key_metadata:
                raise ValueError(f"Key not found in rotator: {key}")
            
            self._expired_keys.discard(key)
            self._key_metadata[key]['expired_at'] = None
            self._key_metadata[key]['added_at'] = time.time()  # Reset TTL
            logger.info(f"Key marked as valid: {key[:8]}...")
    
    def add_key(self, key: str) -> None:
        """
        Add a new key to the rotation pool.
        
        Args:
            key: The API key to add
        
        Raises:
            ValueError: If the key already exists
        """
        with self._lock:
            if key in self._key_metadata:
                raise ValueError(f"Key already exists in rotator: {key}")
            
            self._keys.append(key)
            self._key_metadata[key] = {
                'added_at': time.time(),
                'last_used': None,
                'use_count': 0,
                'expired_at': None
            }
            logger.info(f"New key added: {key[:8]}...")
    
    def remove_key(self, key: str) -> None:
        """
        Remove a key from the rotator entirely.
        
        Args:
            key: The API key to remove
        
        Raises:
            ValueError: If the key is not in the rotator
        """
        with self._lock:
            self._remove_key(key)
    
    def _remove_key(self, key: str) -> None:
        """Internal method to remove a key (without lock)."""
        if key not in self._key_metadata:
            raise ValueError(f"Key not found in rotator: {key}")
        
        self._keys.remove(key)
        self._expired_keys.discard(key)
        del self._key_metadata[key]
        
        # Adjust current index if needed
        if self._current_index >= len(self._keys) and self._keys:
            self._current_index = 0
        
        logger.info(f"Key removed: {key[:8]}...")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the key pool.
        
        Returns:
            dict: Statistics including total keys, available keys, expired keys, and metadata
        """
        with self._lock:
            available_keys = [k for k in self._keys if k not in self._expired_keys]
            
            return {
                'total_keys': len(self._keys),
                'available_keys': len(available_keys),
                'expired_keys': len(self._expired_keys),
                'current_index': self._current_index,
                'ttl_seconds': self._ttl_seconds,
                'has_key_fetcher': self._key_fetcher is not None,
                'keys_metadata': {
                    key[:8] + '...': {
                        'is_expired': key in self._expired_keys,
                        'use_count': meta['use_count'],
                        'last_used': meta['last_used'],
                        'age_seconds': time.time() - meta['added_at'] if meta['added_at'] else None
                    }
                    for key, meta in self._key_metadata.items()
                }
            }
    
    def _check_ttl_expiration(self) -> None:
        """Check and expire keys based on TTL (internal method)."""
        if not self._ttl_seconds:
            return
        
        current_time = time.time()
        for key, meta in self._key_metadata.items():
            if key not in self._expired_keys:
                age = current_time - meta['added_at']
                if age > self._ttl_seconds:
                    logger.info(f"Key expired due to TTL: {key[:8]}...")
                    self._expired_keys.add(key)
                    meta['expired_at'] = current_time
    
    def __len__(self) -> int:
        """Return the total number of keys in the rotator."""
        with self._lock:
            return len(self._keys)
    
    def __repr__(self) -> str:
        """Return string representation of the KeyRotator."""
        stats = self.get_stats()
        return (f"KeyRotator(total={stats['total_keys']}, "
                f"available={stats['available_keys']}, "
                f"expired={stats['expired_keys']})")


def with_key_rotation(rotator: KeyRotator, max_retries: int = 3, retry_on_exceptions: tuple = (Exception,)):
    """
    Decorator for automatic key rotation on API call failures.
    
    Automatically retries the decorated function with a new API key if it fails,
    marking the failed key as expired.
    
    Args:
        rotator: KeyRotator instance to use for rotation
        max_retries: Maximum number of retries before giving up
        retry_on_exceptions: Tuple of exception types to catch and retry on
    
    Examples:
        >>> rotator = KeyRotator(['key1', 'key2', 'key3'])
        >>> @with_key_rotation(rotator)
        ... def api_call(data, api_key=None):
        ...     response = requests.get(url, headers={'Authorization': api_key})
        ...     return response.json()
        >>> result = api_call({'param': 'value'})
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    # Get a new key for this attempt
                    api_key = rotator.get_key()
                    
                    # Inject the key into kwargs if not already provided
                    if 'api_key' not in kwargs:
                        kwargs['api_key'] = api_key
                    
                    # Call the function
                    result = func(*args, **kwargs)
                    
                    # Success! Return the result
                    return result
                    
                except retry_on_exceptions as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries} failed with key {api_key[:8]}...: {str(e)}"
                    )
                    
                    # Mark the key as expired
                    try:
                        rotator.mark_expired(api_key)
                    except ValueError:
                        # Key might have been removed already
                        pass
                    
                    # If this was the last attempt, re-raise
                    if attempt == max_retries - 1:
                        logger.error(f"All {max_retries} attempts failed")
                        raise
                    
                    # Otherwise, continue to next attempt
                    continue
            
            # Should not reach here, but if it does, raise the last exception
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator
