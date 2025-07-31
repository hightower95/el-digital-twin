
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Optional, Type
from abc import ABC, abstractmethod
from dataclasses import dataclass

if TYPE_CHECKING:
    from el_analysis.models.physical.net import Net
    from el_analysis.models.physical.addressable import Addressable

from el_analysis import logging

class SignalGroup(ABC):
        """
        Base class for signal groups.
        
        This class defines the
        interface for signal groups, which are collections of related signals.
        """
        signal_type: str = "default"  # Default signal type for the group

        def __init__(self):
            self.signals: List[Signal] = []  # List of signals in this group

        @property
        @abstractmethod
        def name(self) -> str:
            """
            The name of the signal group.
            """
            pass

        @property
        def signal_count(self) -> int:
            """
            The number of signals in the group.
            """
            return len(self.signals)

        @abstractmethod
        def add_signal(self, signal: Signal) -> bool:
            """
            Add a signal to the group.
            
            Args:
                signal (Signal): The signal to add to the group.
            """
            if signal not in self.signals:
                self.signals.append(signal)
                return True
            return False

        def __repr__(self):
            return f"SignalGroup(name='{self.name}', signals={self.signals})"


class SignalParserBase(ABC):

    signal_group: Type[SignalGroup] = SignalGroup
    signal_type: str = signal_group.signal_type

    """
    Base class for signal parsers.
    
    This class defines the interface for signal parsers, which are responsible for parsing and managing signals.
    """
    
    @staticmethod
    @abstractmethod
    def parse_signal(signal_name: str) -> Signal:
        """
        Parse a signal by its name.

        Args:
            signal_name (str): The name of the signal to parse.

        Returns:
            Signal: The parsed signal object.
        """
        pass

    @staticmethod
    @abstractmethod
    def can_parse(signal_name: str) -> bool:
        """
        Check if this parser can parse the given signal name.

        Args:
            signal_name (str): The name of the signal to check.

        Returns:
            bool: True if this parser can parse the signal, False otherwise.
        """
        pass

    @staticmethod
    @abstractmethod
    def new_signal_group(signal: Signal) -> SignalGroup:
        """
        Create a new signal group for the given signal.

        Args:
            signal (Signal): The signal to create a new group for.

        Returns:
            SignalGroup: A new instance of SignalGroup.
        """
        pass

# class SignalGroup(ABC):
#     group_id: int = 1000  # Static variable to keep track of group IDs

#     def __init__(self, signal_type: str):
#         self.signal_type: str = signal_type
#         self.signals: List[Signal] = []  # List of signals in this group

#     @abstractmethod
#     def add_signal(self, signal: Signal) -> bool:
#         """
#         Add a signal to the group.
        
#         Args:
#             signal (Signal): The signal to add to the group.
#         """
#         if signal not in self.signals:
#             self.signals.append(signal)
#         return True

#     @abstractmethod
#     def parse_signal(self, signal_name: str) -> Signal:
#         """Add a signal to the group."""
#         if signal not in self.signals:
#             self.signals.append(signal)
        
#     @abstractmethod
#     def can_parse(self, signal_name: str) -> bool:
#         raise NotImplementedError("This method should be implemented by subclasses.")
    
#     @classmethod
#     @abstractmethod
#     def create_new_group(cls, signal: Signal) -> SignalGroup:
#         """
#         Create a new group for the given signal.
        
#         Args:
#             signal (Signal): The signal to create a new group for.
        
#         Returns:
#             SignalGroup: A new instance of SignalGroup.
#         """
#         return cls(signal.signal_type)
    
#     @classmethod
#     def next_id(cls) -> str:
#         """Generate the next group ID."""
#         cls.group_id += 1
#         return "#" + str(cls.group_id)

#     def __repr__(self):
#         return f"SignalGroup(name='{self.name}', signals={self.signals})"

@dataclass(frozen=True)
class SignalData:
    name: str
    channel: str
    signal_type: str


class Signal:
    def __init__(self, name: str, signal_group: Optional[SignalGroup] = None, awg: Optional[str] = "") -> None:
        self.name = name
        self.channel = None
        self.awg: Optional[str] = awg
        self.signal_group: Optional[SignalGroup] = signal_group

        self.twisted_with: List[Signal] = []  # Signals that are twisted with this signal
        self.shielded_by: Optional[Signal] = None  # Signal that shields this signal, if any
        self.is_ground: bool = False

        # self.touchpoints: list[Addressable] = []  # List of connections this signal touches
        self.connections: List[Net] = []
        self.nets = {}  # Dictionary to hold nets associated with this signal

    def __repr__(self):
        return f"Signal(name='{self.name}', minified_name='{self.minified_name}')"
    
    @property
    def signal_type(self) -> str:
        """
        Get the type of the signal.
        
        Returns:
            str: The type of the signal.
        """
        return self.signal_group.signal_type if self.signal_group else SignalGroup.signal_type
    
    @property
    def minified_name(self) -> str:
        """
        Get the minified name of the signal.
        
        Returns:
            str: The minified name of the signal.
        """
        return f"{self.name}_{self.awg}"
    
    
    def attach_net(self, net: Net) -> None:
        """
        Attach a net to this signal.
        
        Args:
            net (Net): The net to attach to this signal.
        """
        if net.connection_id not in self.nets:
            self.nets[net.connection_id] = net
            logging.debug(f"Signal '{self.name}' attached to net '{net.net_id}'")
        
    @property
    def touchpoints(self) -> List[Addressable]:
        """
        Get the list of touchpoints for this signal.
        
        Returns:
            List[Addressable]: The list of touchpoints.
        """
        _touchpoints = set()
        for net in self.nets.values():
            _touchpoints.add(net.source)
            _touchpoints.add(net.destination)
        return list(_touchpoints)