"""CLI tool for env-loader-pro."""
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

def main():
    parser = argparse.ArgumentParser(
        description="env-loader-pro: Typed, validated environment variable loader"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show environment variables")
    show_parser.add_argument("--env", help="Environment name (e.g., dev, prod)")
    show_parser.add_argument("--path", default=".env", help="Path to .env file")
    show_parser.add_argument("--format", choices=["json", "yaml", "pretty"], default="pretty")
    show_parser.add_argument("--unmask", action="store_true", help="Show unmasked values")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export config to file")
    export_parser.add_argument("--env", help="Environment name")
    export_parser.add_argument("--path", default=".env", help="Path to .env file")
    export_parser.add_argument("--format", choices=["json", "yaml"], default="json")
    export_parser.add_argument("--output", required=True, help="Output file path")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate environment variables")
    validate_parser.add_argument("--env", help="Environment name")
    validate_parser.add_argument("--path", default=".env", help="Path to .env file")
    validate_parser.add_argument("--required", nargs="+", help="Required variables")
    
    # Generate example command
    gen_parser = subparsers.add_parser("generate-example", help="Generate .env.example file")
    gen_parser.add_argument("--output", default=".env.example", help="Output file path")
    gen_parser.add_argument("--required", nargs="+", help="Required variables")
    gen_parser.add_argument("--optional", nargs="+", help="Optional variables")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == "show":
            cmd_show(args)
        elif args.command == "export":
            cmd_export(args)
        elif args.command == "validate":
            cmd_validate(args)
        elif args.command == "generate-example":
            cmd_generate_example(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_show(args):
    from .loader import load_env
    
    config = load_env(
        path=args.path,
        env=args.env,
        mask_secrets=not args.unmask
    )
    
    if args.format == "json":
        print(json.dumps(config.safe_repr(), indent=2))
    elif args.format == "yaml":
        try:
            import yaml
            print(yaml.dump(config.safe_repr(), default_flow_style=False))
        except ImportError:
            print("PyYAML is required for YAML output. Install with: pip install pyyaml", file=sys.stderr)
            sys.exit(1)
    else:  # pretty
        from .utils import pretty_print_config
        pretty_print_config(config, mask=not args.unmask)

def cmd_export(args):
    from .loader import load_env
    
    config = load_env(
        path=args.path,
        env=args.env
    )
    
    config.save(args.output, format=args.format)
    print(f"Config exported to {args.output}")

def cmd_validate(args):
    from .loader import load_env, EnvLoaderError
    
    try:
        config = load_env(
            path=args.path,
            env=args.env,
            required=args.required or []
        )
        print("✓ Validation passed")
        print(f"Found {len(config)} environment variables")
    except EnvLoaderError as e:
        print(f"✗ Validation failed: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_generate_example(args):
    from .loader import generate_env_example
    
    generate_env_example(
        required=args.required or [],
        optional=args.optional or [],
        defaults={},
        types={},
        output_path=args.output
    )
    print(f"Generated {args.output}")

if __name__ == "__main__":
    main()

