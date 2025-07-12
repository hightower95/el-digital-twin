

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from el_analysis.models.physical.device import Device
    from el_analysis.models.physical.interface import Interface
    from el_analysis.models.physical.pin import Pin
    from el_analysis.models.physical.net import Net
    from el_analysis.models.physical.connection import Connection
    from el_analysis.models.physical.addressable import Addressable
    from el_analysis.models.logical.signal import Signal
    from el_analysis.core.location import Location
    from el_analysis import Address
    from typing import List, Optional, Union

    
from el_analysis import config, logging



class Project:
    """
    Represents a project in the EL Analysis tool.
    
    Attributes:
        name (str): The name of the project.
    """

    def __init__(self, name: str, default_location: str = "C"):
        from el_analysis.core.location import Location
        self.name = name
        self.locations: List[Location] = []  # List of location names associated with the project
        self.default_location = Location(default_location,default_location)
        self.locations.append(self.default_location)    
        self._signals: List[Signal] = []  # List of signals in the project

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
        from el_analysis.core.location import Location
        for location in self.locations:
            if location.prefix == location_name:
                return location
            
        # If we reach here, the location does not exist
        if create_if_not_exists:
            logging.debug(f"Creating new location '{location_name}' in project '{self.name}'")
            new_location = Location(location_name)
            self.locations.append(new_location)
            return new_location
        raise ValueError(f"Location {location_name} not found in project {self.name}")

    def search_by_address(self, address: Address, create_if_not_exists: bool = False) -> Optional[Addressable]:
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
        found_device = None
        location_name = address.location if hasattr(address, 'location') else None
        if location_name is not None:
            location = self.get_location_by_name(location_name, create_if_not_exists=create_if_not_exists)
        else:
            location = self.default_location

        if address.product is not None:
            found_device = location.search_by_address(address, create_if_not_exists=create_if_not_exists)

        # if found_device is not None and address.interface is not None:
        #     found_device = found_device.search_by_address(address, create_if_not_exists=create_if_not_exists)


        if found_device is None:
            logging.debug(f"Device with address {address} not found in project {self.name} at location {location_name}")
        return found_device
    
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
    
    @property
    def interfaces(self) -> List[Interface]:
        """
        Returns a list of all interfaces in the project.
        
        Returns:
            List[Interface]: A list of interfaces in the project.
        """
        interfaces = []
        for device in self.devices:
            interfaces.extend(device.interfaces)
        return interfaces
    
    @property
    def signals(self) -> List[Signal]:
        """
        Returns a list of all signals in the project.
        
        Returns:
            List[Signal]: A list of signals in the project.
        """
        signals = []
        for device in self.devices:
            for interface in device.interfaces:
                signals.extend(interface.signals)
        return signals

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

    def create_net(self, source_pin: Pin, destination_pin: Pin, signal_name: Optional[str] = None) -> Optional[Net]:
        """
        Creates a net connection between two devices in the project.
        
        Args:
            source (Device): The source device for the net connection.
            destination (Device): The destination device for the net connection.
            signal_name (str, optional): The name of the signal for the net connection. Defaults to None.
        
        Returns:
            Device: The device that was connected, or None if the connection could not be made.
        """
        from el_analysis.models.physical.net import Net

        if source_pin is None or destination_pin is None:
            logging.error("Source or destination pin is None.")
            return None
        
        # if we dont have a destination pin, we can look at source_pin.interface.connected_to 

        net = Net(source_pin, destination_pin, signal=None)
        logging.info(f"Created net from {source_pin.name} to {destination_pin.name} with signal '{signal_name}'")

        return net

    def get_signal(self, signal_name: str, create_if_not_exists: bool = False) -> Optional[Signal]:
        """
        Retrieves a signal by its name.
        
        Args:
            signal_name (str): The name of the signal to retrieve.
        
        Returns:
            Signal: The signal with the specified name, or None if not found.
        """
        for signal in self._signals:
            if signal.name == signal_name:
                return signal
            
        if create_if_not_exists:
            from el_analysis.models.logical.signal import Signal
            new_signal = Signal.from_signal_name(signal_name)
            if new_signal is None:
                logging.error(f"Failed to create signal '{signal_name}' in project '{self.name}'")
                return None
            self._signals.append(new_signal)
            logging.debug(f"Created new signal '{signal_name}' in project '{self.name}'")
            return new_signal
        logging.debug(f"Signal {signal_name} not found in project {self.name}")
        return None
    
    def create_connection(self, source: Address, destination: Address, signal_name: Optional[str] = None) -> Optional[Connection]:
        """
        Creates a connection between two devices or interfaces in the project.
        
        Args:
            source (Address): The source address of the connection.
            destination (Address): The destination address of the connection.
            signal_name (str, optional): The name of the signal for the connection. Defaults to None.
        
        Returns:
            Device or Interface: The device or interface that was connected, or None if the connection could not be made.
        """
        from el_analysis.models.physical.pin import Pin
        from el_analysis.models.physical.interface import Interface
        from el_analysis.core.address import Address
        
        source_device = self.search_by_address(source, create_if_not_exists=True)
        destination_device = self.search_by_address(destination, create_if_not_exists=True)
        return_value = None

        signal = self.get_signal(signal_name, create_if_not_exists=True) if signal_name else None

        if source.same_location(destination) is False:
            logging.warning(f"Creating a connection between {source} and {destination} - they are not in the same location. This may not be intended, but is allowed")

        if isinstance(source_device, Pin) and isinstance(destination_device, Pin):        
            source_pin = source_device
            destination_pin = destination_device

            logging.info(f"Connected pins {source} to {destination} with signal '{signal.name if signal else None}'")
            
            net = Pin.create_net(source_pin, destination_pin, signal=signal)

            if net is None:
                logging.error(f"Failed to create net between {source} and {destination}.")
                raise ValueError(f"Failed to create net between {source} and {destination}.")
            
            return_value = net

            # not net.is_internal means between two devices, e.g. a Cable (CW100) to a Device (A2)
            # SO we mean, if the net is not internal, we want to register the connection between the interfaces of the devices 
            if not net.is_internal:
                if source_pin.interface is None or destination_pin.interface is None:
                    logging.error(f"Cannot connect pins {source} and {destination} - one or both pins do not have an interface.")
                    raise ValueError(f"Cannot connect pins {source} and {destination} - one or both pins do not have an interface.")
                coupling = Interface.connect_interfaces(source_pin.interface, destination_pin.interface)

        elif isinstance(source_device, Interface) and isinstance(destination_device, Interface):
            # If we learn that there are two connecting interfaces, we have a small dilemma
            #    Do we go through every pin on both interfaces and creates nets for them?
            #    No - because the logic in this library is that if there is a connection between two pins of different interfaces, then there must be a coupling

            if signal_name is not None:
                raise ValueError("Signal name should not be provided for interface connections. Use pin connections instead.")

            logging.info(f"Connected interfaces {source} to {destination}")
            if Address.product_match(source, destination):
                logging.warning(f"Connecting interfaces {source} and {destination} from the same product. This may not be intended.")

            return_value = Interface.connect_interfaces(source_device, destination_device)
        else:
            logging.error(f"Cannot connect {source} to {destination}: incompatible types.")
            raise ValueError(f"Cannot connect {source} (type {type(source_device).__name__}) to {destination} (type {type(destination_device).__name__}): incompatible types.")

        return return_value



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
    
    def create_cable_summary(self):
        from el_analysis.utils.summarize_project_cables import get_cable_summary
        return get_cable_summary(self)
    
    def create_device_summary(self):
        from el_analysis.utils.summarize_project_devices import get_device_summary
        return get_device_summary(self)
    
    def create_interface_summary(self):
        from el_analysis.utils.summarise_project_connectors import get_connector_summary
        return get_connector_summary(self)
    
    def create_connection_summary(self):
        from el_analysis.utils.summarize_project_connections import get_connection_summary
        return get_connection_summary(self)
    
    def create_signal_summary(self):
        from el_analysis.utils.summarize_project_signals import get_signal_summary
        return get_signal_summary(self)