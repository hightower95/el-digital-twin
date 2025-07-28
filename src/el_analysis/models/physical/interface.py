from __future__ import annotations
from typing import TYPE_CHECKING

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Device, Pin
    from el_analysis import Address
    from el_analysis.models.physical.coupling import Coupling
    from el_analysis.models.logical.signal import Signal

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
        self.connected_to: Optional[Interface] = None  # Reference to another interface this one is connected to

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
    
    @property
    def pins(self) -> List[Pin]:
        """Returns a list of pins associated with this interface."""
        return list(self._pins.values())    
    
    @property
    def signals(self) -> List[Signal]:
        """Returns a list of signals associated with this interface."""
        return [pin.signal for pin in self.pins if pin.signal is not None]
    
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
    
    def get_pin(self, pin_name: str) -> Optional[Pin]:
        """ Get pin by name, return None if not found """
        if pin_name in self._pins:
            return self._pins[pin_name]
        else:
            logging.debug(f"Pin {pin_name} not found in interface {self.name}")
            return None

   
    
    def get_minified_part_code(self, include_keying: bool = False) -> Optional[str]:
        return self.connector.get_minified_part_code(include_keying) if self.connector else None

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