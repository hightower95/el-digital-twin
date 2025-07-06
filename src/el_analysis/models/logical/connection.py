from __future__ import annotations
from typing import TYPE_CHECKING

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Pin, Signal    
    from el_analysis import Address


from typing import Optional, Any
from el_analysis import logging, config

class Connection:
    def __init__(self, a: Pin, b: Pin):
        self.start = a
        self.finish = b
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
