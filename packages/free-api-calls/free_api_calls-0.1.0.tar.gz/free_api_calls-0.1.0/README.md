# free_calls

**Make API requests using free-tier quota across multiple keys automatically.**

`free_calls` automatically rotates through multiple API keys when quotas are exhausted, allowing you to maximize your free-tier usage across services.

## Installation

```bash
pip install free_calls
```

Or install from source:

```bash
git clone https://github.com/MuOssama/free_calls.git
cd free_calls
pip install -e .
```

## Quick Start

### 1. Set up environment variables

```bash
# Single key
export OPENAI_API_KEY="sk-key1"

# Multiple keys (comma-separated)
export OPENAI_API_KEY="sk-key1,sk-key2,sk-key3"
```

### 2. Use in your code

```python
from free_calls import FreeCallsManager

# Initialize manager
manager = FreeCallsManager(env_prefix="OPENAI_API_KEY")

# Define your API function (key must be first parameter)
def call_openai_api(api_key, prompt):
    import openai
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response

# Call with automatic rotation
try:
    result = manager.call_with_rotation(
        call_openai_api,
        "Hello, world!",
        quota_error_types=(openai.error.RateLimitError,)
    )
    print(result)
except Exception as e:
    print(f"All keys exhausted: {e}")
```

## Features

✅ **Automatic key rotation** - Seamlessly switch to next key when quota is exhausted  
✅ **Runtime status tracking** - See which keys are working and which have failed  
✅ **Multiple API support** - Works with any API service  
✅ **Configurable error types** - Define which exceptions trigger rotation  
✅ **Simple integration** - Minimal code changes required

## How it Works

1. Loads all API keys from environment variable
2. Tries first available key
3. If quota error occurs, marks key as failed and tries next key
4. Failed keys are moved to the end of the list
5. If all keys fail, raises `NoValidAPIKeyError`

## API Reference

### `FreeCallsManager(env_prefix, separator=",")`

Initialize the manager with API keys from environment.

**Parameters:**
- `env_prefix` (str): Environment variable name containing API keys
- `separator` (str): Character separating multiple keys (default: ",")

### `call_with_rotation(api_function, *args, quota_error_types=None, **kwargs)`

Call an API function with automatic key rotation on quota errors.

**Parameters:**
- `api_function` (Callable): Function to call (must accept API key as first parameter)
- `quota_error_types` (tuple): Exception types indicating quota exhaustion
- `*args, **kwargs`: Additional arguments passed to the API function

**Returns:** Result from the API function

### `get_ordered_keys()`

Get runtime list of all API keys ordered by status.

**Returns:** List of dicts with:
- `key` (str): Masked API key (e.g., "sk-1...xyz4")
- `status` (str): Either "active" or "failed"

**Example:**
```python
keys = manager.get_ordered_keys()
for item in keys:
    print(f"{item['key']}: {item['status']}")

# Output:
# sk-2...def5: active   <- working keys first
# sk-3...ghi6: active
# sk-1...abc4: failed   <- failed keys last
```

### `reset()`

Reset all failed keys to try them again.

### `get_current_key()`

Get the current active API key (returns None if all failed).

## Examples

### OpenAI API

```python
from free_calls import FreeCallsManager
import openai

manager = FreeCallsManager("OPENAI_API_KEY")

def chat_completion(api_key, prompt):
    openai.api_key = api_key
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

result = manager.call_with_rotation(
    chat_completion,
    "What is Python?",
    quota_error_types=(openai.error.RateLimitError,)
)
```

### Anthropic Claude API

```python
from free_calls import FreeCallsManager
import anthropic

manager = FreeCallsManager("ANTHROPIC_API_KEY")

def claude_message(api_key, prompt):
    client = anthropic.Anthropic(api_key=api_key)
    return client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

result = manager.call_with_rotation(
    claude_message,
    "Hello!",
    quota_error_types=(anthropic.RateLimitError,)
)
```

### Custom API

```python
from free_calls import FreeCallsManager
import requests

manager = FreeCallsManager("MY_API_KEY")

def my_api_call(api_key, endpoint, data):
    response = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {api_key}"},
        json=data
    )
    if response.status_code == 429:  # Rate limit
        raise Exception("Rate limited")
    return response.json()

result = manager.call_with_rotation(
    my_api_call,
    "https://api.example.com/endpoint",
    {"query": "test"},
    quota_error_types=(Exception,)
)
```

## License

MIT License - see LICENSE file for details

## Author

**Mustapha Ossama** - [MuOssama](https://github.com/MuOssama)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please file an issue on the [GitHub issue tracker](https://github.com/MuOssama/free_calls/issues).
