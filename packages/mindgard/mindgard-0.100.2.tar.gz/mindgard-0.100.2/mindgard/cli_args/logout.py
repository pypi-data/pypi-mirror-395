from .types import _SubparserType


def add_logout_command(subparsers: _SubparserType):
    return subparsers.add_parser("logout", help="Logout of the Mindgard platform in the CLI")
