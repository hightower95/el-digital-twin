
from __future__ import annotations
from typing import TYPE_CHECKING

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Pin, Connection
    from el_analysis.models.physical.net import Net
    from el_analysis import Address


from typing import Optional, Any
from el_analysis import logging, config
from enum import Enum as enum


# class SignalTypes(enum):
#     POWER = "power"
#     GROUND = "ground"
#     UNKNOWN = "unknown"
#     CAN = "CAN"
#     RS485 = "RS485"
#     ETHERNET = "Ethernet"
#     ANALOG = "Analog"

# class Signal:
#     def __init__(self, name: str, signal_type: SignalTypes, group: Optional[str] = None) -> None:
#         self.name = name
#         self.signal_type = signal_type
#         self.group = group
#         self.connections: list[Connection] = [] # dead?
#         self.nets: list[Net] = []  # List of nets this signal is connected to

#     def add_connection(self, connection: Connection) -> None:
#         """Add a connection to this signal."""
#         self.connections.append(connection)

#     def print_trace(self) -> None:
#         """Print the trace of this signal."""
#         print(f"Signal: {self.name}, Type: {self.signal_type}, Group: {self.group}")
#         for connection in self.connections:
#             print(f"  Connection: {connection.start} -> {connection.finish}")

#     @classmethod
#     def from_signal_name(cls, signal_name: str) -> Optional[Signal]:
#         """Create a Signal instance from a signal name."""
#         if not signal_name:
#             logging.error("Signal name cannot be empty.")
#             return None
        
#         # Here you might want to implement logic to fetch the signal type and group
#         # For now, we'll just return a Signal with default values
#         return cls(name=signal_name, signal_type=SignalTypes.UNKNOWN, group=None)
    
#     def link_to_net(self, net: Any) -> None:
#         """Link this signal to a net."""
#         if net is None:
#             logging.error("Cannot link to a None net.")
#             return
        
#         if net.connection_id in [n.connection_id for n in self.nets]:
#             logging.debug(f"Signal '{self.name}' is already linked to net '{net.connection_id}' - skipping.")
#             return
        
#         self.nets.append(net)
#         logging.info(f"Linked signal '{self.name}' to net '{net.connection_id}'")

#     def __repr__(self) -> str:
#         return f"Signal(name={self.name!r}, type={self.signal_type!r}, group={self.group!r})"