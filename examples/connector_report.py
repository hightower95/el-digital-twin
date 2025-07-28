
from sideload_devices import project

# minified part type
# How many varieties of connectors do we have?
minifieds = {}
for interface in project.interfaces:
    print(f"Interface: {interface.address}, Part Number: {interface.part_number}, Part Code: {interface.part_code}, Minified Part Code: {interface.connector.minified_part_code if interface.connector else 'None'}")

    if not interface.connector:
        print(f"Interface {interface.address} has no connector.")
        continue
    minifieds[interface.connector.minified_part_code] = minifieds.get(interface.connector.minified_part_code, set())
    minifieds[interface.connector.minified_part_code].add(interface.connector.part_code)

# Summarize minified part codes
for minified_code, part_codes in minifieds.items():
    print(f"Minified Part Code: {minified_code}, Part Codes: {', '.join(part_codes)}")

    

# What is the opposite connector