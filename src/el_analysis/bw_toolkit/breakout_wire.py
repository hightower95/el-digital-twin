


from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from el_analysis.models.physical.coupling import Coupling
    from el_analysis.models.physical.addressable import Addressable
    from el_analysis.connector_toolkit.connector import Connector
    from el_analysis.models.physical.interface import Interface

from enum import Enum

class Compatibility(Enum):
    COMPATIBLE = "match_compatible"
    NON_INDEAL = "match_non_ideal"
    NO_MATCH = "no_match"
    UNKNOWN = "unknown"

    

class BreakoutWire:
    def __init__(self):
        self._x : Interface  # Placeholder for the first connection point
        self._x1 : Interface  # Placeholder for the second connection point
        self._x2 : Interface  # Placeholder for the third connection point
        self._coupling : Coupling
        self.name : str
        pass

    @property
    def connection_id(self) -> str:
        """
        Returns a unique identifier for the wire based on its ID.
        """
        return self._coupling.get_connection_hash(minified=True)

    def compatible_with_interface(self, interface: str) -> bool:
        """
        Determines if the breakout wire can support the given interface.
        
        Args:
            interface (str): The interface type to check compatibility with.
        
        Returns:
            bool: True if the wire can support the interface, False otherwise.
        """
        # Placeholder logic for compatibility check
        return True
    
    
    @classmethod
    def from_coupling(cls, coupling: Coupling) -> 'BreakoutWire':
        """
        Creates a BreakoutWire instance from an interface.
        
        Args:
            interface (str): The interface type to create the wire from.
        
        Returns:
            BreakoutWire: An instance of BreakoutWire.
        """

        for channel in coupling.get_channels():
            if channel.signal is None:
                raise ValueError(f"Channel {channel.name} in coupling {coupling} has no signal.")
            
        
        
        # Placeholder logic for creating a wire from an interface
        return cls(wire_id="default_wire", length=1.0, resistance=0.1)

    def __repr__(self):
        return f"BreakoutWire(id={self.wire_id}, length={self.length}, resistance={self.resistance})"