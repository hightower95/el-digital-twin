import el_analysis

from sideload_devices import project
from dataclasses import dataclass


connections_file = "sample_connections.txt"
filepath = "c:/Users/peter/OneDrive/Documents/Coding/bw/toolkit/examples/" + connections_file
print(f"Loading connections from file: {filepath}")

@dataclass
class ImportedConnection:
    """Class to represent a connection imported from a file."""
    source: el_analysis.Address
    destination: el_analysis.Address
    signal_name: str

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

            if len(parts) != 7:
                print(f"Invalid connection format: {line.strip()}")
                continue

            device_1 = parts[0].strip()
            interface_1 = parts[1].strip()
            pin_1 = parts[2].strip()
            device_2 = parts[3].strip()
            interface_2 = parts[4].strip()
            pin_2 = parts[5].strip()
            signal_name = parts[6].strip()

            address_1 = el_analysis.Address.from_tuple(
                ("C", device_1, interface_1, pin_1)
            )

            address_2 = el_analysis.Address.from_tuple(
                ("C", device_2, interface_2, pin_2)
            )

            connections.append(ImportedConnection(address_1, address_2, signal_name))
    return connections

connections = read_connections_from_file(filepath)


for connection in connections:
    connection = project.create_connection(connection.source, connection.destination, signal_name=connection.signal_name)
   
# headers, data_rows = project.create_interface_summary()

project.create_connection_summary()
