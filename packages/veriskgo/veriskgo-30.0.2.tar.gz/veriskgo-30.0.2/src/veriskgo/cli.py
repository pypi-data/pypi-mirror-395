# veriskgo/cli.py

import argparse


def main():
    parser = argparse.ArgumentParser(prog="veriskgo")
    parser.add_argument(
        "command",
        help="Available commands: instrument, doctor",
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Root path to instrument (default = current directory)"
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Instrument private functions"
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        help="Function names to exclude"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing"
    )

    args = parser.parse_args()

    # -------------------------
    # instrument command
    # -------------------------
    if args.command == "instrument":
        # Lazy import to prevent dependency errors
        from .cli_instrument import instrument_project

        instrument_project(
            path=args.path,
            skip_private=not args.include_private,
            exclude=args.exclude,
            dry_run=args.dry_run
        )

    # -------------------------
    # doctor command
    # -------------------------
    elif args.command == "doctor":
        # Lazy import here too
        from .cli_doctor import run_doctor
        run_doctor()

    else:
        print(f"Unknown command: {args.command}")
        print("Available commands: instrument, doctor")
