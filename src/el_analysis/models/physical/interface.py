from __future__ import annotations
from typing import TYPE_CHECKING, Dict

# from el_analysis.signal_toolkit.net import Net

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Device, Pin
    from el_analysis import Address
    from el_analysis.models.physical.coupling import Coupling
    from el_analysis.signal_toolkit.signal import Signal
    from el_analysis.signal_toolkit.net import Net

print(f"Loaded {__name__} module successfully.")
from el_analysis.connector_toolkit.connector import Connector
from typing import Optional, Any, List
from el_analysis import logging, config
from el_analysis.models.physical.addressable import Addressable



class Interface(Addressable):
    """Represents an interface for parts or connectors in the BW Analysis module."""

    def __init__(self, name: str, parent: Optional[Device]=None, connector: Optional[Connector]=None):

        self._validation(name)
        self.parent = parent
        if parent is not None:
            if hasattr(parent, "address"):
                _address = parent.address.extend(interface=name)
            else:
                raise AttributeError("Parent object does not have an 'address' attribute.")
        else:
            _address = Address(interface=name)
        super().__init__(address=_address, name=name)
        self._connector: Optional[Connector] = None
        self.connector = connector
        self._pins: dict[str, Pin] = {}  #TODO: Import pins from connector part
        self._connected_to: Optional[Interface] = None  # Reference to another interface this one is connected to

        self._nets: Dict[str, Net] = {}  # Dictionary of nets associated with this interface
        self._internal_nets: List[Net] = []  # List of internal nets
        self._external_nets: List[Net] = []  # List of external nets

        # self._internal_nets: List['Net'] = []  # List of internal nets associated with this interface
        # self._channels: List['Channel'] = []  # List of channels associated with this interface
    
    @property
    def connector(self) -> Optional[Connector]:
        """Returns the connector associated with this interface."""
        return self._connector
    
    @connector.setter
    def connector(self, value: Optional[Connector]):
        """Sets the connector for this interface."""
        if value is not None and not isinstance(value, Connector):
            raise TypeError("Connector must be an instance of Connector class.")
        
        if self._connector is None:
            if value is not None:
                value.used_in.append(self)

        elif self._connector is not value:
            self._connector.used_in.remove(self)
            if value is not None:
                value.used_in.append(self)
        
        self._connector = value

    @property
    def connected_to(self) -> Optional[Interface]:
        """Returns the interface this one is connected to, if any."""
        return self._connected_to
    
    @connected_to.setter
    def connected_to(self, new_value: Optional[Interface]):
        if not isinstance(new_value, Interface) and new_value is not None:
            raise TypeError(f"Connected interface must be an instance of Interface, got {type(new_value)} instead.")
        
        if self._connected_to is new_value:
            # No change, already connected to the same interface
            return
        
        # warn if connecting to same product
        if new_value is not None and new_value.address.same_product(self.address):
            logging.warning(f"Attempted to connect Interface {self.address} to itself - {new_value.address}, allowing connection.")

        if self._connected_to is not None and new_value is None:
            # Disconnecting from the current interface
            logging.info(f"Disconnecting Interface {self.address} from Interface {self._connected_to.address}")
            self._connected_to.connected_to = None
            self._connected_to = None
            return
        
        elif self._connected_to is not None and new_value is not None:
            # We are already connected to another interface, raise an error
            logging.error(f"Interface {self.address} is already connected to {self._connected_to.address}, interfaces only support one connection at a time.")
            raise ValueError(f"Interface {self.address} is already connected to {self._connected_to.address}, interfaces only support one connection at a time.")
        
        elif self._connected_to is None and new_value is None:
            # No connection, nothing to do - unnecessary case included for readability
            return
        
        elif self._connected_to is None and new_value is not None:
            # We are not connected to any interface, connect to the new one
            logging.info(f"Connecting Interface {self.address} to Interface {new_value.address}")
            self._connected_to = new_value
            new_value.connected_to = self


    def _validation(self, interface_name):
        if config.Interface.ValidateInterfaceName:
        
            if not Interface.is_standard_name(interface_name):
                logging.info(f"Attempted to add an interface with an invalid name: {interface_name}")

                if config.Interface.LogNonStandardInterfaceNames:
                    logging.warning(f"Non-standard interface name detected: {interface_name}")
                
                if not config.Interface.AllowNonStandardInterfaceNames:
                    logging.error(f"Non-standard interface names are not allowed: {interface_name}")
                    raise ValueError(f"Interface name '{interface_name}' is not standard and is not allowed.")

    @property
    def device(self):
        return self.parent if self.parent else None
    
    @property
    def part_number(self) -> Optional[str]:
        return self.connector.part_number if self.connector else None
    
    @property
    def part_code(self) -> Optional[str]:
        return self.connector.part_code if self.connector else None
    
    def get_minified_part_code(self, include_keying: bool = False) -> Optional[str]:
        return self.connector.get_minified_part_code(include_keying) if self.connector else None
    
    @property
    def pins(self) -> List[Pin]:
        """Returns a list of pins associated with this interface."""
        return list(self._pins.values())    
    
    @property
    def signals(self) -> List[Signal]:
        """Returns a list of signals associated with this interface."""
        return [pin.signal for pin in self.pins if pin.signal is not None]
    
    @property
    def signal_count(self) -> int:
        """Returns the number of signals associated with this interface."""
        return len(self.signals)
    
    @property
    def coupling(self) -> Optional[Coupling]:
        """Returns the coupling associated with this interface, if any."""
        from el_analysis.models.physical.coupling import Coupling
        if self.connected_to is not None:
            return Coupling(self, self.connected_to)
        return None

    def _make_pin(self, name, *args, **kwargs) -> Pin:
        from el_analysis.models import Pin
        return Pin(name, parent=self, *args, **kwargs)

    def add_pin(self, pin_name: str) -> Pin:
        """ Lookup or create pin by name, return created Pin """
        if not pin_name:
            logging.error(f"Attempted to add a pin with an empty name to device {self.name}")
            raise ValueError("Pin name cannot be empty.")

        if pin_name in self._pins:
            pin_obj = self._pins[pin_name]
        else:
            pin_obj = self._make_pin(pin_name)

        self._pins[pin_name] = pin_obj
        logging.debug(f"Adding Pin {pin_name} to interface {self.name} ({self.address})")
        return pin_obj

    def get_pin(self, pin_name: str, create_if_not_found: bool = False) -> Optional[Pin]:
        """ Get pin by name, return None if not found """
        if pin_name in self._pins:
            return self._pins[pin_name]
        elif create_if_not_found:
            return self.add_pin(pin_name)
        else:
            logging.debug(f"Pin {pin_name} not found in interface {self.name}")
            return None

    def _make_net(self, from_pin: Pin, to_pin: Pin, signal: Signal, internal: bool = False, awg: Optional[str] = None) -> Net:
        """ Create a net between two pins, return the created Net """
        from el_analysis.models.physical.pin import Pin
        if not isinstance(from_pin, Pin) or not isinstance(to_pin, Pin):
            raise TypeError("Both from_pin and to_pin must be instances of Pin.")
        
        # warn if net is to another product
        if not from_pin.address.same_location(to_pin.address):
            logging.warning(f"Creating a net between pins {from_pin.name} and {to_pin.name} in different locations: {from_pin.address} and {to_pin.address}.")

        net_name = f"{from_pin.address}-{to_pin.address}"
        if net_name in self._nets:
            # logging.debug(f"Net {net_name} already exists in interface {self.name}, returning existing net.")
            return self._nets[net_name]

        net = signal.make_net(from_pin, to_pin)
        from_pin._attach_net(net)
        to_pin._attach_net(net)
        if internal:
            logging.debug(f"Creating internal net {net.net_id} between {from_pin.name} and {to_pin.name} in interface {self.name}")
            self._internal_nets.append(net)
        else:
            logging.info(f"Creating net {net.net_id} between {from_pin.name} and {to_pin.name} in interface {self.name}")
            self._external_nets.append(net)

        self._nets[net_name] = net
        return net

    def create_net(self, source_pin: Pin, other_pin: Pin, signal: Signal, create_pins_if_not_exists: bool = True, awg: Optional[str] = None) -> Net:
        """ Connect a pin to another pin with a signal.
        This method sets the `connected_to` property of this interface to the other interface.
        @param pin_name: The name of the pin to connect.
        @param other: The pin to connect to.
        @param signal: The signal to associate with the connection.
        """
        from el_analysis.models.physical.pin import Pin
        
        if not isinstance(source_pin, Pin):
            logging.error(f"Attempted to connect {self.address} to a non-pin object: {source_pin}")
            raise TypeError(f"The 'source_pin' parameter must be an instance of Pin - got {type(source_pin)}.")
        if not isinstance(other_pin, Pin):
            logging.error(f"Attempted to connect {self.address} to a non-pin object: {other_pin}")
            raise TypeError(f"The 'other' parameter must be an instance of Pin - got {type(other_pin)}.")

        # check source pin is in this interface
        if source_pin.interface is not self:
            logging.error(f"Pin {source_pin.name} is not in interface {self.name}, cannot create net.")
            raise ValueError(f"Pin {source_pin.name} is not in interface {self.name}, cannot create net.")

        is_internal = not other_pin.address.same_product(self.address)
        new_net = self._make_net(source_pin, other_pin, signal, internal=is_internal, awg=awg)

        signal.attach_net(new_net)

        if other_pin.interface is not None:
            self.connect_to(other_pin.interface)

        return new_net

    def get_channels(self) -> Dict[str, List[Signal]]:
        """ Returns a list of channels associated with this interface.
        This method is a placeholder and should be implemented in subclasses.
        """
        from el_analysis.signal_toolkit import group_signal_list_by_signal_type
        return group_signal_list_by_signal_type(self.signals)


    @staticmethod
    def is_standard_name(name: str) -> bool:
        """Check if the interface name is a standard name.
        It is a standard name if it starts with 'X' or 'J' and is followed by digits.
        @param name: The name of the interface.
        @return: True if the name is standard, False otherwise.
        """
        return name.startswith("X") or name.startswith("J") or name[1:].isdigit()
    
    @property
    def mated_with(self) -> Optional[Interface]:
        """Returns the interface this one is mated with, if any."""
        return self.connected_to
    
    @property
    def coupled_to(self) -> Optional[Any]:
        """Returns the interface this one is coupled with, if any."""
        return self.connected_to

    @staticmethod
    def connect_interfaces(interface_a: Interface, interface_b: Interface) -> Coupling:
        """Connect two interfaces together.
        This method sets the `connected_to` property of both interfaces to each other.
        @param interface_a: The first interface to connect.
        @param interface_b: The second interface to connect.
        """
        from el_analysis.models.physical.coupling import Coupling
        if not isinstance(interface_a, Interface) or not isinstance(interface_b, Interface):
            raise TypeError("Both arguments must be instances of Interface.")
        
        interface_a.connect_to(interface_b)
        interface_b.connect_to(interface_a)

        return Coupling(interface_a, interface_b)
    
    def connect_to(self, other: Interface) -> bool:
        """Connect this interface to another interface.
        This method sets the `connected_to` property of this interface to the other interface.
        @param other: The interface to connect to.
        """
        if not isinstance(other, Interface):
            logging.error(f"Attempted to connect {self.address} to a non-interface object: {other}")
            raise TypeError("The 'other' parameter must be an instance of Interface.")

        if self.connected_to is not None:
            if self.connected_to is other:
                logging.debug(f"In connecting {self.address} to {other.address}, found interfaces are already connected, no action taken.")
                return True
            else:
                logging.error(f"Interface {self.address} is already connected to {self.connected_to.address}, interfaces only support one connection at a time.")
                raise ValueError(f"Interface {self.address} is already connected to {self.connected_to.address}, interfaces only support one connection at a time.")

        if other.address.same_product(self.address):
            logging.warning(f"Attempted to connect Interface {self.address} to itself, allowing connection.")

        self.connected_to = other
        logging.info(f"Connected Interface {self.address} to Interface {other.address}")
        return True
    
    def search_by_address(self, address: Address, create_if_not_exists: bool = False) -> Optional[Addressable]:
        """
        Retrieves a device by its address.
        
        Args:
            address (str): The address of the device.
            create_if_not_exists (bool): Whether to create the device if it does not exist.
        
        Returns:
            Device: The device with the specified address.
        """
        logging.debug(f"Searching for pin by address: {address}, as_tuple: {address.as_tuple()}")
        
        if address.pin is None:
            logging.error(f"Address {address} does not contain a pin name, cannot find device")
            return None

        found_device = self.get_pin(address.pin)

        if create_if_not_exists and found_device is None:
            found_device = self.add_pin(address.pin)

        logging.debug(f"Found pin: {found_device} for address: {address}, as_tuple: {address.as_tuple()}")

        return found_device
    
    def __repr__(self):
        if self.connector:
            return f"Interface(name={self.name}, parent={self.parent}, address={self.address}, connector={self.connector})"
        else:
            # If no connector is set, we still want to show the basic info
            return f"Interface(name={self.name}, parent={self.parent}, address={self.address})"