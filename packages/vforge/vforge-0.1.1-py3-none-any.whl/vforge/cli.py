#!/usr/bin/env python3
import argparse
from vforge import helpers
import os
import subprocess
import sys

def main():
    # Create parser to handle arguments passed to CLI
    log = helpers.make_logger()
    parser = argparse.ArgumentParser(
        description="vforge command line tool"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init command args
    parser_init = subparsers.add_parser("init", help="Initialize a vforge venv")
    parser_init.add_argument(
        "--venv-name",
        type=str,
        default="vforge_venv",
        metavar="",
        help="Name of the virtual environment to create"
    )
    parser_init.add_argument(
        "--target-dir",
        type=str,
        default=os.getcwd(),
        metavar="",
        help="Parent directory to host the virtual environment (defaults to current working directory)"
    )
    parser_init.add_argument(
        "--project-dir",
        type=str,
        default=os.getcwd(),
        metavar="",
        help="Project directory to build the virtual environment from (defaults to current working directory)"
    )
    parser_init.add_argument(
        "--sync",
        type=str,
        default="y",
        metavar="",
        help="Automatically call vforge sync after init (y/n)? (defaults to y)"
    )

    # sync command args
    parser_sync = subparsers.add_parser("sync", help="Install packages to the venv")
    parser_sync.add_argument(
        "--project-dir",
        type=str,
        default=os.getcwd(),
        metavar="",
        help="Project directory to build the virtual environment from (defaults to current working directory)"
    )

    # purge command args
    parser_purge = subparsers.add_parser("purge", help="Remove unused packages from venv")
    parser_purge.add_argument(
        "--project-dir",
        default=os.getcwd(),
        metavar="",
        help="Project directory (defaults to current working directory)"
    )

    # freeze command args
    parser_freeze = subparsers.add_parser("freeze", help="Generate requirements.txt from virtual environment.")
    parser_freeze.add_argument(
        "--project-dir",
        type=str,
        default=os.getcwd(),
        metavar="",
        help="Path of the virtual environment"
    )
    parser_freeze.add_argument(
        "--out-dir",
        type=str,
        default=os.getcwd(),
        metavar="",
        help="Directory to send the file to (defaults to current working directory)"
    )


    # help command
    parser_help = subparsers.add_parser("help", help="Display vforge help information")

    args, unknown = parser.parse_known_args()

    if args.command == "help":
        # brief user guide
        log.info(
            "vforge CLI\n"
            "Commands:\n"
            "  init      Initialize a vforge virtual environment\n"
            "  sync      Install packages into a vforge virtual environment\n"
            "  purge     Remove unused packages from a vforge virtual environment\n"
            "  freeze    Generate requirements.txt file from a vforge virtual environment\n"
            "Usage:\n"
            "  vforge <command> [--flags]\n"
            "Use 'vforge <command> --help' for command-specific arguments."
        )
        return

    # all available commands are in this dict
    commands = {
        "init": "vforge.init",
        "sync": "vforge.sync",
        "purge": "vforge.purge",
        "freeze": "vforge.freeze"
    }

    # safely retrieve command and alert user if not found
    script = commands.get(args.command)
    if not script:
        print(f"Unknown command: {args.command}")
        sys.exit(1)

    # set up arguments for the script
    arg_list = [sys.executable, "-m", script]
    for key, value in vars(args).items():
        if key in ("command",):
            continue
        if value is not None:
            arg_list.append(f"--{key.replace('_', '-')}")
            arg_list.append(str(value))

    arg_list.extend(unknown)

    # call the script
    subprocess.run(arg_list)