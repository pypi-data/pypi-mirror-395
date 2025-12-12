# Standard library imports
import textwrap

# Project imports
from mindgard.multiturn.attack import VALID_MULTI_TURNS

from .shared import add_shared_arguments
from .types import _SubparserType


def add_run_command(subparsers: _SubparserType):
    run_parser = subparsers.add_parser("run", help="Run a multiturn technique against your target system")
    run_subparser = run_parser.add_subparsers(title="Run subcommands", dest="run_subcommands", required=True)
    add_run_multiturn_command(run_subparser)
    return run_parser


def add_run_multiturn_command(run_subparser: _SubparserType):
    run_multiturn_parser = run_subparser.add_parser("multiturn", help="Run multiturn attacks")
    add_shared_arguments(run_multiturn_parser)
    run_multiturn_parser.add_argument(
        "--goal",
        required=True,
        type=str,
        help="The goal for all multi-turn techniques to run against your system",
    )
    run_multiturn_parser.add_argument(
        "--include",
        type=str,
        choices=VALID_MULTI_TURNS,
        help=textwrap.dedent(
            """
            Include a selected set of attacks in the test.
            """
        ),
        action="append",
        required=True,
    )
    run_multiturn_parser.add_argument(
        "--project-id",
        type=str,
        help="The project ID to associate the multiturn run with.",
        required=False,
    )
    return run_multiturn_parser
