from .types import _SubparserType


def add_list_command(subparsers: _SubparserType):
    list_parser = subparsers.add_parser("list", help="List items")
    list_subparsers = list_parser.add_subparsers(dest="list_command")
    list_test_parser = list_subparsers.add_parser("tests", help="List tests")
    list_subparsers.add_parser("projects", help="List projects")
    list_test_parser.add_argument("--json", action="store_true", help="Return json output", required=False)
    list_test_parser.add_argument("--id", type=str, help="Get the details of a specific test.", required=False)
    return list_parser
