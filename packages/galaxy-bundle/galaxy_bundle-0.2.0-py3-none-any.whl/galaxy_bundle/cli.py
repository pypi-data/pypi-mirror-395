"""
Galaxy Bundle CLI

Provides command-line interface for galaxy-bundle.
"""

import argparse
import sys
from galaxy_bundle.info import show_info, show_starters, show_versions
from galaxy_bundle.versions import generate_requirements_txt, STARTERS


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="galaxy-bundle",
        description="🌌 Galaxy Bundle - A BOM-style Dependency Management Package",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  galaxy-bundle starters                 # List all available starters
  galaxy-bundle starters fastapi         # Show packages in fastapi starter
  galaxy-bundle versions                 # Show all curated versions
  galaxy-bundle generate redis fastapi   # Generate requirements.txt
        """,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Info command
    subparsers.add_parser("info", help="Show general information about galaxy-bundle")
    
    # Starters command
    starters_parser = subparsers.add_parser("starters", help="List available starters")
    starters_parser.add_argument(
        "starter",
        nargs="?",
        help="Specific starter to show details for",
    )
    
    # Versions command
    versions_parser = subparsers.add_parser("versions", help="Show curated package versions")
    versions_parser.add_argument(
        "category",
        nargs="?",
        help="Category to filter by",
    )
    
    # Generate command
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate requirements.txt for selected starters",
    )
    generate_parser.add_argument(
        "starters",
        nargs="+",
        choices=list(STARTERS.keys()),
        help="Starters to include",
    )
    generate_parser.add_argument(
        "-o", "--output",
        help="Output file (default: stdout)",
    )
    
    return parser


def main() -> None:
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command is None:
        show_info()
    elif args.command == "info":
        show_info()
    elif args.command == "starters":
        show_starters(args.starter)
    elif args.command == "versions":
        show_versions(args.category)
    elif args.command == "generate":
        content = generate_requirements_txt(args.starters)
        if args.output:
            with open(args.output, "w") as f:
                f.write(content)
            print(f"✅ Generated {args.output}")
        else:
            print(content)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

