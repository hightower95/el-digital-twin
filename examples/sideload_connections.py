import el_analysis

from sideload_devices import project
from dataclasses import dataclass
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Build path to the connections file in the sample_data_simple folder
connections_file = "sample_connections.txt"
filepath = os.path.join(script_dir, "sample_data_simple", connections_file)
# connections_file = "sample_connections.txt"
# filepath = "c:/Users/peter/OneDrive/Documents/Coding/bw/toolkit/examples/" + connections_file
print(f"Loading connections from file: {filepath}")

@dataclass
class ImportedConnection:
    """Class to represent a connection imported from a file."""
    source: el_analysis.Address
    destination: el_analysis.Address
    signal_name: str
    awg: str

    def __repr__(self):
        return f"ImportedConnection(source={self.source}, destination={self.destination}, signal_name='{self.signal_name}')"

def read_connections_from_file(file_path: str) -> list[ImportedConnection]:
    # Example format:
    # A2,X1,17,W13,X2,X2,SignalGroup-GND-8598-B
    # Annotated:
    # Device 1 Name: A2, 
    # Device 1 Interface: X1,
    # Device 1 Pin: 17,
    # Device 2 Name: W13,
    # Device 2 Interface: X2,
    # Device 2 Pin: 2,
    # Signal Name: SignalGroup-GND-8598-B
    connections = []
    with open(file_path, "r") as file:
        for line in file:
            if not line.strip():
                continue  # Skip empty lines
            parts = line.strip().split(",")

            if len(parts) != 8:
                print(f"Invalid connection format: {line.strip()}")
                continue

            device_1 = parts[0].strip()
            interface_1 = parts[1].strip()
            pin_1 = parts[2].strip()
            device_2 = parts[3].strip()
            interface_2 = parts[4].strip()
            pin_2 = parts[5].strip()
            signal_name = parts[6].strip()
            awg = parts[7].strip() 

            address_1 = el_analysis.Address.from_tuple(
                ("C", device_1, interface_1, pin_1)
            )

            address_2 = el_analysis.Address.from_tuple(
                ("C", device_2, interface_2, pin_2)
            )

            connections.append(ImportedConnection(address_1, address_2, signal_name, awg))
    return connections

connections = read_connections_from_file(filepath)


for connection in connections:
    connection = project.create_connection(connection.source, connection.destination, signal_name=connection.signal_name, awg=connection.awg)
   
# headers, data_rows = project.create_interface_summary()

if __name__ == "__main__":
    print("Creating connection summary...")
    project.create_connection_summary()

    # print("Creating interface summary...")
    # project.create_interface_summary()

    print("Creating signal summary...")
    project.create_signal_summary()

    for signal in project.signals:
        print(f"Signal: {signal.name}, Type: {signal.signal_type}, Group: {signal.signal_group}")


    for interface in project.interfaces:
        if interface.signal_count > 0:
            print(f"Interface: {interface.name}")

            # print(interface.get_channels())
            print(interface._channels.print_summary())

        # print(f" {signal.name} connections: ")
        # for touchpoint in signal.touchpoints:
        #     print(f"  Touchpoint: {touchpoint.address}")