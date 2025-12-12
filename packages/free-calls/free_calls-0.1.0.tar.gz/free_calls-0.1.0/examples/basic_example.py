"""
Basic example of using free_calls
"""

from free_calls import FreeCallsManager
import os

# Set up test API keys (replace with your actual keys)
os.environ["TEST_API_KEY"] = "key1,key2,key3"

# Initialize manager
manager = FreeCallsManager(env_prefix="TEST_API_KEY")

# Define a mock API function
def mock_api_call(api_key, message):
    """Simulates an API call"""
    print(f"Calling API with key: {api_key[:8]}...")
    
    # Simulate quota error for first key
    if api_key == "key1":
        raise Exception("Rate limit exceeded")
    
    return f"Success with {api_key}: {message}"

# Make calls with automatic rotation
try:
    result = manager.call_with_rotation(
        mock_api_call,
        "Hello, World!",
        quota_error_types=(Exception,)
    )
    print(result)
    
    # Check key status
    print("\nKey Status:")
    for item in manager.get_ordered_keys():
        print(f"  {item['key']}: {item['status']}")
        
except Exception as e:
    print(f"Error: {e}")
