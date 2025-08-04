from __future__ import annotations
from typing import TYPE_CHECKING

from el_analysis.models.physical.addressable import Addressable

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Interface, Pin
    from el_analysis import Address
    from el_analysis.signal_toolkit.signal import Signal

from dataclasses import dataclass
from typing import Optional, Any
from el_analysis import logging, config
from el_analysis.models.physical.connection import Connection

@dataclass
class Net(Connection):
    '''Represents a net in the EL Analysis tool.
    A net is a connection between two pins, which can be on the same or different devices.
    
    A net is supposed to be the simplest physical connection between two points.
    This means it has no knowledge of twisting / shielding - simply the two points it joins together
    and the signal that is carried by that connection and AWG data
    '''
    # source: Addressable
    # destination: Addressable
    signal: Signal
    # other data fields
    awg: Optional[str] = None

    @property
    def is_internal(self) -> bool:
        from el_analysis.core import Address
        """Returns True if the net is internal (i.e., both source and destination are on the same device)."""
        return Address.product_match(self.source.address, self.destination.address)

    @property
    def net_id(self) -> str:
        """Returns a unique identifier for the net."""
        return self.connection_id
        # if self.source is None or self.destination is None:
        #     raise ValueError("Both source and destination pins must be defined for a net.")

        # if self.source.address.address_string < self.destination.address.address_string:
        #     # Ensure the source is always the one with the lower address
        #     return f"{self.destination.address}-{self.source.address}"
        # else:
        #     return f"{self.source.address}-{self.destination.address}"

    def flipped(self) -> Net:
        """Returns a new Net with the source and destination flipped."""
        return Net(source=self.destination, destination=self.source, signal=self.signal)

    def get_pin(self, address: Address) -> Optional[Pin]:
        from el_analysis.models.physical.pin import Pin
        """Returns the pin with the given address, if it exists."""
        if not isinstance(self.source, Addressable) or not isinstance(self.destination, Addressable):
            return None

        if self.source.address.interface_address == address.interface_address:
            if not isinstance(self.source, Pin):
                logging.warning(f"Source {self.source} is not a Pin, cannot get pin by address {address}.")
                return None
            return self.source if self.source else None

        elif self.destination.address.interface_address == address.interface_address:
            if not isinstance(self.destination, Pin):
                logging.warning(f"Destination {self.destination} is not a Pin, cannot get pin by address {address}.")
                return None
            return self.destination if self.destination else None

        else:
            logging.warning(f"Address {address} does not match either source or destination of net {self.net_id}.")

        return None