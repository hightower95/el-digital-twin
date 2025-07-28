
from el_analysis.connector_toolkit.specification import Specification
from el_analysis.connector_toolkit.property import PropertyValue, ConnectorProperty
from typing import Dict, Optional


"""CustomSpecification is a specification for a custom connector type.

We want to be able to define a custom connector type that can be used in the toolkit. - maybe a D38999 Mark 5?

A specification is a set of properties that define a connector type. E.g. D38999 is a specification, also VG95234

In theory this should be handled by the ConnectorToolkit library, but this demonstrates how to do it if needed

The specification is to be used in conjuction with the connector database - see connector_database.py for an example of how to use it.

"""

class CustomSpecification(Specification):
    SPECIFICATION_NAME = "CustomSpecification"

    class Variants(ConnectorProperty):
        STANDARD = PropertyValue("Standard", "1")
        HIGH_CURRENT = PropertyValue("High Current", "2")
        LOW_PROFILE = PropertyValue("Low Profile", "3")
    VARIANTS = Variants

    class Material(ConnectorProperty):
        ZINC = PropertyValue("Zinc", "Z")
        CADMIUM = PropertyValue("Cadmium", "W")
        ALUMINIUM = PropertyValue("Aluminium", "A")

    class Sizes(ConnectorProperty):
        SMALL = PropertyValue("Small", "S")
        MEDIUM = PropertyValue("Medium", "M")
        LARGE = PropertyValue("Large", "L")

    class Genders(ConnectorProperty):
        MALE = PropertyValue("Male", "M")
        FEMALE = PropertyValue("Female", "F")
    GENDERS = Genders

    def __init__(self, 
                 variant: PropertyValue, 
                 material: PropertyValue,
                 size: PropertyValue,
                 gender: PropertyValue):
        super().__init__(CustomSpecification.SPECIFICATION_NAME)
        self.variant: PropertyValue = variant
        self.material: PropertyValue = material
        self.size: PropertyValue = size
        self.gender: PropertyValue = gender

    @property
    def aspects(self) -> Dict[str, type[ConnectorProperty]]:
        """Returns the aspects of the specification."""
        return {
            'variant': CustomSpecification.Variants,
            'material': CustomSpecification.Material,
            'size': CustomSpecification.Sizes,
            'gender': CustomSpecification.Genders
        }
    
    @property
    def values(self) -> Dict[str, PropertyValue]:
        """Returns the values of the specification aspects."""
        return {
            'variant': self.variant,
            'material': self.material,
            'size': self.size,
            'gender': self.gender
        }

    @staticmethod
    def can_parse_part_code(part_code: str) -> bool:
        """Checks if the part code can be parsed by this specification."""
        parts = part_code.split('-')
        # todo: check all parts are valid 

        return len(parts) == 4
    
    
    def get_part_code(self) -> str:
        """Returns a string representation of the connector part."""
        return f"{self.variant.short_name}-{self.material.short_name}-{self.size.short_name}-{self.gender.short_name}"
        

    def get_minified_part_code(self, minify_keying: bool = False) -> str:
        """Returns a minified part type string."""
        return f"{self.variant.short_name}-_-{self.size.short_name}-{self.gender.short_name}"
        
    
    def can_connect_to(self, other: Specification) -> bool:
        """
        Checks if this specification can connect to another specification.
        This should be implemented in subclasses to define specific connection logic.
        """
        """Checks if this part can connect to another part."""
        if not isinstance(other, CustomSpecification):
            return False

        variant_match = self.variant == other.variant
        size_match = self.size == other.size

        if self.gender == self.GENDERS.MALE.value and other.gender == self.GENDERS.FEMALE.value:
            gender_match = True
        elif self.gender == self.GENDERS.FEMALE.value and other.gender == self.GENDERS.MALE.value:
            gender_match = True
        else:
            gender_match = False

        return variant_match and size_match and gender_match
    
    @classmethod
    def from_part_code_string(cls, part_code: str) -> 'CustomSpecification':
        """Initializes the connector part from a string representation."""
        parts = part_code.split('-')
        # print(f"Parsing part type: {part_type}, got parts: {parts}")
        if len(parts) != 4:
            raise ValueError(f"Part type must be in the format 'Variant-Material-Size-Gender' - got {part_code}")
        
        variant = CustomSpecification.Variants.get_property_value_from_short_name(parts[0])
        material = CustomSpecification.Material.get_property_value_from_short_name(parts[1])
        size = CustomSpecification.Sizes.get_property_value_from_short_name(parts[2])
        gender = CustomSpecification.Genders.get_property_value_from_short_name(parts[3])

        return cls(variant=variant, material=material, size=size, gender=gender)
    
    def get_opposite(self) -> 'CustomSpecification':
        opposite_gender = CustomSpecification.Genders.FEMALE.value if self.gender == CustomSpecification.Genders.MALE.value else CustomSpecification.Genders.MALE.value
        return CustomSpecification(variant=self.variant, material=self.material, size=self.size, gender=opposite_gender)

    def get_compatible(self) -> list[Specification]:
        """Returns a list of part types that are compatible with this connector."""
        compatible_parts = []
        opposite_gender = self.gender
        if self.gender == CustomSpecification.Genders.MALE.value:
            opposite_gender = CustomSpecification.Genders.FEMALE.value
        elif self.gender == CustomSpecification.Genders.FEMALE.value:
            opposite_gender = CustomSpecification.Genders.MALE.value

        else:
            raise ValueError(f"Unsupported gender: {self.gender}")

        for material in CustomSpecification.Material:
            part = CustomSpecification(variant=self.variant, material=material.value, size=self.size, gender=opposite_gender)
            compatible_parts.append(part)
        return compatible_parts
    
    def get_adjacent(self) -> list[Specification]:
        """Returns a list of adjacent parts that are compatible with this connector."""
        adjacent_parts = []
        for material in CustomSpecification.Material:
            part = CustomSpecification(variant=self.variant, material=material.value, size=self.size, gender=self.gender)
            adjacent_parts.append(part)
        return adjacent_parts

if __name__ == "__main__":
    # Example usage
    print("")
    print("Lets use the CustomSpecification class to create a custom connector specification (component).")
    spec = CustomSpecification.from_part_code_string("1-W-S-F")
    print("Now thats done, lets looking at the values extracted from part code '1-W-S-F':")

    # database.add_handler(CustomSpecification)
    print("Can parse part code:", CustomSpecification.can_parse_part_code("1-W-S-F"))
    print("Connector Type:", spec.connector_type)
    print("Connector Family:", spec.connector_family)
    print("Part Code:", spec.get_part_code())
    print("Minified Part Code:", spec.get_minified_part_code())
    
    print("")
    print("Within our specification we embed all properties allowed by our made up standard, now we can look at these")
    for aspect_name, aspect in spec.aspects.items():
        print(f"Property: {aspect_name}, Options: {aspect.get_options()}")

    print("")
    print("We can also read the values of the properties out to a dictionary")
    print(spec.values)

    mating_spec = CustomSpecification.from_part_code_string("1-W-S-M")

    print("Can connect to mating part:", spec.can_connect_to(mating_spec))
    # Output: {'material': <PropertyValue: Zinc, Z>}
    # Output: {'material': <PropertyValue: Zinc, Z>}

    print("Lets check equality of two specifications:")
    spec1 = CustomSpecification.from_part_code_string("1-W-S-F")
    spec2 = CustomSpecification.from_part_code_string("1-W-S-F")
    spec3 = CustomSpecification.from_part_code_string("1-W-S-M")
    print("Spec1 == Spec2:", spec1 == spec2)  # Should be True
    print("Spec1 == Spec3:", spec1 == spec3)  # Should be False


    
