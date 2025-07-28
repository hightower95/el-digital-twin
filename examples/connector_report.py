
from sideload_devices import project

# minified part type
# How many varieties of connectors do we have?
minifieds = {}
for interface in project.interfaces:
    print(f"Interface: {interface.address}, Part Number: {interface.part_number}, Part Type: {interface.part_code}, Minified Part Type: {interface.connector.minified_part_type if interface.connector else 'None'}")


    

# What is the opposite connector