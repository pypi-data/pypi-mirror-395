# Command Line Interface (CLI) code

import argparse
from .pip_package_extract import extract_pip_requirement, generate_full_requirements

def main():
    parser = argparse.ArgumentParser(
        description="minireqs command line interface"
    )

    # Create subparsers for subcommands
    subparsers = parser.add_subparsers(
        title="subcommands",
        dest="command",
        required=True
    )

    # ---- MINI command ----
    mini_cmd = subparsers.add_parser(
        "mini",
        help="Generate a minimum set of requirements based on import statements in python scripts."
    )
    mini_cmd.add_argument("-i", required=True, help="Input file path")
    mini_cmd.add_argument("-o", required=True, help="Output file path")

    # ---- FULL command ----
    full_cmd = subparsers.add_parser(
        "full",
        help="Generate a full reproducible set of requirements based on a base requirement file"
    )
    full_cmd.add_argument("-i", required=True, help="Input file path")
    full_cmd.add_argument("-o", required=True, help="Output file path")

    args = parser.parse_args()

    # Dispatch based on subcommand
    if args.command == "mini":
        extract_pip_requirement(args.i, args.o)
    elif args.command == "full":
        generate_full_requirements(args.i, args.o)


if __name__ == "__main__":
    main()
