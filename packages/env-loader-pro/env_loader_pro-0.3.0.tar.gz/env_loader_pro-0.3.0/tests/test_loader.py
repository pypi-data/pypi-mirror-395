import os
import json
import pytest
from env_loader_pro import load_env, EnvLoaderError, generate_env_example

def test_load_env_with_defaults(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=5000\nDEBUG=true\nAPI_KEY=abcd1234")
    cfg = load_env(path=str(env_file), types={"PORT": int, "DEBUG": bool}, required=["API_KEY"], defaults={"TIMEOUT": 30})
    assert cfg["PORT"] == 5000
    assert cfg["DEBUG"] is True
    assert cfg["API_KEY"] == "abcd1234"
    assert cfg["TIMEOUT"] == 30

def test_missing_required(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("FOO=bar")
    try:
        load_env(path=str(env_file), required=["API_KEY"]) 
        assert False, "Should have raised EnvLoaderError"
    except EnvLoaderError:
        assert True

def test_variable_expansion(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("BASE_URL=https://example.com\nAPI_ENDPOINT=${BASE_URL}/api")
    cfg = load_env(path=str(env_file))
    assert cfg["API_ENDPOINT"] == "https://example.com/api"

def test_variable_expansion_nested(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("BASE=https://example.com\nAPI=${BASE}/api\nFULL=${API}/v1")
    cfg = load_env(path=str(env_file))
    assert cfg["FULL"] == "https://example.com/api/v1"

def test_variable_expansion_circular(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("A=${B}\nB=${A}")
    with pytest.raises(EnvLoaderError, match="Circular reference"):
        load_env(path=str(env_file))

def test_list_parsing_json(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text('DOMAINS=["a.com","b.com","c.com"]')
    cfg = load_env(path=str(env_file), types={"DOMAINS": list})
    assert cfg["DOMAINS"] == ["a.com", "b.com", "c.com"]

def test_list_parsing_comma_separated(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("LIMITS=10,20,400")
    cfg = load_env(path=str(env_file), types={"LIMITS": list})
    assert cfg["LIMITS"] == ["10", "20", "400"]

def test_multiple_environments(tmp_path):
    base_env = tmp_path / ".env"
    base_env.write_text("PORT=8080\nDEBUG=false")
    
    prod_env = tmp_path / ".env.prod"
    prod_env.write_text("PORT=9000\nDEBUG=true")
    
    # Test prod environment
    cfg = load_env(path=str(tmp_path / ".env"), env="prod")
    assert cfg["PORT"] == "9000"  # From .env.prod
    assert cfg["DEBUG"] == "true"  # From .env.prod

def test_validation_rules(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=8080")
    cfg = load_env(
        path=str(env_file),
        types={"PORT": int},
        rules={"PORT": lambda v: 1024 < v < 65535}
    )
    assert cfg["PORT"] == 8080

def test_validation_rules_fail(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=80")
    with pytest.raises(EnvLoaderError, match="Validation rule failed"):
        load_env(
            path=str(env_file),
            types={"PORT": int},
            rules={"PORT": lambda v: v > 1024}
        )

def test_strict_mode(tmp_path, caplog):
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=8080\nUNKNOWN_VAR=test")
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        cfg = load_env(
            path=str(env_file),
            required=["PORT"],
            types={"PORT": int},
            strict=True
        )
        assert len(w) > 0
        assert "Unknown environment variables" in str(w[0].message)

def test_export_json(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=8080\nAPI_KEY=secret123")
    cfg = load_env(path=str(env_file), types={"PORT": int})
    
    output_file = tmp_path / "config.json"
    cfg.save(str(output_file), format="json")
    
    assert output_file.exists()
    with open(output_file) as f:
        data = json.load(f)
        assert "PORT" in data
        assert "API_KEY" in data

def test_safe_repr(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("API_KEY=secret12345\nPORT=8080")
    cfg = load_env(path=str(env_file), types={"PORT": int})
    
    safe = cfg.safe_repr()
    assert safe["API_KEY"] != "secret12345"
    assert "****" in safe["API_KEY"] or safe["API_KEY"] == "************"
    assert safe["PORT"] == 8080

def test_generate_env_example(tmp_path):
    output_file = tmp_path / ".env.example"
    generate_env_example(
        required=["API_KEY", "DB_URI"],
        optional=["DEBUG"],
        defaults={"PORT": 8080, "DEBUG": False},
        types={"PORT": int, "DEBUG": bool},
        output_path=str(output_file)
    )
    
    assert output_file.exists()
    content = output_file.read_text()
    assert "API_KEY" in content
    assert "DB_URI" in content
    assert "PORT=8080" in content
    assert "DEBUG=False" in content

def test_priority_system(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=8080")
    monkeypatch.setenv("PORT", "9000")
    
    # File priority (default)
    cfg = load_env(path=str(env_file), types={"PORT": int}, priority="file")
    assert cfg["PORT"] == 8080
    
    # System priority
    cfg = load_env(path=str(env_file), types={"PORT": int}, priority="system")
    assert cfg["PORT"] == 9000

def test_bool_casting(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("DEBUG1=true\nDEBUG2=1\nDEBUG3=yes\nDEBUG4=false\nDEBUG5=0\nDEBUG6=no")
    cfg = load_env(
        path=str(env_file),
        types={"DEBUG1": bool, "DEBUG2": bool, "DEBUG3": bool, "DEBUG4": bool, "DEBUG5": bool, "DEBUG6": bool}
    )
    assert cfg["DEBUG1"] is True
    assert cfg["DEBUG2"] is True
    assert cfg["DEBUG3"] is True
    assert cfg["DEBUG4"] is False
    assert cfg["DEBUG5"] is False
    assert cfg["DEBUG6"] is False

def test_expand_vars_disabled(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("BASE_URL=https://example.com\nAPI_ENDPOINT=${BASE_URL}/api")
    cfg = load_env(path=str(env_file), expand_vars=False)
    assert cfg["API_ENDPOINT"] == "${BASE_URL}/api"  # Not expanded
