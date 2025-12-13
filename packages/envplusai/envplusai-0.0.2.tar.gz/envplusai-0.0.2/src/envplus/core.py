import os
import sys
from typing import Any, List, Optional, Union, Dict
from pathlib import Path
from dotenv import dotenv_values
from .exceptions import MissingEnvError, ValidationError
from .utils import to_bool, to_list, to_json

class Env:
    def __init__(self, env_file: str = ".env", strict: bool = False):
        self.env_file = Path(env_file).resolve()
        self.strict = strict
        self._cache: Dict[str, str] = {}
        self._last_modified: float = 0.0
        self.load()

    def load(self) -> None:
        """Load environment variables from .env file and system environment."""
        # Check if .env file exists and has been modified
        if self.env_file.exists():
            current_mtime = self.env_file.stat().st_mtime
            if current_mtime > self._last_modified:
                self._cache = dotenv_values(self.env_file)
                self._last_modified = current_mtime
        else:
            self._cache = {}

    def _get_raw(self, key: str) -> Optional[str]:
        """Get raw string value from system env or .env file."""
        # Hot reload check
        if self.env_file.exists():
             current_mtime = self.env_file.stat().st_mtime
             if current_mtime > self._last_modified:
                 self.load()

        # System env takes priority
        if key in os.environ:
            return os.environ[key]
        
        # Fallback to .env
        return self._cache.get(key)

    def get(self, key: str, default: Any = None, cast: Any = None) -> Any:
        """Get environment variable with optional casting."""
        value = self._get_raw(key)

        if value is None:
            if default is not None:
                return default
            if self.strict:
                raise MissingEnvError(f"Missing required environment variable: {key}")
            return None

        if cast:
            try:
                return cast(value)
            except Exception as e:
                raise ValidationError(f"Failed to cast {key}='{value}': {e}") from e
        
        return value

    def str(self, key: str, default: Any = None) -> str:
        val = self.get(key, default=default)
        if val is None:
             # If default is None and not strict, return None (or empty string? Prompt says "Default must return only when variable is absent or empty")
             # But return type hint is str. Let's return None if optional, but strict mode handles required.
             return None 
        return str(val)

    def int(self, key: str, default: Any = None) -> int:
        return self.get(key, default=default, cast=int)

    def float(self, key: str, default: Any = None) -> float:
        return self.get(key, default=default, cast=float)

    def bool(self, key: str, default: Any = None) -> bool:
        return self.get(key, default=default, cast=to_bool)

    def list(self, key: str, default: Any = None, delimiter: str = ",") -> List[str]:
        return self.get(key, default=default, cast=lambda v: to_list(v, delimiter))

    def json(self, key: str, default: Any = None) -> Any:
        return self.get(key, default=default, cast=to_json)

    def alias(self, keys: List[str], default: Any = None) -> Any:
        """Try multiple keys in order."""
        for key in keys:
            val = self._get_raw(key)
            if val is not None:
                return val
        
        if default is not None:
            return default
            
        if self.strict:
             raise MissingEnvError(f"Missing required environment variables: {keys}")
        return None

    def debug(self) -> None:
        """Print all loaded environment variables."""
        print("DEBUG: Loaded Environment Variables")
        print("-" * 40)
        
        # Combine system and .env for display
        all_keys = set(os.environ.keys()) | set(self._cache.keys())
        
        for key in sorted(all_keys):
            val = self._get_raw(key)
            print(f"{key}={val}")
        print("-" * 40)
