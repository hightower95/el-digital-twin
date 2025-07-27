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

    def __post_init__(self):
        from el_analysis.models.physical.interface import Interface
        if not isinstance(self.source, Interface) or not isinstance(self.destination, Interface):
            raise TypeError("Both source and destination must be of type Interface for a Coupling.")
        logging.debug(f"Created Coupling: {self.source.address} <-> {self.destination.address}")

    def get_connection_hash(self, minified: bool = False, ordered: bool = True) -> str:
        """Returns a unique hash for the coupling connection."""
        from el_analysis.models.physical.interface import Interface
        a = self.source 
        b = self.destination
        if a is None or b is None:
            raise ValueError("Both source and destination must be defined for a coupling.")
        
        if ordered:
            if a.address.address_string < b.address.address_string:
                # no reordering needed
                pass
            else:
                a, b = b, a
        if a.address is None or b.address is None:
            raise ValueError("Both source and destination must have addresses for a coupling.")
        
        if not isinstance(a, Interface) or not isinstance(b, Interface):
            raise TypeError("Both source and destination must be of type Interface for a Coupling.")

        if a.connector is None or b.connector is None:
            raise ValueError("Both source and destination must have connectors for a coupling.")

        return f"<{a.connector.get_part_type(minified)}::{b.connector.get_part_type(minified)}>"

    @property
    def connection_hash(self) -> str:
        """Returns a unique hash for the coupling connection."""
        return self.get_connection_hash()
    
    @property
    def minified_connection_hash(self) -> str:
        """Returns a minified unique hash for the coupling connection."""
        return self.get_connection_hash(minified=True)
    
    @property
    def connection_hash_unordered(self) -> str:
        """Returns a unique hash for the coupling connection without ordering."""
        return self.get_connection_hash(ordered=False)
    
    @property
    def minified_connection_hash_unordered(self) -> str:
        """Returns a minified unique hash for the coupling connection without ordering."""
        return self.get_connection_hash(minified=True, ordered=False)