from __future__ import annotations
from typing import TYPE_CHECKING

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Interface, Connection
    from el_analysis import Address

from dataclasses import dataclass
from typing import Optional, Any
from el_analysis import logging, config


# @dataclass
# class PinConfiguration(frozen=True):
#     AWG: str
#     name: str


class Pin:
    def __init__(self, name: str, parent: Optional[Interface]=None):
        self.name = name
        self.parent = parent
        if parent is not None:
            if hasattr(parent, "address"):
                self.address = parent.address.extend(pin=name)
            else:
                raise AttributeError("Parent object does not have an 'address' attribute.")
        else:
            self.address = Address(pin=name)

        self._connecting_pin = None
        # Connection is to another pin
        self.connection: Optional[Connection] = None

    @property
    def interface(self):
        return self.parent if self.parent else None
    
    @property
    def signal(self) -> Optional[str]:
        """Returns the signal attached the connection on this pin, if any."""
        # if self.connection:
        #     None
            # return self.connection.signal
        return None
    
        

    def __repr__(self):
        return (f"Pin(name={self.name!r}, address={self.address!r}, "
                f"interface={self.interface!r})")