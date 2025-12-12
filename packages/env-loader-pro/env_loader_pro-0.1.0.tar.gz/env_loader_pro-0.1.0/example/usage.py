"""Example usage of env-loader-pro with various features."""

from env_loader_pro import load_env, load_with_schema, generate_env_example

# Example 1: Basic usage with types and defaults
print("=== Example 1: Basic Usage ===")
cfg = load_env(
    path='.env',
    required=['API_KEY'],
    types={'PORT': int, 'DEBUG': bool},
    defaults={'PORT': 8080},
    priority='system'
)
print('Config:', cfg.safe_repr())
print()

# Example 2: Variable expansion
print("=== Example 2: Variable Expansion ===")
# .env should have: BASE_URL=https://example.com and API_ENDPOINT=${BASE_URL}/api
try:
    cfg2 = load_env(path='.env', expand_vars=True)
    if 'API_ENDPOINT' in cfg2:
        print(f"API_ENDPOINT: {cfg2['API_ENDPOINT']}")
except Exception as e:
    print(f"Note: {e}")
print()

# Example 3: Validation rules
print("=== Example 3: Validation Rules ===")
try:
    cfg3 = load_env(
        path='.env',
        types={'PORT': int},
        rules={'PORT': lambda v: 1024 < v < 65535},
        defaults={'PORT': 8080}
    )
    print(f"Port validated: {cfg3['PORT']}")
except Exception as e:
    print(f"Validation error: {e}")
print()

# Example 4: List parsing
print("=== Example 4: List Parsing ===")
# .env should have: DOMAINS=["a.com","b.com"] or DOMAINS=a.com,b.com
try:
    cfg4 = load_env(path='.env', types={'DOMAINS': list})
    if 'DOMAINS' in cfg4:
        print(f"Domains: {cfg4['DOMAINS']}")
except Exception as e:
    print(f"Note: {e}")
print()

# Example 5: Export to file
print("=== Example 5: Export Config ===")
try:
    cfg5 = load_env(path='.env')
    cfg5.save('example_config.json', format='json')
    print("Config exported to example_config.json")
except Exception as e:
    print(f"Export error: {e}")
print()

# Example 6: Generate .env.example
print("=== Example 6: Generate .env.example ===")
try:
    generate_env_example(
        required=['API_KEY', 'DB_URI'],
        optional=['DEBUG', 'LOG_LEVEL'],
        defaults={'PORT': 8080, 'DEBUG': False},
        types={'PORT': int, 'DEBUG': bool},
        output_path='.env.example'
    )
    print(".env.example generated")
except Exception as e:
    print(f"Generation error: {e}")
print()

# Example 7: Dataclass schema (if available)
print("=== Example 7: Dataclass Schema ===")
try:
    from dataclasses import dataclass
    
    @dataclass
    class AppConfig:
        port: int = 8080
        debug: bool = False
        api_key: str = ""
    
    config = load_with_schema(AppConfig, path='.env')
    print(f"Config from schema: port={config.port}, debug={config.debug}")
except Exception as e:
    print(f"Schema error: {e}")
print()

print("=== All examples completed ===")
