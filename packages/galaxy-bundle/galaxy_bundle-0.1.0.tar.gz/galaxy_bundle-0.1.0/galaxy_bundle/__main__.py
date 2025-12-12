"""
Galaxy Bundle CLI

Usage:
    python -m galaxy_bundle              # Show help
    python -m galaxy_bundle starters     # List all starters
    python -m galaxy_bundle versions     # Show all versions
    python -m galaxy_bundle info         # Show general info
"""

import sys
from galaxy_bundle.info import show_info, show_starters, show_versions


def main() -> None:
    """Main entry point for CLI."""
    if len(sys.argv) < 2:
        show_info()
        return
    
    command = sys.argv[1].lower()
    
    if command in ("help", "-h", "--help"):
        show_info()
    elif command == "starters":
        if len(sys.argv) > 2:
            show_starters(sys.argv[2])
        else:
            show_starters()
    elif command == "versions":
        if len(sys.argv) > 2:
            show_versions(sys.argv[2])
        else:
            show_versions()
    elif command == "info":
        show_info()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: starters, versions, info, help")
        sys.exit(1)


if __name__ == "__main__":
    main()

