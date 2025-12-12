# mindgard/cli_args/__init__.py
# Standard library imports
import argparse
from typing import TYPE_CHECKING, Any, List

from ..constants import ENABLE_DEV_FEATURES, VERSION
from ..types import log_levels
from .create import add_create_command
from .list import add_list_command
from .login import add_login_command
from .logout import add_logout_command
from .recon import add_recon_command
from .run import add_run_command
from .sandbox import add_sandbox_command
from .test import add_test_command
from .validate import add_validate_command


def create_parser():
    parser = argparse.ArgumentParser(
        description="Securing AIs",
        prog="mindgard",
        usage="%(prog)s [command] [options]",
        epilog="Enjoy the program! :)",
        add_help=True,
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {VERSION}", help="Show the current version number"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        help="Specify the output verbosity",
        choices=log_levels,
        required=False,
        default="warn",
    )
    subparsers = parser.add_subparsers(
        dest="command", title="commands", description="Use these commands to interact with the Mindgard API"
    )
    # Add prod commands
    add_login_command(subparsers)
    add_logout_command(subparsers)
    add_sandbox_command(subparsers)
    add_list_command(subparsers)
    add_test_command(subparsers)
    add_validate_command(subparsers)
    add_recon_command(subparsers)
    add_create_command(subparsers)
    add_run_command(subparsers)

    # Add dev commands
    if ENABLE_DEV_FEATURES:
        pass

    return parser


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = create_parser()
    return parser.parse_args(args)
