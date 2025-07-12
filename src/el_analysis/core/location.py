
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from el_analysis.models.physical.device import Device
    from el_analysis.models.physical.addressable import Addressable
    from el_analysis import Address
    from typing import List, Optional , Dict


from el_analysis import config, logging


class Location:
    """
    A project can have multiple locations
    
    Attributes:
        name (str): The name of the project.
        prefix (str): The prefix for the location.
    """

    def __init__(self, name: str, prefix: str = ""):
        from el_analysis import Address

        self.name: str = name
        self.prefix: str = prefix
        self._devices: Dict[str, Device] = {}  # Dictionary of devices in this location, keyed by device name
        self.address: Address = Address(location=prefix)

    @property
    def devices(self) -> List[Device]:
        """
        Returns a list of devices in this location.
        
        Returns:
            List[Device]: A list of devices in this location.
        """
        return list(self._devices.values())

    def search_by_address(self, address: Address, create_if_not_exists: bool = False) -> Optional[Addressable]:
        """
        Retrieves a device by its address.
        
        Args:
            address (str): The address of the device.
            create_if_not_exists (bool): Whether to create the device if it does not exist.
        
        Returns:
            Device: The device with the specified address.
        """
        from el_analysis.models.physical.device import Device
        from el_analysis.models.physical.addressable import Addressable
        
        # Todo add or create stack
        logging.debug(f"Searching for device by address: {address}, as_tuple: {address.as_tuple()}")

        if address.product is None:
            logging.error(f"Address {address} does not contain a product name, cannot find device")
            return None
        
        found_device = self._devices.get(address.product, None)
        
        if create_if_not_exists and found_device is None:
            found_device = self.new_device(address.product)
        
        logging.debug(f"Found device: {found_device} for address: {address}, as_tuple: {address.as_tuple()}")
        if found_device is not None and address.interface is not None:
            logging.debug(f"Address {address} contains an interface, searching for device by interface address: {address.interface_address}")
            found_device = found_device.search_by_address(address, create_if_not_exists=True)

        logging.debug(f"Found device: {found_device} for address: {address}, as_tuple: {address.as_tuple()}")

        return found_device
    
    def new_device(self, name: str) -> Device:
        """
        Creates a new device in this location.
        
        Args:
            name (str): The name of the device to create.
        
        Returns:
            Device: The newly created device.
        """
        from el_analysis.models.physical.device import Device

        if name in self._devices:
            logging.warning(f"Failed to create new device {name} in location {self.name} - already exists. Returning existing device")
            return self._devices[name]

        new_device = Device(name=name, parent=self)
        self._devices[name] = new_device
        logging.debug(f"Created new device {new_device} in location {self.name}")
        return new_device

    def __repr__(self):
        return f"Location(name={self.name}, devices={len(self._devices)})"