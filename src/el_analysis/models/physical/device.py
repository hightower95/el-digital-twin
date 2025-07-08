# from ... import logging, config, Address
from __future__ import annotations
from typing import TYPE_CHECKING


print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Interface
    from el_analysis.models.physical.connector import Connector
    from el_analysis import Address, config, Location

from typing import Optional, Any, List
from el_analysis import logging

class Device:
    def __init__(self, name: str, parent: Optional[Any]=None, long_name: Optional[str] = None):
        """Initialize a Device with an address, name, and optional long name.
        @param address: The Address object representing the device's address.
        @param name: The name of the device. Example "A2"
        @param long_name: An optional long name for the device. Example "Main Power Supply"""
        self.name = name
        
        self.parent = parent
        if parent is not None:
            if hasattr(parent, "address"):
                self.address = parent.address.extend(product=name)
                # self.address: Address.union(parent.location_address, product=name) = parent.address.extend(product=name)
                # self.address = parent.address
            else:
                raise AttributeError("Parent object does not have an 'address' attribute.")
        else:
            self.address = Address(product=name)
            
        self.long_name = long_name
        self._interfaces: dict[str, Interface] = {}

        self.is_cable = False
        if self.name.startswith("W"):
            self.is_cable = True
            logging.debug(f"Device {self.name} is identified as a cable.")

    @property
    def interfaces(self) -> List[Interface]:
        """Returns a list of interfaces associated with this device."""
        return list(self._interfaces.values())
    
    @property
    def location(self) -> Optional[Location]:
        """Returns the location of the device, if available."""
        from el_analysis.core.location import Location
        if self.parent and isinstance(self.parent, Location):
            return self.parent
        return None

    def _make_interface(self, name, *args, **kwargs) -> Interface:
        from el_analysis.models import Interface
        return Interface(name, parent=self, *args, **kwargs)

    def add_interface(self, interface_name: str, connector: Optional[Connector] = None) -> Interface:
        """Add an interface to the device.
        @param interface_name: The name of the interface to add.
        @param connector: An optional Connector object to associate with the interface.
        @return: The Interface object that was added.
        Raises ValueError if the interface already exists and config.ErrorOnDuplicateInterface is True.
        """
        
        from el_analysis import config, logging

        if not interface_name:
            logging.error(f"Attempted to add an interface with an empty name to device {self.name}")
            raise ValueError("Interface name cannot be empty.")

        if interface_name in self._interfaces:
            interface_obj = self._interfaces[interface_name]
        else:
            interface_obj = self._make_interface(interface_name, connector=connector)

        self._interfaces[interface_name] = interface_obj
        logging.debug(f"Adding interface {interface_name} to device {self.name}")
        return interface_obj

    def get_interface(self, interface_name: str) -> Optional[Interface]:
        """Retrieve an interface by its name. Returns None if not found.
        @param interface_name: The name of the interface to retrieve.
        @return: The Interface object if found, otherwise None.
        """
        return self._interfaces.get(interface_name)

    def remove_interface(self, interface_name: str) -> bool:
        """Remove an interface from the device.
        @param interface_name: The name of the interface to remove.
        @return: True if the interface was removed successfully, False if it did not exist."""
        removed = False
        if interface_name in self._interfaces:
            logging.debug(f"Removing interface {interface_name} from device {self.name}")
            self._interfaces.pop(interface_name)  # Ensure the interface is closed before removal
            removed = True
        else:
            logging.error(f"Attempted to remove non-existent interface: {interface_name} from existing device {self.name}")
            if config.Interface.ErrorOnNonExistentInterface:
                raise KeyError(f"Interface '{interface_name}' not found.")
            
        return removed

    def list_interfaces(self) -> list[str]:
        return list(self._interfaces.keys())
    
    @property
    def interfaceCount(self):
        return len(self._interfaces.keys())
        
    def __repr__(self):
        return (f"Device(name={self.name!r}, address={self.address!r}, "
                f"long_name={self.long_name!r}, interfaces={list(self._interfaces.keys())})")
