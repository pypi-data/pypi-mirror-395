import argparse
import sys
import os
from .core import create_tests


def main():
    parser = argparse.ArgumentParser(
        description="Generate tests for Python code using ghtest."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the source directory (default: current directory)",
    )
    parser.add_argument(
        "--test-dir",
        default="tests",
        help="Directory to output generated tests (default: tests)",
    )
    parser.add_argument(
        "--cassette-dir",
        default="tests/cassettes",
        help="Directory to store VCR cassettes (default: tests/cassettes)",
    )
    parser.add_argument(
        "--unsafe",
        action="store_true",
        help="Run potentially destructive functions without asking for permission",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Enable interactive mode (opposite of --unsafe)",
    )
    parser.add_argument(
        "--verbose", "-v", action="count", default=0, help="Increase verbosity level"
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Do not clean up existing tests and cassettes before running",
    )
    parser.add_argument(
        "--history", action="store_true", help="Use parameter history (default: False)"
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    args = parser.parse_args()

    # Resolve paths
    src_dir = os.path.abspath(args.path)
    test_dir = os.path.abspath(args.test_dir)
    cassette_dir = os.path.abspath(args.cassette_dir)

    # Determine safety mode
    # Default is safe (interactive) unless --unsafe is specified
    # But core.create_tests defaults to unsafe=True in the signature I copied?
    # Let's check core.py signature: unsafe: bool = True
    # So if I want default to be safe, I should pass unsafe=False unless --unsafe is set.
    # Wait, the user asked for "unsafe (for using destructive tsts without asking)".
    # So default should probably be safe (interactive).

    unsafe_mode = args.unsafe
    if args.interactive:
        unsafe_mode = False

    print(f"Generating tests for {src_dir}...")
    print(f"Output directory: {test_dir}")

    try:
        create_tests(
            cassette_dir=cassette_dir,
            test_dir=test_dir,
            src_dir=src_dir,
            clean_up=not args.no_cleanup,
            unsafe=unsafe_mode,
            history=args.history,
            vb=args.verbose,
        )
        print("Test generation complete.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose > 0:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
