# Standard library imports
import textwrap

from ..types import valid_llm_datasets
from .shared import add_shared_arguments
from .types import _SubparserType


def add_test_command(subparsers: _SubparserType):
    test_parser = subparsers.add_parser("test", help="Attacks command")
    add_shared_arguments(test_parser)
    test_parser.add_argument(
        "--parallelism",
        type=int,
        help="The maximum number of parallel requests that can be made to the API.",
        required=False,
    )
    test_parser.add_argument(
        "--rate-limit",
        type=int,
        help="The maximum number of requests to make to model in one minute (default: 3600)",
        required=False,
    )
    test_parser.add_argument(
        "--force-multi-turn",
        type=bool,
        help="Enable multi turn attacks in scenarios where they may not be safe, such as when testing an API without chat completions history.",
        required=False,
    )
    test_parser.add_argument(
        "--dataset",
        type=str,
        help=textwrap.dedent(
            f"""
            The dataset to be used for running the attacks on the given model.
            This should be a csv formatted file path, with each prompt on a new line"""
        ),
        required=False,
    )
    test_parser.add_argument(
        "--domain",
        type=str,
        help="The domain to inform the dataset used for LLMs.",
        choices=valid_llm_datasets,
        required=False,
    )
    test_parser.add_argument(
        "--mode",
        type=str,
        help="Specify the number of samples to use during attacks; contact Mindgard for access to 'thorough' or 'exhaustive' test",
        choices=["fast", "thorough", "exhaustive"],
        required=False,
    )
    test_parser.add_argument(
        "--exclude",
        type=str,
        help=textwrap.dedent(
            f"""
            Exclude certain attacks from the test. Exclusions can be done either by name or category.
            The supported attacks can be found here - https://docs.mindgard.ai/user-guide/running-subset-of-attacks#list-of-attacks"""
        ),
        action="append",
        required=False,
    )
    test_parser.add_argument(
        "--include",
        type=str,
        help=textwrap.dedent(
            f"""
            Include a selected set of attacks in the test. A name or category can be provided as part of the inclusion. 
            The supported attacks can be found here - https://docs.mindgard.ai/user-guide/running-subset-of-attacks#list-of-attacks"""
        ),
        action="append",
        required=False,
    )
    test_parser.add_argument(
        "--prompt-repeats",
        type=int,
        help="The number of times to repeat the prompt for each sample in the dataset.",
        required=False,
    )
    test_parser.add_argument(
        "--project-id",
        type=str,
        help="The project ID to associate the test run with.",
        required=False,
    )
    return test_parser
