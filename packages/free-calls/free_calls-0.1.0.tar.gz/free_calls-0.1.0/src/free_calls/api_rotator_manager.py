import os
from typing import List, Callable, Any, Optional
from .exceptions import NoValidAPIKeyError


class APIKeyManager:
    """Manages multiple API keys and rotates through them when quotas are exhausted"""
    
    def __init__(self, env_prefix: str, separator: str = ","):
        """
        Initialize the API Key Manager
        
        Args:
            env_prefix: Environment variable prefix (e.g., 'OPENAI_API_KEY')
            separator: Character used to separate multiple keys in env var
        """
        self.env_prefix = env_prefix
        self.separator = separator
        self.keys = self._load_keys()
        self.failed_keys = set()
        
    def _load_keys(self) -> List[str]:
        """Load API keys from environment variable"""
        env_value = os.getenv(self.env_prefix, "")
        if not env_value:
            raise ValueError(f"No API keys found in environment variable: {self.env_prefix}")
        
        keys = [k.strip() for k in env_value.split(self.separator) if k.strip()]
        if not keys:
            raise ValueError(f"No valid API keys found in: {self.env_prefix}")
        
        return keys
    
    def _get_active_keys(self) -> List[str]:
        """Get list of keys that haven't failed yet"""
        return [k for k in self.keys if k not in self.failed_keys]
    
    def _mark_failed(self, key: str):
        """Mark a key as failed and move it to the end"""
        self.failed_keys.add(key)
        if key in self.keys:
            self.keys.remove(key)
            self.keys.append(key)
    
    def call_with_rotation(
        self, 
        api_function: Callable,
        *args,
        quota_error_types: Optional[tuple] = None,
        **kwargs
    ) -> Any:
        """
        Call an API function with automatic key rotation on quota errors
        
        Args:
            api_function: Function to call with API key as first argument
            *args: Additional positional arguments for the function
            quota_error_types: Tuple of exception types that indicate quota exhaustion
            **kwargs: Additional keyword arguments for the function
            
        Returns:
            Result from the API function
            
        Raises:
            NoValidAPIKeyError: When all API keys have been exhausted
        """
        if quota_error_types is None:
            quota_error_types = (Exception,)
        
        active_keys = self._get_active_keys()
        
        if not active_keys:
            # Reset failed keys and try again
            self.failed_keys.clear()
            active_keys = self.keys.copy()
        
        last_error = None
        
        for key in active_keys:
            try:
                return api_function(key, *args, **kwargs)
            except quota_error_types as e:
                last_error = e
                self._mark_failed(key)
                continue
            except Exception as e:
                # Re-raise non-quota errors immediately
                raise
        
        raise NoValidAPIKeyError(
            f"All API keys exhausted. Last error: {last_error}"
        )
    
    def reset(self):
        """Reset all failed keys, allowing them to be tried again"""
        self.failed_keys.clear()
    
    def get_current_key(self) -> Optional[str]:
        """Get the first available (non-failed) API key"""
        active = self._get_active_keys()
        return active[0] if active else None
    
    def get_ordered_keys(self) -> List[dict]:
        """
        Get all keys ordered by status (working first, failed last)
        
        Returns:
            List of dicts with 'key' (masked) and 'status' ('active' or 'failed')
        """
        result = []
        
        # Add active keys first
        for key in self._get_active_keys():
            result.append({
                'key': self._mask_key(key),
                'status': 'active'
            })
        
        # Add failed keys last
        for key in self.keys:
            if key in self.failed_keys:
                result.append({
                    'key': self._mask_key(key),
                    'status': 'failed'
                })
        
        return result
    
    def _mask_key(self, key: str) -> str:
        """Mask API key for safe display (show first 4 and last 4 chars)"""
        if len(key) <= 8:
            return '*' * len(key)
        return f"{key[:4]}...{key[-4:]}"
