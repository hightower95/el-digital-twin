from __future__ import annotations
from typing import TYPE_CHECKING

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Interface, Connection
    from el_analysis.signal_toolkit.signal import Signal
    from el_analysis import Address
    from el_analysis.signal_toolkit.net import Net

from dataclasses import dataclass
from typing import Optional, Any, List
from el_analysis import logging, config
from el_analysis.models.physical.addressable import Addressable


# @dataclass
# class PinConfiguration(frozen=True):
#     AWG: str
#     name: str


class Pin(Addressable):
    def __init__(self, name: str, parent: Optional[Interface]=None):
        
        self.parent = parent
        if parent is not None:
            if hasattr(parent, "address"):
                _address = parent.address.extend(pin=name)
            else:
                raise AttributeError("Parent object does not have an 'address' attribute.")
        else:
            _address = Address(pin=name)

        super().__init__(address=_address, name=name)

        self._connecting_pin = None
        # Connection is to another pin
        self.connection: Optional[Connection] = None
        self.nets: List[Net] = []  # List of nets this pin is connected to

    @property
    def interface(self):
        return self.parent if self.parent else None
    
    @property
    def coupling(self) -> Optional[Any]:
        """Returns the coupling associated with this pin, if any."""
        if self.interface is not None and self.interface.coupled_to is not None:
            return self.interface.coupled_to.get_pin(self.name)
        return None
    
    @property
    def signal(self) -> Optional[Signal]:
        """Returns the signal attached the connection on this pin, if any."""
        # if self.connection:
        #     None
            # return self.connection.signal
        for net in self.nets:
            if net.signal is not None:
                return net.signal
        return None
    
    def get_net(self, net_id: str) -> Optional[Net]:
        """Returns the net with the specified ID if it exists."""
        for net in self.nets:
            if net.net_id == net_id:
                return net
        return None
    
    def _attach_net(self, net: 'Net') -> 'Net':

        existing_net = self.get_net(net.net_id)
        if existing_net is not None:
            # A net with this ID is already attached to this pin
            if net.signal != existing_net.signal:
                logging.warning(f"When attaching net {net.net_id} to pin {self.address}, the signal {net.signal} does not match the existing signal {existing_net.signal}."\
                                " This net is ignored")
            else:
                logging.debug(f"Net {net.net_id} is already attached to pin {self.name}, existing signal {existing_net.signal} matches the new signal {net.signal}.")
            return existing_net
        
        if net.source != self and net.destination != self:
            logging.error(f"Net {net.net_id} does not use {self.name} as source")
            raise ValueError(f"Net {net.net_id} does not use {self.name} as source")
        
        for existing_net in self.nets:
            if existing_net.signal != net.signal and existing_net.signal is not None and net.signal is not None:
                logging.warning(f"Pin at {self.address} already has a net with a different signal {existing_net.signal}, new net has signal {net.signal}. This may cause issues.") 
                # return existing_net

        self.nets.append(net)
        return net


    def __repr__(self):
        return (f"Pin(name={self.name!r}, address={self.address!r}, "
                f"interface={self.interface!r})")
    
    # @staticmethod
    # def create_net(pin_a: Pin, pin_b: Pin, signal: Optional[Signal] = None) -> Optional[Net]:
    #     """
    #     Attach a net to two pins.
    #     This is used to create a connection between two pins.
    #     """
    #     from el_analysis.signal_toolkit.net import Net
    #     if pin_a is None or pin_b is None:
    #         logging.error(f"Failed to attach nets to pins - one or both pins are None. Pin A: {pin_a}, Pin B: {pin_b}")
    #         return None
        
    #     # Create a new Net instance and attach it to both pins, where pin_a is the source and pin_b is the destination.
    #     net = Net(pin_a, pin_b, signal=signal)
    #     if signal is not None:
    #         signal.link_to_net(net)

    #     pin_a._attach_net(net)
    #     pin_b._attach_net(net.flipped())

    #     return net


    