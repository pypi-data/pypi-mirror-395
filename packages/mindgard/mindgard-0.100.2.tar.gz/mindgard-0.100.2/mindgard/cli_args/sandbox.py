from .types import _SubparserType


def add_sandbox_command(subparsers: _SubparserType):
    sandbox_test_parser = subparsers.add_parser("sandbox", help="Test a mindgard example model")
    sandbox_test_parser.add_argument("--json", action="store_true", help="Return json output", required=False)
    sandbox_test_parser.add_argument(
        "--risk-threshold",
        type=int,
        help="Set a flagged event to total event ratio threshold above which the system will exit 1",
        required=False,
        default=80,
    )
    return sandbox_test_parser
