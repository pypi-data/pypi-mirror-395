# Standard library imports
import argparse

from ..types import type_model_presets_list


def add_shared_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("target", nargs="?", type=str, help="This is your own model identifier.")
    parser.add_argument(
        "--config-file", type=str, help="Path to mindgard.toml config file", default=None, required=False
    )
    parser.add_argument(
        "--json", action="store_true", help="Output the info in JSON format.", required=False, default=False
    )
    parser.add_argument("--headers", type=str, help="The headers to use. Comma separated list.", required=False)
    parser.add_argument(
        "--header", type=str, help="The headers to use, repeat flag for each header.", action="append", required=False
    )
    parser.add_argument("--preset", type=str, help="The preset to use", choices=type_model_presets_list, required=False)
    parser.add_argument("--api-key", type=str, help="Specify the API key for the wrapper", required=False)
    parser.add_argument("--url", type=str, help="Specify the url for the wrapper", required=False)
    parser.add_argument(
        "--model-name", type=str, help="Specify which model to run against (OpenAI and Anthropic)", required=False
    )
    parser.add_argument(
        "--az-api-version", type=str, help="Specify the Azure OpenAI API version (Azure only)", required=False
    )
    parser.add_argument("--prompt", type=str, help="Specify the prompt to use", required=False)
    parser.add_argument("--system-prompt", type=str, help="Text file containing system prompt to use.", required=False)
    parser.add_argument(
        "--selector",
        type=str,
        help="The selector to retrieve the text response from the LLM response JSON.",
        required=False,
    )
    parser.add_argument("--request-template", type=str, help="The template to wrap the API request in.", required=False)
    parser.add_argument(
        "--tokenizer",
        type=str,
        help="Choose a HuggingFace model to provide a tokeniser for prompt and chat completion templating.",
        required=False,
    )
    parser.add_argument(
        "--risk-threshold",
        type=int,
        help="Set a flagged event to total event ratio threshold above which the system will exit 1",
        required=False,
    )
