"""
API Key Rotator - Automatically rotate through API keys when quotas are exhausted
"""

from .manager import APIKeyManager

__version__ = "0.1.0"
__all__ = ["APIKeyManager"]
