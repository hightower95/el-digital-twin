
from dataclasses import dataclass, field
from enum import Enum

"""
 This file defines the SpecificationAspect class, which is used to represent aspects of a connector specification.

 For example the D38999 connector has a property called Material. The property values can be Zinc, Cadmium, or Aluminium.

"""

@dataclass
class PropertyValue:
    name: str = field(default="")
    short_name: str = field(default="")

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, PropertyValue):
            raise ValueError(f"Cannot compare PropertyValue with {type(value)}")
        return self.short_name == value.short_name


class ConnectorProperty(Enum):

    @classmethod
    def get_options(cls) -> list:
        """Returns a list of short names for the property values."""
        return [member.value for member in cls]

    @classmethod
    def get_property_value_from_short_name(cls, short_name: str) -> PropertyValue:
        """Returns the PropertyValue from the enum class by its short name."""
        for member in cls:
            if member.value.short_name == short_name:
                return member.value
        raise ValueError(f"Short name '{short_name}' not found in {cls.__name__}")