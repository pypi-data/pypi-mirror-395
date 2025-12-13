"""Main entry point for Green Microservices Mining CLI."""

import sys

from cli import cli

from greenmining.utils import colored_print, print_banner


def main():
    """Main entry point with error handling."""
    try:
        print_banner("🌱 Green Microservices Mining Tool")
        colored_print("Analyze GitHub repositories for sustainability practices\n", "cyan")

        cli(obj={})

    except KeyboardInterrupt:
        colored_print("\n\n⚠️  Operation cancelled by user", "yellow")
        sys.exit(130)

    except Exception as e:
        colored_print(f"\n❌ Unexpected error: {e}", "red")

        if "--verbose" in sys.argv or "-v" in sys.argv:
            import traceback

            colored_print("\nFull traceback:", "red")
            traceback.print_exc()
        else:
            colored_print("Run with --verbose for detailed error information", "yellow")

        sys.exit(1)


if __name__ == "__main__":
    main()
