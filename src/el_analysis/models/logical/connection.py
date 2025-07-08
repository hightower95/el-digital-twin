from __future__ import annotations
from typing import TYPE_CHECKING

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Pin, Signal, Interface    
    from el_analysis import Address


from typing import Optional, Any
from el_analysis import logging, config

# We have connections between interfaces, which are the logical connections between devices.
# Pin connections are physical connections between pins on a device and are implied by the interfaces
class Connection:
    def __init__(self, a: Interface, b: Interface):
        self.start: Interface = a
        self.finish: Interface = b
        self.channel = None
        self.signal: Optional[Signal] = None

    def connect(self):
        # Logic to connect interface_a and interface_b
        pass

    @property
    def signal_type(self) -> Optional[str]:
        """Returns the signal type of the connection."""
        if self.signal:
            return self.signal.signal_type
        return None
    

    @property
    def minified_connectors(self) -> tuple[Optional[str], Optional[str]]:
        """Returns the minified part types of the connectors, if available."""
        if self.start and self.start.connector:
            start_minified = self.start.connector.minified_part_type
        else:
            start_minified = None

        if self.finish and self.finish.connector:
            finish_minified = self.finish.connector.minified_part_type
        else:
            finish_minified = None

        return start_minified, finish_minified
    
    # def get_connector_types(self, minified=False, sorted=False) -> tuple[Optional[str], Optional[str]]:
    #     """Returns the part types of the connectors, optionally minified."""
    #     if self.start and self.start.connector:
    #         start_type = self.start.connector.get_minified_part_type(include_keying=minified)
    #     else:
    #         start_type = None

    #     if self.finish and self.finish.connector:
    #         finish_type = self.finish.connector.get_minified_part_type(include_keying=minified)
    #     else:
    #         finish_type = None

    #     if sorted:
    #         return tuple(sorted([start_type, finish_type]))
    #     return start_type, finish_type
