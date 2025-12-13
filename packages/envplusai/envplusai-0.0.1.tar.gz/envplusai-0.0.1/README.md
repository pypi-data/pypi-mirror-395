# envplus

**envplus** is a lightweight Python package for managing environment variables with advanced features like type conversion, auto validation, hot reloading, and alias support.

## Features

- **Type Casting**: Easily cast environment variables to `str`, `int`, `float`, `bool`, `list`, and `json`.
- **Auto Validation**: Detect missing keys and invalid types with clear error messages.
- **Hot Reload**: Automatically reload values when `.env` file changes (lazy reload).
- **Alias Support**: Fallback to alternative keys if the primary key is missing.
- **Strict Mode**: Enforce presence of required variables.
- **Default Values**: Safe handling of defaults.
- **Debug Console**: Inspect loaded variables.

## Installation

```bash
pip install envplus
```

## Usage

### Basic Usage

Create a `.env` file:

```ini
APP_ENV=development
DEBUG=true
PORT=8080
ALLOWED_HOSTS=localhost,127.0.0.1
DB_CONFIG={"host": "localhost", "port": 5432}
```

Use `envplus` in your code:

```python
from envplus import Env

env = Env()

# Read values with type casting
mode = env.str("APP_ENV")
debug = env.bool("DEBUG")
port = env.int("PORT")
hosts = env.list("ALLOWED_HOSTS")
db_config = env.json("DB_CONFIG")

print(f"Mode: {mode}, Debug: {debug}, Port: {port}")
print(f"Hosts: {hosts}")
print(f"DB Config: {db_config}")
```

### Strict Mode

Enable strict mode to raise errors for missing variables without defaults.

```python
env = Env(strict=True)

# Raises MissingEnvError if API_KEY is missing
api_key = env.str("API_KEY")

# Safe with default
api_key = env.str("API_KEY", default="secret")
```

### Aliases

Support legacy or alternative environment variable names.

```python
# Tries DATABASE_URL first, then DB_URL
db_url = env.alias(["DATABASE_URL", "DB_URL"])
```

### Debugging

Print all loaded environment variables (masked values not implemented yet, be careful in production!).

```python
env.debug()
```

## Development Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -e .[dev]
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT
