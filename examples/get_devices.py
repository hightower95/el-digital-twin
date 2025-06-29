
import el_analysis


new_project = el_analysis.Project("Project Name")

devices_to_add = [
    "A1",
    "A2",
    "A3"
]

interfaces_to_add = {}
interfaces_to_add["A1"] = ["X1", "X2"]
interfaces_to_add["A2"] = ["X1", "X3"]
interfaces_to_add["A3"] = ["X2", "X3", "X4"]

pins_to_add = {
    "X1": ["1", "2"],
    "X2": ["3", "4"],
    "X3": ["5", "6"],
}

# Importing to the Project
for device_name in devices_to_add:
    new_device = new_project.new_device(device_name)

    device_interfaces = interfaces_to_add[device_name]
    for interface_name in device_interfaces:
        new_interface = new_device.add_interface(interface_name)

        if interface_name in pins_to_add:
            for pin_name in pins_to_add[interface_name]:
                new_interface.add_pin(pin_name)

# project.load_device_table()


# Summarising the project
for device in new_project.devices:
    print(f"Device: {device.name}, Address: {device.address}")
    for interface in device.interfaces:
        print(f"  Interface: {interface.name}, Address: {interface.address}")
        if interface.connector:
            print(f"    Connector: {interface.connector.part_number}")
        else:
            print("    No connector assigned")


        for pin in interface.pins:
            print(f"    Pin: {pin.name}, Address: {pin.address}")