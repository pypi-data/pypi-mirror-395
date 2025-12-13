import pytest
import os
import time
from envplus import Env, MissingEnvError, ValidationError

def test_basic_loading(env_file):
    env = Env(env_file=str(env_file))
    assert env.str("TEST_KEY") == "test_value"
    assert env.int("INT_KEY") == 123
    assert env.bool("BOOL_KEY") is True
    assert env.list("LIST_KEY") == ["a", "b", "c"]
    assert env.json("JSON_KEY") == {"a": 1}

def test_system_priority(env_file, clean_env):
    os.environ["TEST_KEY"] = "system_value"
    env = Env(env_file=str(env_file))
    assert env.str("TEST_KEY") == "system_value"

def test_missing_and_default(env_file):
    env = Env(env_file=str(env_file))
    assert env.str("MISSING_KEY") is None
    assert env.str("MISSING_KEY", default="default") == "default"

def test_strict_mode(env_file):
    env = Env(env_file=str(env_file), strict=True)
    with pytest.raises(MissingEnvError):
        env.str("MISSING_KEY")
    
    # Should not raise if default is provided
    assert env.str("MISSING_KEY", default="default") == "default"

def test_type_casting_error(env_file):
    env = Env(env_file=str(env_file))
    with pytest.raises(ValidationError):
        env.int("TEST_KEY") # "test_value" is not int

def test_hot_reload(env_file):
    env = Env(env_file=str(env_file))
    assert env.str("TEST_KEY") == "test_value"
    
    # Modify file
    time.sleep(0.1) # Ensure mtime changes
    env_file.write_text("TEST_KEY=new_value")
    
    assert env.str("TEST_KEY") == "new_value"

def test_alias(env_file):
    env = Env(env_file=str(env_file))
    assert env.alias(["MISSING", "TEST_KEY"]) == "test_value"
    assert env.alias(["MISSING", "ALSO_MISSING"], default="fallback") == "fallback"

def test_alias_strict(env_file):
    env = Env(env_file=str(env_file), strict=True)
    with pytest.raises(MissingEnvError):
        env.alias(["MISSING", "ALSO_MISSING"])

def test_list_delimiter(env_file):
    env_file.write_text("IPS=1.1.1.1;2.2.2.2")
    env = Env(env_file=str(env_file))
    assert env.list("IPS", delimiter=";") == ["1.1.1.1", "2.2.2.2"]
