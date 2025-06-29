from __future__ import annotations
from typing import TYPE_CHECKING

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Pin    
    from el_analysis import Address


from typing import Optional, Any
from el_analysis import logging, config

class Connection:
    def __init__(self, a: Pin, b: Pin):
        self.start = a
        self.finish = b
        self.channel = None

    def connect(self):
        # Logic to connect interface_a and interface_b
        pass
