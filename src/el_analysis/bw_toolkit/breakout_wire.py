


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

def signal_compatible(bw: BreakoutWire, coupling: Coupling) -> Compatibility:
    """
    Determines if the breakout wire is compatible with the given coupling.
    
    Args:
        bw (BreakoutWire): The breakout wire to check.
        coupling (Coupling): The coupling to check against.
    
    Returns:
        Compatibility: An enum indicating the compatibility status.
    """
    if bw.compatible_with_interface(coupling.interface):
        return Compatibility.COMPATIBLE
    else:
        return Compatibility.NO_MATCH
    
def connector_compatible(bw: BreakoutWire, connector: Connector, ignore_keying=False) -> Compatibility:
    """
    Determines if the breakout wire is compatible with the given connector.
    
    Args:
        bw (BreakoutWire): The breakout wire to check.
        connector (Connector): The connector to check against.
    
    Returns:
        Compatibility: An enum indicating the compatibility status.
    """
    if bw.compatible_with_interface(connector.interface):
        return Compatibility.COMPATIBLE
    else:
        return Compatibility.NO_MATCH
    

class BreakoutWire:
    def __init__(self, wire_id: str, length: float, resistance: float):
        self._x : Interface = None  # Placeholder for the first connection point

        self.name : str
        pass

    @property
    def connection_id(self) -> str:
        """
        Returns a unique identifier for the wire based on its ID.
        """
        return self.wire_id

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
        # Placeholder logic for creating a wire from an interface
        return cls(wire_id="default_wire", length=1.0, resistance=0.1)

    def __repr__(self):
        return f"BreakoutWire(id={self.wire_id}, length={self.length}, resistance={self.resistance})"