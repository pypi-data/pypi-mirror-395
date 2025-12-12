from ..constants import ENABLE_DEV_FEATURES
from .shared import add_shared_arguments
from .types import _SubparserType


def add_recon_command(subparsers: _SubparserType):
    recon_parser = subparsers.add_parser(
        "recon", help="Run various reconnaissance techniques against your target system"
    )
    recon_subparsers = recon_parser.add_subparsers(title="Recon subcommands", dest="recon_subcommand", required=True)

    # Define prod recon subcommands
    subcommands = {
        "guardrail": "Run guardrail reconnaissance against your target system",
        "input-encoding": "Run input encoding reconnaissance against your target system",
        "output-encoding": "Run output encoding reconnaissance against your target system",
    }
    # Add dev recon subcommands
    if ENABLE_DEV_FEATURES:
        subcommands["non-contextual"] = "Run non-contextual reconnaissance against your target system"
        subcommands["output-format-generation"] = (
            "Run output format generation reconnaissance against your target system"
        )
        subcommands["output-rendering-format"] = "Run output rendering format reconnaissance against your target system"
        subcommands["code-generation"] = "Run code generation reconnaissance against your target system"

    for cmd, help_text in subcommands.items():
        subparser = recon_subparsers.add_parser(cmd, help=help_text)
        add_shared_arguments(subparser)

    recon_parser.add_argument(
        "--project-id",
        type=str,
        help="The project ID to associate the reconnaissance run with.",
        required=False,
    )

    return recon_parser
