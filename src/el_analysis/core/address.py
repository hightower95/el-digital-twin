from typing import Optional
from dataclasses import dataclass
from el_analysis import config
import re

AddressConfig = config.Address
LoggingEnabled = AddressConfig.EnableLogging

@dataclass(frozen=True)
class Address:
    location: Optional[str] = None
    product: Optional[str] = None
    interface: Optional[str] = None
    pin: Optional[str] = None

    def __post_init__(self):
        """Post-initialization to ensure all parts are strings and validate dependencies."""
        object.__setattr__(self, 'location', str(self.location) if self.location else None)
        object.__setattr__(self, 'product', str(self.product) if self.product else None)
        object.__setattr__(self, 'interface', str(self.interface) if self.interface else None)
        object.__setattr__(self, 'pin', str(self.pin) if self.pin else None)

        if self.pin and not (self.interface and self.product):
            raise ValueError("Pin Address cannot be set when Interface and Product are not set")
        if self.interface and not self.product:
            raise ValueError("Interface Address cannot be set when Product is not set")

    def as_tuple(self, length:Optional[int]=None) -> tuple:
        """Return the address as a tuple."""
        if length and length > 3: 
            raise ValueError("Address 'as tuple' does not accept length greater than 3")

        result = (self.location, self.product, self.interface, self.pin)
        if length is not None:
            result = result[0:length]

            def pad_to_4(t: tuple) -> tuple:
                return t + (None,) * (4 - len(t))

            result = pad_to_4(result)

        return result
    
    #  ==== Match Methods ====
    # Match methods to compare different parts of the address
    @staticmethod
    def location_match(first: 'Address', second: 'Address') -> bool:
        """Check if the location part of two addresses matches."""
        return first.location == second.location if first and second else False

    @staticmethod
    def product_match(first: 'Address', second: 'Address') -> bool:
        """Check if the product part of two addresses matches."""
        return Address.location_match(first, second) and first.product == second.product if first and second else False
    
    @staticmethod
    def interface_match(first: 'Address', second: 'Address') -> bool:
        """Check if the interface part of two addresses matches."""
        return Address.product_match(first, second) and first.interface == second.interface if first and second else False
    
    @staticmethod
    def pin_match(first: 'Address', second: 'Address') -> bool:
        """Check if the pin part of two addresses matches."""
        return Address.interface_match(first, second) and first.pin == second.pin if first and second else False
    
    # ==== Address Subsets ====
    # Methods to return subsets of the address
    @property
    def location_address_string(self) -> str:
        """Return the location part of the address."""
        return f"{AddressConfig.PrefixLocation}{self.location}" if AddressConfig.PrefixLocation and self.location else self.location or ""
    
    @property
    def product_address_string(self) -> str:
        """Return the product part of the address."""
        return f"{self.location_address_string}{AddressConfig.PrefixProduct}{self.product}" if AddressConfig.PrefixProduct and self.product else self.product or ""
    
    @property
    def interface_address_string(self) -> str:
        """Return the interface part of the address."""
        return f"{self.product_address_string}{AddressConfig.PrefixInterface}{self.interface}" if AddressConfig.PrefixInterface and self.interface else self.interface or ""

    @property
    def pin_address_string(self) -> str:
        """Return the pin part of the address."""
        return f"{self.interface_address_string}{AddressConfig.PrefixPin}{self.pin}" if AddressConfig.PrefixPin and self.pin else self.pin or ""


    @property
    def address_string(self) -> str:
        """Return the full address as a string."""
        if self.pin is not None:
            return self.pin_address_string
        if self.interface is not None:
            return self.interface_address_string
        if self.product is not None:
            return self.product_address_string
        if self.location is not None:
            return self.location_address_string
        raise ValueError("Address is empty, cannot return a valid address string")
    
    @property
    def location_address(self) -> 'Address':

        return Address.from_tuple(self.as_tuple(length=1))
    
    @property
    def product_address(self) -> 'Address':
        return Address.from_tuple(self.as_tuple(length=2))
    
    @property
    def interface_address(self) -> 'Address':
        return Address.from_tuple(self.as_tuple(length=3))
    
    @property
    def pin_address(self) -> 'Address':
        return self
    
    # ====  Check What Address Represents ====
    @property
    def is_location(self) -> bool:
        """Check if the address represents a location."""
        return self.location is not None and self.product is None and self.interface is None and self.pin is None
    @property
    def is_product(self) -> bool:
        """Check if the address represents a product."""
        return self.location is not None and self.product is not None and self.interface is None and self.pin is None
    @property
    def is_interface(self) -> bool:
        """Check if the address represents an interface."""
        return self.product is not None and self.interface is not None and self.pin is None
    
    @property
    def is_pin(self) -> bool:
        """Check if the address represents a pin."""
        return self.product is not None and self.interface is not None and self.pin is not None

    ### Override Inbuilt Methods ###
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Address):
            raise TypeError(f"Cannot compare Address with {type(value)}")
        
        return self.as_tuple() == value.as_tuple()

    def __repr__(self) -> str:
        return self.address_string
    

    @classmethod
    def from_string(cls, address_str: str) -> 'Address':
        """Create an Address instance from a string."""
        # Remove all configured prefixes from the string
        # prefixes = [
        #     getattr(AddressConfig, "PrefixLocation", ""),
        #     getattr(AddressConfig, "PrefixProduct", ""),
        #     getattr(AddressConfig, "PrefixInterface", ""),
        #     getattr(AddressConfig, "PrefixPin", ""),
        # ]
        # # Escape and join non-empty prefixes for regex
        # prefix_pattern = "|".join(re.escape(p) for p in prefixes if p)
        # cleaned = re.sub(prefix_pattern, "", address_str)

        # Split by any punctuation: + . :
        parts = [p for p in re.split(r"[+.:]", address_str) if p]
        # Pad to 4 elements
        while len(parts) < 4:
            parts.append(None)
        return cls(location=parts[0], product=parts[1], interface=parts[2], pin=parts[3])
        parts = address_str.split('.')
        if len(parts) != 4:
            raise ValueError("Address string must contain exactly four parts: location, product, interface, pin")
        
        return cls(location=parts[0], product=parts[1], interface=parts[2], pin=parts[3])
    
    @classmethod
    def from_tuple(cls, address_tuple: tuple) -> 'Address':
        """Create an Address instance from a tuple."""
        if len(address_tuple) != 4:
            raise ValueError("Address tuple must contain exactly four elements: location, product, interface, pin")
        
        return cls(location=address_tuple[0], product=address_tuple[1], interface=address_tuple[2], pin=address_tuple[3])

    def extend(self, product=None, interface=None, pin=None) -> 'Address':
        #TODO: handle issue where we have interface None, but pin not None
        return Address(
            location=self.location,
            product=product if product is not None else self.product,
            interface=interface if interface is not None else self.interface,
            pin=pin if pin is not None else self.pin
        )
    
    @staticmethod
    def union(first:'Address', second:'Address') -> 'Address':
        """Returns a new address that is the union of the first and second.
        """
        def pick(name: str, a: Optional[str], b: Optional[str]) -> Optional[str]:
            if a == b:
                return a
            if a is None:
                return b
            if b is None:
                return a
            raise ValueError(f"Cannot union field '{name}': {a!r} vs {b!r}")

        return Address(
            location=pick("location", first.location, second.location),
            product=pick("product", first.product, second.product),
            interface=pick("interface", first.interface, second.interface),
            pin=pick("pin", first.pin, second.pin),
        )

if __name__ == "__main__":
    # Example usage
    addr1 = Address(location="C", product="A2", interface="X1", pin="13")
    addr2 = Address(location="C", product="A2", interface="X1", pin="14")
    addr3 = Address(location="C", product="A2", interface="X1", pin="15")
    addr4 = Address(location="C", product="A2", interface="X1", pin="16")
    
    print(addr1)  # Output: Pin1
    print(addr2)  # Output: Pin2
    print(addr1 == addr2)  # Output: False
    print(addr1.is_pin)  # Output: True
    print(addr1.product)  # Output: True
    print(addr1.as_tuple())  # Output: ('Location1', 'Product1', 'Interface1', 'Pin1')

    # logger.info(f"Address 1: {addr1}")
    # logger.debug(f"Address 1: {addr1}")
    # logger.warning(f"Address 3: {addr3}")
    # logger.error(f"Address 2: {addr2}")