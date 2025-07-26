
from connector_part import ConnectorPart, Connector, Variants, Materials, Sizes, Genders
import os

def generate_part_number(part: ConnectorPart) -> str:
    """Generates a part number for the given connector part. We use details from the part type to create a unique part number"""

    # First two numbers are decided by the material
    material_code = ord(part.material.short_name) 

    # Next two numbers are decided by the variant
    variant_code = ord(part.variant.short_name) 

    # Next two numbers are decided by the size
    size_code = ord(part.size.short_name)
    # Last two numbers are decided by the gender
    gender_code = ord(part.gender.short_name)

    return f"PN-{material_code:02}_{variant_code:02}_{size_code:02}_{gender_code:02}"


def generate_random_connector() -> Connector:
    """Generates a random connector with a random part number."""
    import random
    variant = random.choice(list(Variants)).value
    material = random.choice(list(Materials)).value
    size = random.choice(list(Sizes)).value
    gender = random.choice(list(Genders)).value
    part = ConnectorPart(variant=variant, material=material, size=size, gender=gender)
    part_number = generate_part_number(part)
    return Connector(part=part, part_number=part_number)

def generate_all_permutations() -> list[Connector]:
    """Generates all permutations of connectors based on the defined components."""
    from itertools import product

    connectors = []
    for variant in Variants:
        for material in Materials:
            for size in Sizes:
                for gender in Genders:
                    part = ConnectorPart(variant=variant.value, material=material.value, size=size.value, gender=gender.value)
                    part_number = generate_part_number(part)
                    connectors.append(Connector(part=part, part_number=part_number))
    return connectors

# for x in range(10):
#     connector = generate_random_connector()
#     print(f"Connector Part Type: {connector.part_type}, Connector Part Number: {connector.part_number}")

all_connectors = generate_all_permutations()
for connector in all_connectors:
    print(f"Connector Part Type: {connector.part_type}, Connector Part Number: {connector.part_number}")

# lets check there are no PN collisions
part_numbers = set([connector.part_number for connector in all_connectors])
if len(part_numbers) != len(all_connectors):
    print("There are duplicate part numbers!")
else:
    print("All part numbers are unique.")


script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "connectors.csv")
with open(csv_path, "w") as f:
    f.write("Connector Part Type, Connector Part Number\n")
    for connector in all_connectors:
        f.write(f"{connector.part_type}, {connector.part_number}\n")