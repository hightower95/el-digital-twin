
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from el_analysis.models.physical.device import Device
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

    def get_device_by_address(self, address: Address, create_if_not_exists: bool = False) -> Optional[Device]:
        """
        Retrieves a device by its address.
        
        Args:
            address (str): The address of the device.
            create_if_not_exists (bool): Whether to create the device if it does not exist.
        
        Returns:
            Device: The device with the specified address.
        """

        if address.product in self._devices:
            return self._devices[address.product]
        
        if create_if_not_exists:
            device_name = address.product if address.product is not None else None
            if device_name is None:
                logging.error(f"Address {address} does not contain a product name, cannot create device")
                raise ValueError("Address does not contain a product name")

            new_device = self.new_device(device_name)
            return new_device

        return None
    
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