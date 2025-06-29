

from typing import List, Set
from el_analysis.models import Connection
from abc import ABC, abstractmethod

class ConnectionGroup(ABC):
    def __init__(self) -> None:
        self.is_twisted: bool = False
        self.signal_type: str = ""
        self.channel_name: str = ""

    @property
    @abstractmethod
    def connections(self) -> Set[Connection]:
        """Returns a list of connections in this group."""
        pass

class CAN(ConnectionGroup):
    def __init__(self, channel_name: str) -> None:
        self.signal_type = "CAN"
        self.channel_name = channel_name
        self.is_twisted = True
        self.is_shielded = True
        self.high: Connection
        self.low: Connection 
        self.shield: Connection

    @property
    def all_twisted_groups(self):
        return [(self.high, self.low)]

    @property
    def connections(self) -> Set[Connection]:
        return {self.high, self.low, self.shield}
    
    def can_add_connection(self, connection: Connection) -> bool:
        """Check if a connection can be added to this CAN group."""
        # TODO: logic
        matching_signal_type = False
        matching_channel_name = False
        matching_source_destination = False # Check source interface and destination interface are same as the group
        if connection.signal_type == self.signal_type:
            matching_signal_type = True

        return False
    
    def add_connection(self, connection: Connection) -> None:
        pass
    
    @property
    def group_is_full(self) -> bool:
        """Check if the group is complete."""
        return (self.high is not None and
                self.low is not None and
                self.shield is not None)

    def __repr__(self):
        return f"CAN(channel_name={self.channel_name!r}, connections={self.connections!r})"