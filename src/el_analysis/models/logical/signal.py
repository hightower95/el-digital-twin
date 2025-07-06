
from __future__ import annotations
from typing import TYPE_CHECKING

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Pin, Connection
    from el_analysis import Address


from typing import Optional, Any
from el_analysis import logging, config



class Signal:
    def __init__(self, name: str, signal_type: str, group: Optional[str] = None) -> None:
        self.name = name
        self.signal_type = signal_type
        self.group = group
        self.connections: list[Connection] = []

    def add_connection(self, connection: Connection) -> None:
        """Add a connection to this signal."""
        self.connections.append(connection)

    def print_trace(self) -> None:
        """Print the trace of this signal."""
        print(f"Signal: {self.name}, Type: {self.signal_type}, Group: {self.group}")
        for connection in self.connections:
            print(f"  Connection: {connection.start} -> {connection.finish}")

    def __repr__(self) -> str:
        return f"Signal(name={self.name!r}, type={self.signal_type!r}, group={self.group!r})"