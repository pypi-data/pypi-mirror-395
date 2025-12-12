from ..constants import ENABLE_DEV_FEATURES
from .types import _SubparserType


def add_create_command(subparsers: _SubparserType):
    create_parser = subparsers.add_parser("create", help="Create commands")
    create_subparsers = create_parser.add_subparsers(dest="create_command")
    add_create_dataset_command(create_subparsers)
    add_create_project_command(create_subparsers)
    return create_parser


def add_create_dataset_command(create_subparsers: _SubparserType):
    create_dataset_parser = create_subparsers.add_parser("dataset", help="Create a custom dataset for your test")
    create_dataset_parser.add_argument(
        "--seed-prompt",
        type=str,
        help='A seed prompt representing a policy, for which a dataset encouraging violations of the policy will be generated.\nFor example: "The model should never generate harmful, unethical, or illegal content."',
        required=True,
    )
    create_dataset_parser.add_argument(
        "--perspective",
        type=str,
        help="The perspective to use while generating the dataset. This skews the dataset generation towards asking the same question, but through a historical, cultural, etc lens that may subvert a target model.",
        choices=["nonspecific", "historical", "cultural", "scientific"],
        default="nonspecific",
        required=False,
    )
    create_dataset_parser.add_argument(
        "--tone",
        type=str,
        help="The tone to use for the questions in the dataset.",
        choices=["neutral", "forceful", "leading", "innocent", "corrigible", "indirect"],
        default="neutral",
        required=False,
    )
    create_dataset_parser.add_argument(
        "--output-filename",
        type=str,
        help="Name of the file the dataset will be stored in.",
        default="mindgard_custom_dataset.txt",
    )
    create_dataset_parser.add_argument(
        "--num-entries",
        type=int,
        help="Number of dataset entries to generate. Provided number is a goal, but the LLM may generate more or less than requested.",
        default=15,
    )
    return create_dataset_parser


def add_create_project_command(create_subparsers: _SubparserType):
    create_project_parser = create_subparsers.add_parser("project", help="Create a project for your test executions")
    create_project_parser.add_argument(
        "--name",
        type=str,
        help="Name of the project to create.",
        required=True,
    )
