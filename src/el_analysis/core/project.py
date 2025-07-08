

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from el_analysis.models.physical.device import Device
    from el_analysis.core.location import Location
    from el_analysis import Address
    from typing import List, Optional

    
from el_analysis import config, logging



class Project:
    """
    Represents a project in the EL Analysis tool.
    
    Attributes:
        name (str): The name of the project.
    """

    def __init__(self, name: str, default_location: str = ""):
        from el_analysis.core.location import Location
        self.name = name
        self.locations: List[Location] = []  # List of location names associated with the project
        self.default_location = Location(default_location,default_location)
        self.locations.append(self.default_location)    

    def get_location_by_name(self, location_name: str, create_if_not_exists: bool = False) -> Location:
        """
        Retrieves a location by its name.
        
        Args:
            location_name (str): The name of the location to retrieve.
        
        Returns:
            Location: The location with the specified name.
        
        Raises:
            ValueError: If no location with the specified name exists in the project.
        """
        for location in self.locations:
            if location.prefix == location_name:
                return location
            
        if create_if_not_exists:
            new_location = Location(location_name)
            self.locations.append(new_location)
            return new_location
        raise ValueError(f"Location {location_name} not found in project {self.name}")

    def get_device_by_address(self, address: Address, create_if_not_exists: bool = False) -> Optional[Device]:
        """
        Retrieves a device by its address.
        
        Args:
            address (str): The address of the device to retrieve.
            create_if_not_exists (bool): If True, creates a new device if it does not exist.
        
        Returns:
            Device: The device with the specified address.
        
        Raises:
            ValueError: If no device with the specified address exists and create_if_not_exists is False.
        """
        # 1 find location
        location_name = address.location if hasattr(address, 'location') else None
        if location_name is not None:
            location = self.get_location_by_name(location_name, create_if_not_exists=create_if_not_exists)
        else:
            location = self.default_location

        device = location.get_device_by_address(address, create_if_not_exists=create_if_not_exists)

        if device is not None:
            return device
        
        logging.warning(f"Device with address {address} not found in project {self.name} at location {location_name}")
        return None
    
    @property
    def devices(self) -> List[Device]:
        """
        Returns a list of all devices in the project.
        
        Returns:
            List[Device]: A list of devices in the project.
        """
        devices = []
        for location in self.locations:
            devices.extend(location.devices)
        return devices

    def new_device(self, name: str, location: Optional[Location] = None) -> Device:
        """
        Creates a new device in the project.
        
        Args:
            name (str): The name of the device to create.
            location (Location, optional): The location where the device should be created. Defaults to None.
        
        Returns:
            Device: The newly created device.
        """
        from el_analysis.models.physical.device import Device
        
        if location is None:
            location = self.default_location
        
        new_device = location.new_device(name)        
        return new_device
    
    def summarize(self):
        """
        Prints a summary of the project, including the number of devices and their locations.
        """
        print(f"Project Summary for {self.name}:")
        print(f"Total Devices: {len(self.devices)}")

        for loc in self.locations:
            print(f"Location: {loc.name}, Devices: {len(loc.devices)}")
            for device in loc.devices:
                interfaces = device.interfaces
                print(f"\t{device.name} : {','.join([i.name for i in interfaces])}")

    def __repr__(self):
        # Count devices per location
        location_counts = {}
        for device in self.devices:
            loc = getattr(device, "location", None)
            if loc:
                location_counts[loc] = location_counts.get(loc, 0) + 1
            else:
                location_counts["<no location>"] = location_counts.get("<no location>", 0) + 1

        location_str = ", ".join(f"{loc}: {count}" for loc, count in location_counts.items())
        return f"Project(name={self.name}, devices={len(self.devices)}, device_counts_by_location={{ {location_str} }})"