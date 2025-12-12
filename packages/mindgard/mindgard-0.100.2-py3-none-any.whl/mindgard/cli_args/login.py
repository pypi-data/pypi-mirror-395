from .types import _SubparserType


def add_login_command(subparsers: _SubparserType):
    login_parser = subparsers.add_parser("login", help="Login to the Mindgard platform")
    login_parser.add_argument(
        "--instance",
        nargs="?",
        type=str,
        help="Point to your deployed Mindgard instance. If not provided, cli will point towards Mindgard Sandbox",
    )
    return login_parser
