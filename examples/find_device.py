import el_analysis

from sideload_devices import project



search_address = el_analysis.Address.from_string("+C+W11.X1")   # Example address to search for

print(f"Searching for device at address: {search_address}")

device_to_find = project.get_device_by_address(search_address)

if device_to_find:
    print(f"Device found: {device_to_find.name} at address {device_to_find.address}")

else:
    print(f"No device found at address {search_address}.")