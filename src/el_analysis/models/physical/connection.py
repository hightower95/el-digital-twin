from __future__ import annotations
from typing import TYPE_CHECKING

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Interface, Signal, Pin
    from el_analysis import Address
from el_analysis.models.physical.addressable import Addressable

from dataclasses import dataclass
from typing import Optional, Any
from el_analysis import logging, config

@dataclass
class Connection:
    """Base class for connections between addressable objects."""
    source: Addressable
    destination: Addressable

    @property
    def connection_id(self) -> str:
        """Returns a unique identifier for the connection."""
        if self.source is None or self.destination is None:
            raise ValueError("Both source and destination pins must be defined for a net.")

        if self.source.address.address_string < self.destination.address.address_string:
            # Ensure the source is always the one with the lower address
            return f"{self.destination.address}-{self.source.address}"
        else:
            return f"{self.source.address}-{self.destination.address}"


# @dataclass
# class Coupling(Connection):
#     """Represents a coupling between two addressable objects."""
#     coupling_factor: float = 0.0
    

# @dataclass
# class Net(Connection):
#     """Represents a net connection between addressable objects."""
#     net_name: Optional[str] = None
#     net_type: Optional[str] = None
