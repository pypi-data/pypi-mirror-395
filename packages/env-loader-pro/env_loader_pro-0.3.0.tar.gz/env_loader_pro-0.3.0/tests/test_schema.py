import pytest
from dataclasses import dataclass
from env_loader_pro import load_with_schema, EnvLoaderError

def test_dataclass_schema(tmp_path):
    @dataclass
    class Config:
        port: int
        debug: bool
        api_key: str
    
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=8080\nDEBUG=true\nAPI_KEY=secret123")
    
    config = load_with_schema(Config, path=str(env_file))
    assert config.port == 8080
    assert config.debug is True
    assert config.api_key == "secret123"

def test_dataclass_with_defaults(tmp_path):
    @dataclass
    class Config:
        port: int = 8080
        debug: bool = False
        api_key: str = "default"
    
    env_file = tmp_path / ".env"
    env_file.write_text("API_KEY=secret123")
    
    config = load_with_schema(Config, path=str(env_file))
    assert config.port == 8080  # Default
    assert config.debug is False  # Default
    assert config.api_key == "secret123"  # From env

def test_pydantic_schema(tmp_path):
    pytest.importorskip("pydantic")
    from pydantic import BaseModel
    
    class Config(BaseModel):
        port: int
        debug: bool
        api_key: str
    
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=8080\nDEBUG=true\nAPI_KEY=secret123")
    
    config = load_with_schema(Config, path=str(env_file))
    assert config.port == 8080
    assert config.debug is True
    assert config.api_key == "secret123"
    assert isinstance(config, Config)

def test_pydantic_with_defaults(tmp_path):
    pytest.importorskip("pydantic")
    from pydantic import BaseModel
    
    class Config(BaseModel):
        port: int = 8080
        debug: bool = False
        api_key: str = "default"
    
    env_file = tmp_path / ".env"
    env_file.write_text("API_KEY=secret123")
    
    config = load_with_schema(Config, path=str(env_file))
    assert config.port == 8080
    assert config.debug is False
    assert config.api_key == "secret123"

def test_schema_missing_required(tmp_path):
    @dataclass
    class Config:
        port: int
        api_key: str
    
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=8080")
    
    with pytest.raises(EnvLoaderError):
        load_with_schema(Config, path=str(env_file))

