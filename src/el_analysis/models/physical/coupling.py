from __future__ import annotations
from typing import TYPE_CHECKING

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Interface, Connection, Signal, Pin
    from el_analysis import Address

from dataclasses import dataclass
from typing import Optional, Any
from el_analysis import logging, config
from el_analysis.models.physical.connection import Connection

@dataclass
class Coupling(Connection):
    """Represents a coupling between two pins or interfaces in the BW Analysis module."""
    pass