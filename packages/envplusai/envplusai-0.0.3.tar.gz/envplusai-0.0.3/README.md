# envplus

**envplus** is a lightweight, robust, and developer-friendly Python package designed to simplify environment variable management. It goes beyond basic `.env` loading by providing built-in type casting, automatic validation, hot reloading, and alias support—all in a single, easy-to-use interface.

## 🚀 Why envplus?

Managing environment variables in Python often involves repetitive boilerplate code:
- Manually casting strings to integers or booleans.
- checking if a variable exists and raising custom errors.
- Restarting the application every time a `.env` value changes during development.
- Handling legacy variable names (aliases) when migrating configurations.

**envplus** solves these problems by providing a centralized `Env` handler that takes care of the heavy lifting, allowing you to focus on building your application. It is designed to work seamlessly with Flask, Django, FastAPI, scripts, and microservices.

## ✨ Features

- **Type Casting**: Effortlessly cast environment variables to `str`, `int`, `float`, `bool`, `list`, and `json`.
- **Auto Validation**: Automatically detect missing keys and invalid types with clear, readable error messages.
- **Hot Reload**: (Development Friendly) Automatically reload values when the `.env` file changes without restarting your app.
- **Alias Support**: Define multiple keys for a single value (e.g., `DATABASE_URL` or `DB_URL`) to support legacy configs.
- **Strict Mode**: Enforce the presence of critical environment variables, raising errors immediately if they are missing.
- **Default Values**: Safe and predictable handling of default values when variables are absent.
- **Debug Console**: A built-in helper to inspect loaded variables (sanitized for security).
- **System Priority**: Always prioritizes system environment variables over `.env` file values.

## 📦 Installation

Install `envplus` via pip:

```bash
pip install envplus
```

## 🛠 Usage

### 1. Basic Setup

Create a `.env` file in your project root:

```ini
APP_ENV=development
DEBUG=true
PORT=8080
ALLOWED_HOSTS=localhost,127.0.0.1
DB_CONFIG={"host": "localhost", "port": 5432}
API_KEY=
```

Initialize `envplus` in your application:

```python
from envplus import Env

# Load environment variables
env = Env()
```

### 2. Reading Variables with Type Casting

Stop doing `int(os.getenv("PORT", 8000))`. Use `envplus` methods instead:

```python
# String (default behavior)
app_env = env.str("APP_ENV", default="production")

# Boolean (handles 'true', '1', 'yes', 'on', etc.)
debug_mode = env.bool("DEBUG", default=False)

# Integer
port = env.int("PORT", default=3000)

# Float
threshold = env.float("THRESHOLD", default=0.5)

# List (auto-splits by comma or custom delimiter)
hosts = env.list("ALLOWED_HOSTS") 
# Result: ['localhost', '127.0.0.1']

# JSON (parses JSON strings into Python objects)
db_config = env.json("DB_CONFIG")
# Result: {'host': 'localhost', 'port': 5432}
```

### 3. Strict Mode & Validation

Ensure your application doesn't start with missing configuration.

```python
# Enable strict mode
env = Env(strict=True)

# This will raise a MissingEnvError if "SECRET_KEY" is not found
secret = env.str("SECRET_KEY")

# This is still safe because a default is provided
optional_val = env.str("OPTIONAL_KEY", default="fallback")
```

### 4. Alias Support

Great for migrations or supporting multiple naming conventions.

```python
# Tries 'DATABASE_URL' first. If missing, tries 'DB_CONNECTION_STRING'.
db_url = env.alias(["DATABASE_URL", "DB_CONNECTION_STRING"])
```

### 5. Hot Reloading

Perfect for local development. If you change your `.env` file while the app is running, `envplus` will pick up the new value on the next access.

```python
# ... modify .env file ...
print(env.str("MY_VAR")) # Returns the updated value!
```

### 6. Debugging

Print a summary of all loaded environment variables to the console.

```python
env.debug()
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
