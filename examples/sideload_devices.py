from dataclasses import dataclass
from typing import List, Optional
from el_analysis import Project, Address#, get_connector_from_part_number

# Sideloading is when we manually add devices and connections to a project without using the built-in loading methods.



from examples.custom_connector_db_interface import database_interface

# Create the project instance
project = Project("Project Name", default_location="C", connectors_database=database_interface)

# Read in our data. In this case we are reading from a file that contains a list of connectors and their part numbers
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Build path to the connections file in the sample_data_simple folder
devices_file = "sample_device.txt"
filepath = os.path.join(script_dir, "sample_data_simple", devices_file)
file_data = None
with open(filepath, "r") as file:
    file_data = file.read()

for line in file_data.splitlines():
    if not line.strip():
        continue  # Skip empty lines
    address_str, part_number = line.strip().split(",")
    address = Address.from_string(address_str)

    # We create an "empty" device at the specified address.
    # If the device already exists, it will return the existing device.
    new_device = project.search_by_address(address.product_address, create_if_not_exists=True)

    if new_device is None:
        print("Could not create device for address:", address_str)
        continue

    if new_device.is_cable: #type:ignore
        # The library guesses if the device is a cable based on the address.
        # Sometimes we want to override this, so we can set the device as a cable explicitly.
        # new_device.is_cable = True
        # continue
        pass
    
    # If the address is an interface, we create the interface for the device, and populate it with the connector.
    # The library handles creating a connector object with the correct part number / part type / aliases
    if address.is_interface and address.interface is not None:
        connector = project.get_connector_from_part_number(part_number)
        interface = new_device.add_interface(address.interface, connector=connector) #type:ignore

        if interface is None:
            print("Could not create interface for address:", address_str)
            continue
    else:
        print("Could not create interface for address:", address_str)

if __name__ == "__main__":
    project.summarize()