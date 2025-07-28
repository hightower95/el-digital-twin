# from ... import logging, config, Address
from __future__ import annotations
from typing import TYPE_CHECKING


print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Interface
    from el_analysis.connector_toolkit.connector import Connector
    from el_analysis import Address, config, Location

from typing import Optional, Any, List
from el_analysis import logging
from el_analysis.models.physical.addressable import Addressable
from tabulate import tabulate

class Device(Addressable):
    def __init__(self, name: str, parent: Optional[Any]=None, long_name: Optional[str] = None):
        """Initialize a Device with an address, name, and optional long name.
        @param address: The Address object representing the device's address.
        @param name: The name of the device. Example "A2"
        @param long_name: An optional long name for the device. Example "Main Power Supply"""
        
        self.parent = parent
        if parent is not None:
            if hasattr(parent, "address"):
                _address = parent.address.extend(product=name)
                # self.address: Address.union(parent.location_address, product=name) = parent.address.extend(product=name)
                # self.address = parent.address
            else:
                raise AttributeError("Parent object does not have an 'address' attribute.")
        else:
            _address = Address(product=name)
        super().__init__(address=_address, name=name)
            
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
    
    def search_by_address(self, address: Address, create_if_not_exists: bool = False) -> Optional[Addressable]:
        """
        Retrieves a device by its address.
        
        Args:
            address (str): The address of the device.
            create_if_not_exists (bool): Whether to create the device if it does not exist.
        
        Returns:
            Device: The device with the specified address.
        """
        logging.debug(f"Searching for interface by address: {address}, as_tuple: {address.as_tuple()}")
        
        if address.interface is None:
            logging.error(f"Address {address} does not contain an interface name, cannot find device")
            return None
        
        found_device = self.get_interface(address.interface)
        
        if create_if_not_exists and found_device is None:
            found_device = self.add_interface(address.interface)

        if found_device is not None and address.pin is not None:
            logging.debug(f"Address {address} contains a pin, searching for device by pin address: {address.pin_address}")
            found_device = found_device.search_by_address(address, create_if_not_exists=True)
        
        logging.debug(f"Found device: {found_device} for address: {address}, as_tuple: {address.as_tuple()}")

        return found_device

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

    def print_device_summary(self) -> None:
        """Return a formatted string summarizing the device and its interfaces."""
        
        summary_lines = [f"Device: {self.name} ({self.long_name or 'No description'})", 
                f"Address: {self.address}"]

        if self.interfaces:
            # Prepare data for the interface table as a list of dictionaries
            interface_data = []
            for interface in self.interfaces:
                # Create a dictionary with interface properties
                interface_info = {
                    "Interface": interface.address.address_string,
                    "Part Number": interface.part_number,
                    "Part Type": interface.part_code
                    # Add more key-value pairs as needed
                }
                interface_data.append(interface_info)

            # Extract headers from the first dictionary (assumes all dictionaries have the same keys)
            if interface_data:
                headers = list(interface_data[0].keys())
            
            # Create the table title
            table_title = f"\nDevice {self.name}, ({self.address}) has the following interfaces:"
            summary_lines.append(table_title)
            
            # Create a table with the interface data
            interface_table = tabulate(
                [list(iface.values()) for iface in interface_data],
                headers=headers, # type:ignore
                showindex="always",  # Show index for each interface
                tablefmt="grid"
            )
            summary_lines.append(interface_table)
        else:
            summary_lines.append("\nNo interfaces connected")

        print("\n".join(summary_lines))

