[![PyPI version](https://badge.fury.io/py/llm7token.svg)](https://badge.fury.io/py/llm7token)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/llm7token)](https://pepy.tech/project/llm7token)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://www.linkedin.com/in/eugene-evstafev-716669181/)

# llm7token

`llm7token` is a lightweight Python utility for working with encrypted access tokens issued by the LLM7 API. It allows local validation, existence checking, and usage stat submission without requiring database access.

## Installation

To install `llm7token`, use pip:

```bash
pip install llm7token
````

## Usage

Set required environment variables:

```bash
export LLM7_SECRET_KEY="your-secret"
export LLM7_TOKEN_URL="https://llm7-api.chigwel137.workers.dev"
export LLM7_SALT="some-salt"
```

### Validate token (decrypt and check expiration)

```python
from llm7token import is_token_valid

valid = is_token_valid("your_token_string")
print(valid)  # True or False
```

### Introspect a token via API

```python
from llm7token import introspect_token

info = introspect_token("your_token_string")
print(info)  # e.g., {"email": "...", "sub": 1} or {"error": "..."}
```

### Check if token exists remotely

```python
from llm7token import token_exists

exists = token_exists("your_token_string")
print(exists)  # True or False
```

### Submit usage stats to the API

```python
from llm7token import record_usage

success = record_usage(
    email="user@example.com",
    token_value="your_token_string",
    model="gpt-4",
    tokens_in=123,
    tokens_out=456
)
print(success)  # True or False
```

## Features

* Secure AES-GCM token decryption using PBKDF2 with SHA-256
* Offline token expiration validation
* Remote token introspection via `/tokens/introspect`
* Remote token existence check
* API usage logging via `/admin/stats` endpoint
* Minimal dependencies: `cryptography`, `requests`

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/chigwell/llm7token/issues).

## License

`llm7token` is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
