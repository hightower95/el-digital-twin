from dataclasses import dataclass, field
from enum import Enum as enum

@dataclass
class ConnectorComponent:
    name: str = field(default="")
    short_name: str = field(default="")

def extract_options_from_enum(enum_class):
    """Extracts the short names from an enum class."""
    return [member.value.short_name for member in enum_class]

def get_component_by_short_name(enum_class, short_name: str) -> ConnectorComponent:
    """Returns the ConnectorComponent from the enum class by its short name."""
    for member in enum_class:
        if member.value.short_name == short_name:
            return member.value
    raise ValueError(f"Short name '{short_name}' not found in {enum_class.__name__}")

class Materials(enum):
    ZINC = ConnectorComponent("Zinc", "Z")
    CADMIUM = ConnectorComponent("Cadmium", "W")
    ALUMINIUM = ConnectorComponent("Aluminium", "A")
MATERIAL_OPTIONS = extract_options_from_enum(Materials)

class Sizes(enum):
    SMALL = ConnectorComponent("Small", "S")
    MEDIUM = ConnectorComponent("Medium", "M")
    LARGE = ConnectorComponent("Large", "L")
SIZE_OPTIONS = extract_options_from_enum(Sizes)

class Variants(enum):
    STANDARD = ConnectorComponent("Standard", "1")
    HIGH_CURRENT = ConnectorComponent("High Current", "2")
    LOW_PROFILE = ConnectorComponent("Low Profile", "3")
VARIANT_OPTIONS = extract_options_from_enum(Variants)

class Genders(enum):
    MALE = ConnectorComponent("Male", "M")
    FEMALE = ConnectorComponent("Female", "F")
GENDER_OPTIONS = extract_options_from_enum(Genders)

@dataclass
class DBConnectorPart:
    variant: ConnectorComponent
    material: ConnectorComponent
    size: ConnectorComponent
    gender: ConnectorComponent

    def as_string(self) -> str:
        """Returns a string representation of the connector part."""
        return f"{self.variant.short_name}-{self.material.short_name}-{self.size.short_name}-{self.gender.short_name}"
    
    def minified_part_type(self) -> str:
        """Returns a minified part type string."""
        return f"{self.variant.short_name}-_-{self.size.short_name}-{self.gender.short_name}"
    
    def can_connect_to(self, other: 'DBConnectorPart') -> bool:
        """Checks if this part can connect to another part."""
        variant_match = self.variant == other.variant
        size_match = self.size == other.size
        if self.gender == Genders.MALE.value and other.gender == Genders.FEMALE.value:
            gender_match = True
        elif self.gender == Genders.FEMALE.value and other.gender == Genders.MALE.value:
            gender_match = True
        else:
            gender_match = False

        return variant_match and size_match and gender_match

    @classmethod
    def from_part_code_string(cls, part_type: str) -> 'DBConnectorPart':
        """Initializes the connector part from a string representation."""
        parts = part_type.split('-')
        # print(f"Parsing part type: {part_type}, got parts: {parts}")
        if len(parts) != 4:
            raise ValueError(f"Part type must be in the format 'Variant-Material-Size-Gender' - got {part_type}")
        
        variant = get_component_by_short_name(Variants, parts[0])
        material = get_component_by_short_name(Materials, parts[1])
        size = get_component_by_short_name(Sizes, parts[2])
        gender = get_component_by_short_name(Genders, parts[3])

        return cls(variant=variant, material=material, size=size, gender=gender)
    
    def get_opposite_part(self) -> 'DBConnectorPart':
        """Returns the opposite part type for this connector."""
        opposite_gender = Genders.FEMALE.value if self.gender == Genders.MALE.value else Genders.MALE.value
        return DBConnectorPart(variant=self.variant, material=self.material, size=self.size, gender=opposite_gender)

    def get_compatible_parts(self) -> list['DBConnectorPart']:
        """Returns a list of part types that are compatible with this connector."""
        compatible_parts = []
        opposite_gender = self.gender
        if self.gender == Genders.MALE.value:
            opposite_gender = Genders.FEMALE.value
        elif self.gender == Genders.FEMALE.value:
            opposite_gender = Genders.MALE.value

        else:
            raise ValueError(f"Unsupported gender: {self.gender}")

        for material in Materials:
            part = DBConnectorPart(variant=self.variant, material=material.value, size=self.size, gender=opposite_gender)
            compatible_parts.append(part)
        return compatible_parts
    
    def get_adjacent_parts(self) -> list['DBConnectorPart']:
        """Returns a list of adjacent parts that are compatible with this connector."""
        adjacent_parts = []
        for material in Materials:
            part = DBConnectorPart(variant=self.variant, material=material.value, size=self.size, gender=self.gender)
            adjacent_parts.append(part)
        return adjacent_parts


@dataclass
class DBConnector:
    part_code: str
    part_number: str = field(default="")

    # @property
    # def part_type(self) -> str:
    #     """Returns the part type as a string."""
    #     return self.part.as_string()
    
    # @property
    # def minified_part_type(self) -> str:
    #     """Returns the minified part type."""
    #     return self.part.minified_part_type()
    
    # def can_connect_to(self, other: 'Connector') -> bool:
    #     """Checks if this connector can connect to another connector."""
    #     return self.part.can_connect_to(other.part)
    
    # def get_compatible_parts(self) -> list[DBConnectorPart]:
    #     """Returns a list of part types that are compatible with this connector."""

    #     return self.part.get_compatible_parts()
    
    # def get_adjacent_parts(self) -> list[DBConnectorPart]:
    #     """Returns a list of adjacent parts that are compatible with this connector."""
    #     return self.part.get_adjacent_parts()


if __name__ == "__main__":
    # Example usage
    part = DBConnectorPart(variant=Variants.STANDARD.value, material=Materials.ZINC.value, size=Sizes.SMALL.value, gender=Genders.MALE.value)
    print(f"Created part: {part.as_string()}")
    opposite_parts = part.get_compatible_parts()
    print(f"Compatible parts for {part.as_string()}:")
    for compatible_part in opposite_parts:
        print(compatible_part.as_string())