"""Schema support for Pydantic and dataclasses."""
from typing import Any, Dict, Optional, Type, Union

def load_with_schema(
    schema: Union[Type, Any],
    path: str = ".env",
    env: Optional[str] = None,
    **kwargs
) -> Any:
    """Load environment variables and validate against a schema.
    
    Args:
        schema: Pydantic BaseModel class or dataclass
        path: path to .env file
        env: environment name
        **kwargs: additional arguments passed to load_env
    
    Returns:
        Schema instance (Pydantic model or dataclass instance)
    """
    from .loader import load_env
    
    # Extract field names from schema
    field_names = _get_schema_fields(schema)
    
    # Create case-insensitive mapping (uppercase env vars -> lowercase field names)
    # Environment variables are typically uppercase, but schema fields might be lowercase
    field_types = _get_field_types(schema)
    field_defaults = _get_field_defaults(schema)
    
    # Map both lowercase and uppercase versions
    types_mapping = {}
    defaults_mapping = {}
    required_vars = []
    optional_vars = []
    
    for field_name in field_names:
        # Map uppercase version (env vars are typically uppercase)
        upper_name = field_name.upper()
        types_mapping[upper_name] = field_types.get(field_name, str)
        if field_name in field_defaults:
            defaults_mapping[upper_name] = field_defaults[field_name]
        
        if _is_required_field(schema, field_name):
            # Only require uppercase (env vars are typically uppercase)
            required_vars.append(upper_name)
        else:
            optional_vars.append(upper_name)
    
    # Load env with schema fields
    config = load_env(
        path=path,
        env=env,
        required=required_vars,
        optional=optional_vars,
        types=types_mapping,
        defaults=defaults_mapping,
        schema=schema,
        **kwargs
    )
    
    # Normalize keys to match schema field names (case-insensitive matching)
    # Environment variables are typically uppercase, schema fields might be lowercase
    normalized_config = {}
    
    # First, map all config values to their schema field names (case-insensitive)
    for key, value in config.items():
        # Find matching field name (case-insensitive)
        for field_name in field_names:
            if key.upper() == field_name.upper():
                normalized_config[field_name] = value
                break
    
    # Convert to schema instance
    return _to_schema_instance(schema, normalized_config)

def _get_schema_fields(schema: Union[Type, Any]) -> list:
    """Extract field names from schema."""
    # Try Pydantic
    try:
        from pydantic import BaseModel
        if issubclass(schema, BaseModel):
            return list(schema.__fields__.keys())
    except (ImportError, TypeError):
        pass
    
    # Try dataclass
    try:
        from dataclasses import fields
        if hasattr(schema, '__dataclass_fields__'):
            return [f.name for f in fields(schema)]
    except Exception:
        pass
    
    return []

def _is_required_field(schema: Union[Type, Any], field_name: str) -> bool:
    """Check if a field is required (no default value)."""
    # Try Pydantic
    try:
        from pydantic import BaseModel
        if issubclass(schema, BaseModel):
            field = schema.__fields__.get(field_name)
            if field:
                return field.required
    except (ImportError, TypeError):
        pass
    
    # Try dataclass
    try:
        import dataclasses
        from dataclasses import fields, MISSING
        if hasattr(schema, '__dataclass_fields__'):
            for f in fields(schema):
                if f.name == field_name:
                    return f.default == MISSING and f.default_factory == MISSING
    except Exception:
        pass
    
    return True  # Default to required

def _get_field_types(schema: Union[Type, Any]) -> Dict[str, type]:
    """Extract type hints from schema."""
    types = {}
    
    # Try Pydantic
    try:
        from pydantic import BaseModel
        if issubclass(schema, BaseModel):
            for name, field in schema.__fields__.items():
                types[name] = field.outer_type_ if hasattr(field, 'outer_type_') else field.type_
    except (ImportError, TypeError):
        pass
    
    # Try dataclass
    try:
        from dataclasses import fields
        import typing
        if hasattr(schema, '__dataclass_fields__'):
            for f in fields(schema):
                types[f.name] = f.type
                # Handle Optional types
                if hasattr(typing, 'get_origin') and typing.get_origin(f.type) is Union:
                    args = typing.get_args(f.type)
                    if len(args) == 2 and type(None) in args:
                        types[f.name] = [a for a in args if a is not type(None)][0]
    except Exception:
        pass
    
    return types

def _get_field_defaults(schema: Union[Type, Any]) -> Dict[str, Any]:
    """Extract default values from schema."""
    defaults = {}
    
    # Try Pydantic
    try:
        from pydantic import BaseModel
        if issubclass(schema, BaseModel):
            for name, field in schema.__fields__.items():
                if not field.required and hasattr(field, 'default'):
                    defaults[name] = field.default
    except (ImportError, TypeError):
        pass
    
    # Try dataclass
    try:
        from dataclasses import fields, MISSING
        if hasattr(schema, '__dataclass_fields__'):
            for f in fields(schema):
                if f.default != MISSING:
                    defaults[f.name] = f.default
                elif f.default_factory != MISSING:
                    defaults[f.name] = f.default_factory()
    except Exception:
        pass
    
    return defaults

def _to_schema_instance(schema: Union[Type, Any], config: Dict[str, Any]) -> Any:
    """Convert config dict to schema instance."""
    # Try Pydantic
    try:
        from pydantic import BaseModel
        if issubclass(schema, BaseModel):
            return schema(**config)
    except (ImportError, TypeError):
        pass
    
    # Try dataclass
    try:
        if hasattr(schema, '__dataclass_fields__'):
            return schema(**config)
    except Exception:
        pass
    
    return config

