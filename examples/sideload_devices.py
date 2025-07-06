from dataclasses import dataclass
from typing import List, Optional
from el_analysis import Project, Address, get_connector_from_part_number

# Sideloading is when we manually add devices and connections to a project without using the built-in loading methods.

# We might do this when we have a format that the library does not support, or if we want to modify the data before adding it to the project.


# Create the project instance
project = Project("Project Name", default_location="C")

# Read in our data. In this case we are reading from a file that contains a list of connectors and their part numbers
file_data = None
with open("c:/Users/peter/OneDrive/Documents/Coding/bw/toolkit/examples/sample_device.txt", "r") as file:
    file_data = file.read()

for line in file_data.splitlines():
    if not line.strip():
        continue  # Skip empty lines
    address_str, part_number = line.strip().split(",")
    address = Address.from_string(address_str)

    # We create an "empty" device at the specified address.
    # If the device already exists, it will return the existing device.
    new_device = project.get_device_by_address(address.product_address, create_if_not_exists=True)

    if new_device is None:
        print("Could not create device for address:", address_str)
        continue

    if new_device.is_cable:
        # The library guesses if the device is a cable based on the address.
        # Sometimes we want to override this, so we can set the device as a cable explicitly.
        # new_device.is_cable = True
        continue
    
    # If the address is an interface, we create the interface for the device, and populate it with the connector.
    # The library handles creating a connector object with the correct part number / part type / aliases
    if address.is_interface and address.interface is not None:
        connector = get_connector_from_part_number(part_number)
        interface = new_device.add_interface(address.interface, connector=connector)

        if interface is None:
            print("Could not create interface for address:", address_str)
            continue

project.summarize()