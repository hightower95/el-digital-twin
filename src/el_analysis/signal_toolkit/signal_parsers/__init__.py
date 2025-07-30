from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from el_analysis.signal_toolkit.signal import SignalParserBase

_SIGNAL_PARSERS = [

]

def add_signal_parser(parser: SignalParserBase):
    """
    Register a new signal parser.
    
    Args:
        parser (SignalParserBase): The signal parser to register.
    """
    _SIGNAL_PARSERS.append(parser)