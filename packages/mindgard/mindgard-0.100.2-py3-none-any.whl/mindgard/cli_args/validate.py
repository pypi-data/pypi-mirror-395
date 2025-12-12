from .shared import add_shared_arguments
from .types import _SubparserType


def add_validate_command(subparsers: _SubparserType):
    validate_parser = subparsers.add_parser("validate", help="Validates that we can communicate with your model")
    add_shared_arguments(validate_parser)
    return validate_parser
