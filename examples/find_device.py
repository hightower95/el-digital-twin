import el_analysis

from sideload_devices import project


# In this example, we will search for a device by its address.

# We assume that the project has been populated with devices and interfaces (in this case refer to sideload_devices.py).

# Example Use Cases:
# 1. We want to print a summary of a specific device - to know what connectors it has, what interfaces it has, etc.


# Method:
# First we create the search address. This may be improved later to be less verbose.
search_address = el_analysis.Address.from_string("+C+W11")   # Example address to search for
# Note: we can tweak appearance of address by editing the config - see examples/change_config.py
print(f"Searching for device at address: {search_address}")
device_to_find = project.search_by_address(search_address)

if device_to_find:
    print(f"Device found: {device_to_find.name} at address {device_to_find.address}")
else:
    raise ValueError(f"Device not found at address {search_address}.")

# Use Case 1: Summarise a specific devices connectors and interfaces
print(f"Summarising device {device_to_find.name} at address {device_to_find.address}")

device_to_find.print_device_summary() # type:ignore  # This will print a summary of the device and its interfaces