# Standard library imports
from argparse import ArgumentParser, _SubParsersAction
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    _SubparserType = _SubParsersAction[ArgumentParser]
else:
    _SubparserType = Any
