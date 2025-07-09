from __future__ import annotations
from typing import TYPE_CHECKING

print(f"Loaded {__name__} module successfully.")
if TYPE_CHECKING:
    from el_analysis.models import Device, Pin
    from el_analysis import Address

print(f"Loaded {__name__} module successfully.")
from .connector import Connector
from typing import Optional, Any, List
from el_analysis import logging, config




class Interface:
    """Represents an interface for parts or connectors in the BW Analysis module."""
    
    def __init__(self, name: str, parent: Optional[Any]=None, connector: Optional[Connector]=None):
        
        self._validation(name)
        self.name = name
        self.parent = parent
        if parent is not None:
            if hasattr(parent, "address"):
                self.address = parent.address.extend(interface=name)
            else:
                raise AttributeError("Parent object does not have an 'address' attribute.")
        else:
            self.address = Address(interface=name)
       
        self.connector = connector 
        self._pins: dict[str, Pin] = {}  #TODO: Import pins from connector part
        self.connected_to: Optional[Interface] = None  # Reference to another interface this one is connected to
    
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
    def part_type(self) -> Optional[str]:
        return self.connector.part_type if self.connector else None
    
    @property
    def pins(self) -> List[Pin]:
        """Returns a list of pins associated with this interface."""
        return list(self._pins.values())    

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
        logging.debug(f"Adding Pin {pin_name} to device {self.name}")
        return pin_obj

   
    
    def get_minified_part_type(self, include_keying: bool = False) -> Optional[str]:
        return self.connector.get_minified_part_type(include_keying) if self.connector else None
    
    @staticmethod
    def is_standard_name(name: str) -> bool:
        """Check if the interface name is a standard name.
        It is a standard name if it starts with 'X' or 'J' and is followed by digits.
        @param name: The name of the interface.
        @return: True if the name is standard, False otherwise.
        """
        return name.startswith("X") or name.startswith("J") or name[1:].isdigit()
    
    def __repr__(self):
        if self.connector:
            return f"Interface(name={self.name}, parent={self.parent}, address={self.address}, connector={self.connector})"
        else:
            # If no connector is set, we still want to show the basic info
            return f"Interface(name={self.name}, parent={self.parent}, address={self.address})"