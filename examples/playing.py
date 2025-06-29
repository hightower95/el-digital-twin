import el_analysis

el_analysis.config.Address.EnableLogging = True  # Enable logging for the module

print("EL Analysis module initialized successfully.")

addresses = [
    el_analysis.Address("C", "A2", "X4", "1"),
    el_analysis.Address("C", "A2", "X4", "2"),
    el_analysis.Address("C", "A2", "X4", "3"),
    el_analysis.Address("C", "A2", "X4", "4"),
]
# class MockLocation:
#     address = el_analysis.Address(location="E")

project = el_analysis.Project("Test Project", default_location="E")


location = project.get_location_by_name("E")


new_device = location.new_device("A2")

print(f"Created Device: {new_device}")
print(f"Created Device: {new_device.address}")


addr = new_device.address.interface_address

interface = new_device.add_interface("X1")
interface = new_device.add_interface("X2")
interface = new_device.add_interface("X3")

print(interface)

interface.add_pin("1")
interface.add_pin("2")
pin_3 = interface.add_pin("3")

print(pin_3)

for device in project.devices:
    print(f"Device: {device.name}, Address: {device.address}")


print(project.get_device_by_address(el_analysis.Address("E", "A2", "X1")))