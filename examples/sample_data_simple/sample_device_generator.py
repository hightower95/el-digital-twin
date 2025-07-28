
import random
from typing import Set, Any, Optional, Union
from dataclasses import dataclass, field
import os
import re

# Add the parent directory to the Python path to access adjacent modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Now we can import from the adjacent folder
from sample_connector_db.connector_database import ConnectorDatabase
from sample_connector_db.connector_part import Variants, Materials, Sizes, Genders
from custom_connector_db_interface import CustomSpecification
from el_analysis.connector_toolkit.connector import Connector

connector_db = ConnectorDatabase()
connector_db.add_connector_deserialization_handler(CustomSpecification)

# Improvements:
#  1. When picking connector for a cable, use a part number that corresponds to the device connector
# This could be improved with a kind of forest fire algorithm
#
# e.g. Pick a starting device, 
CHANCE_REUSE_SIGNAL = 0.3
CHANCE_GENERATE_SIGNAL_GROUP = 0.1
CHANCE_GENERATE_SIGNAL_PAIR = 0.4

CHANCE_FAIL_COPY_ACROSS_SIGNALS = 0.5
DEFAULT_MAX_SIGNALS = 6

output_filename = "sample_device.txt"
random.seed(output_filename)
output_filename = os.path.join(os.path.dirname(__file__), output_filename)

def generate_part_numbers(condition=None, count=10) -> Set[str]:
    numbers = set()
    for _ in range(count):
        number1 = random.randint(1000, 3999)
        number2 = random.randint(100, 899)
        if condition is None or condition(number1, number2):
            numbers.add(f"1234 {number1}-{number2}")
    return numbers

def is_odd(x: int) -> bool:
    return x % 2 == 1

def is_even(x: int) -> bool:
    return x % 2 == 0

def get_opposite_part_number(part_number: str) -> str:
    """Returns the opposite part number based on the last digit."""
    if not part_number:
        return part_number
    match = re.match(r"1234 (\d+)-(\d+)", part_number)
    if not match:
        return part_number
    number1, number2 = map(int, match.groups())
    number1 += 4000
    number2 += 1

    result = f"1234 {number1}-{number2}"
    # print(f"get_opposite_part_number called with {part_number}, returning {result}")

    return result

def get_connectors(quantity=5) -> list[Connector]:
    """Returns a list of all connectors."""
    if quantity is None or quantity <= 0:
        return connector_db.connectors
    
    connectors_selected = []

    # max loops
    max_loops = 1000

    while len(connectors_selected) < quantity:
        if max_loops <= 0:
            raise ValueError("Could not find enough connectors that are not mateable with existing connectors.")
        max_loops -= 1
        # Get a random connector
        connector = connector_db.get_random_connector()
        # check connector not in connectors_selected
        if connector in connectors_selected:
            continue

        if not connector or not connector.component:
            continue

        # connector should not be mateable with any existing connector
        if any(connector.component.can_connect_to(existing_connector) or connector.minified_part_code == existing_connector.minified_part_code for existing_connector in connectors_selected):
            continue
        
        connectors_selected.append(connector)

    return connectors_selected

# generated_part_numbers = list(generate_part_numbers())

# generate_part_numbers_devices = list(generate_part_numbers(condition=lambda x, y: is_even(y), count=5))

generated_connectors = get_connectors(6)
# generate_part_numbers_devices = [connector.part_number for connector in generated_connectors]
def get_random_connector(connectors, chance_of_material_change=0.7) -> Connector:
    """Returns a random connector from the list of connectors."""
    # TODO TODO TODO
    connector = random.choice(connectors)
    material = connector.component.values.get("material")
    if random.random() < chance_of_material_change:
        choices = connector_db.find_adjacent_connectors(connector)

        # Change the material of the connector
        # choices = connector.component.aspects["material"].get_options()
        # current_material = connector.component.values["material"]
        # choices.remove(connector.component.values["material"])  # Remove current material to avoid no change
        # new_material = random.choice(choices)
        
        connector = random.choice(choices)
        if connector.component is None:
            print(f"Warning: Connector {connector.part_code} has no component specification.")
            return connector
        new_material = connector.component.values.get("material", "Unknown")
        print("Changed material of connector to", new_material, "from", material)
    return connector

# print(generated_part_numbers)


device_names = [
    "A2",
    "A3",
    "A4",
    # "A5",
    # "A12",
    # "A123",
    # "B21",
    # "A6",
    # "KA2",
]

cable_names = [
    "W10",
    "W11",
    "W12",      
    "W13",
    "W14",
    "W15",
    "W16",  
    "W17",
    "W18",
    "W19",
    "W20",
    "W21",
    "W22",
]

min_connectors = 2
max_connectors = 7

location = "C"

cable_interfaces = {

}
device_interfaces = {}

@dataclass
class Interface:
    name: str
    connector: Connector
    connects_to: Optional['Interface'] = None
    attached_to: Optional[Union['Device', 'Cable']] = None  # Can be a Device or Cable
    pins: dict[str, str] = field(default_factory=dict)  # Pin mapping for signals

    @property
    def part_number(self):
        return self.connector.part_number if self.connector else ""

    @property
    def address(self):
        if self.attached_to is None:
            return f"{self.name}"
        return f"{self.attached_to.name}.{self.name}"

@dataclass
class Cable:
    name: str
    interfaces: list[Interface]

    def __str__(self):
        return f"{self.name} with interfaces {self.interfaces}"
    
    def get_unconnected_interfaces(self):
        return [interface for interface in self.interfaces if interface.connects_to is None]
    
    def get_signals(self):
        signals = set()
        for interface in self.interfaces:
            if interface.connects_to is not None:
                signals.update(interface.pins.values())
        return signals
    
    @property
    def unconnected_interfaces_count(self):
        return len(self.get_unconnected_interfaces())

cables: list[Cable] = []
@dataclass
class Device:
    name: str
    interfaces: list[Interface]

    def __str__(self):
        return f"{self.name} with interfaces {self.interfaces}"
    
    def get_unconnected_interfaces(self):
        return [interface for interface in self.interfaces if interface.connects_to is None]
    
    def get_signals(self):
        signals = set()
        for interface in self.interfaces:
            if interface.connects_to is not None:
                signals.update(interface.pins.values())
        return signals
    
    @property
    def unconnected_interfaces_count(self):
        return len(self.get_unconnected_interfaces())
devices: list[Device] = []

# Generate devices and cables with interfaces
print("Generating devices and cables with interfaces...")

for device_name in device_names:
    device = Device(name=device_name, interfaces=[])

    connector_count = random.randint(3, max_connectors)
    for x in range(1, connector_count):
        chosen_connector = get_random_connector(generated_connectors)
        # chosen_part_number = random.choice(generate_part_numbers_devices)
        interface = Interface(name=f"X{x}", connector=chosen_connector)
        interface.attached_to = device
        device.interfaces.append(interface)
    devices.append(device)

print(f"Generated {len(devices)} devices with interfaces.")
# summarize devices and interfaces
for device in devices: 
    print(f"\tDevice {device.name} has {len(device.interfaces)} interfaces: {', '.join([interface.name for interface in device.interfaces])}")

for cable_name in cable_names:
    cable = Cable(name=cable_name, interfaces=[])
    connector_count = random.randint(3, 6)
    for x in range(1, connector_count):
        chosen_connector = get_random_connector(generated_connectors)
        interface = Interface(name=f"X{x}", connector=chosen_connector)
        interface.attached_to = cable
        cable.interfaces.append(interface)
    cables.append(cable)
print(f"Generated {len(cables)} cables with interfaces.")
      # summarize cables and interfaces
for cable in cables:
    print(f"\tCable {cable.name} has {len(cable.interfaces)} interfaces: {', '.join([interface.name for interface in cable.interfaces])}")

# Now we connect up devices and cables
def connect_devices(devices: list[Device], cables: list[Cable]):

    for device in devices:
        # max_connections = random.randint(1, len(device.interfaces))
        for interface in device.interfaces:
            if random.random() < 0.3:  # 30% chance to connect this interface
                continue

            if interface.connects_to is None:
                other_device_choices = [d for d in devices if d != device and d.unconnected_interfaces_count > 0]
                if len(other_device_choices) == 0:
                    continue
                other_device = random.choice(other_device_choices)
                interface_choices = other_device.get_unconnected_interfaces()
                if len(interface_choices) == 0:
                    continue
                other_interface = random.choice(interface_choices)
                # interface.connects_to = other_interface
                # other_interface.connects_to = interface

                # now we need a cable - we need to find a cable with at least 2 unconnected interfaces
                cable_options = [c for c in cables if c.unconnected_interfaces_count >= 2]
                if len(cable_options) == 0:
                    continue
                cable = random.choice(cable_options)
                cable_interface = random.choice(cable.get_unconnected_interfaces())

                # We connect the cable to the device
                cable_interface.connects_to = interface
                interface.connects_to = cable_interface

                # We need to align the connectors
                opposite_connector = connector_db.get_opposite_connector(interface.connector)
                if opposite_connector is None:
                    print(f"No opposite connector found for {interface.connector.part_code}")
                    continue
                cable_interface.connector = opposite_connector

                other_cable_interface = random.choice(cable.get_unconnected_interfaces())

                other_interface.connects_to = other_cable_interface
                other_cable_interface.connects_to = other_interface
                other_cable_interface.connector = opposite_connector
                # other_cable_interface.part_number = get_opposite_part_number(other_interface.part_number)

                print(f"Connecting {device.name}.{interface.name} to {interface.connects_to.address} -- {other_interface.connects_to.address} to {other_device.name}.{other_interface.name}")

connect_devices(devices, cables)

# lets assume every connctor has 6 pins
@dataclass
class Connection:
    from_product: str
    from_pin: str
    from_interface: str
    to_product: str
    to_interface: str
    to_pin: str
    signal: Optional[str] = None

    def to_dict(self):
        return {
            "from_product": self.from_product,
            "from_pin": self.from_pin,
            "to_product": self.to_product,
            "to_pin": self.to_pin,
            "signal": self.signal
        }

connections = []

def generate_signals(count=DEFAULT_MAX_SIGNALS, seed_signals=None, group_enabled: bool = True) -> list[str]:
    signals_generated = set()
    if seed_signals:
        filtered_seed_signals = [s for s in seed_signals if "SignalGroup" not in s]
        seed_signals = filtered_seed_signals if filtered_seed_signals else None

    while len(signals_generated) < count:
        if seed_signals and random.random() < CHANCE_REUSE_SIGNAL:  # 50% chance to use seed signals
            # Use seed signals if available
            signal = random.choice(seed_signals)
            signals_generated.add(signal)
            seed_signals.remove(signal)  # Remove to avoid duplicates
            print(f"Using seed signal: {signal}")

        elif group_enabled and random.random() < CHANCE_GENERATE_SIGNAL_GROUP:  # 10% chance to generate a signal group
            group_name = random.choice(["A", "B", "C", "D", "E", "F"])
            a = f"SignalGroup-CH-{group_name}-high"
            b = f"SignalGroup-CH-{group_name}-low"
            c = f"SignalGroup-CH-{group_name}-gnd"
            signals_generated.add(a)
            signals_generated.add(b)
            signals_generated.add(c)

        elif random.random() < CHANCE_GENERATE_SIGNAL_PAIR:  # 40% chance to generate signal pair
            signal_id = random.randint(1000, 9999)
            a = f"SignalGroup-28V-{signal_id}-A"
            b = f"SignalGroup-GND-{signal_id}-B"
            signals_generated.add(a)
            signals_generated.add(b)

        else:
            signals_generated.add(f"Signal-{random.randint(1000, 9999)}")

    return list(signals_generated)


def generate_signals_to_interface(interface: Interface, max_signals=DEFAULT_MAX_SIGNALS):
    if interface.connects_to is None:
        return
    
    def assign_pins(signals: list[str]):
        assignment = {}
        if len(signals) == 0:
            return assignment
        for i, signal in enumerate(signals):
            pin_number = random.randint(1, 55)
            pin_name = f"{pin_number:02d}"
            assignment[signal] = pin_name
        return assignment
    
    available_signals = set()
    if interface.attached_to:
        available_signals = interface.attached_to.get_signals()

    signals = generate_signals(max_signals, seed_signals=available_signals)
    pin_mapping = assign_pins(signals)

    for signal, pin in pin_mapping.items():
        interface.pins[pin] = signal

        if "SignalGroup" not in signal and random.random() < CHANCE_FAIL_COPY_ACROSS_SIGNALS:
            if isinstance(interface.connects_to, Interface):
                interface.connects_to.pins[pin] = signal
                # print(f"Adding signal {signal} to {interface.address} on pin {pin}")
                # print(f"Adding signal {signal} to {interface.connects_to.address} on pin {pin}")
        else:
            interface.connects_to.pins[pin] = signal
            # print(f"Adding signal {signal} to {interface.address} on pin {pin}")

# Improvement, we follow the existing connection map and fill in signals.
# e.g. a signal added to A1.X1 that connects to B2.X1 could also turn up on another B2 interface
for device in devices:
    for interface in device.interfaces:
        generate_signals_to_interface(interface)

# Generate connections based on interfaces
print("Generating connections...")
for device in devices:
    for interface in device.interfaces:
        # if interface.connects_to is None:
        #     continue

        for pin, signal in interface.pins.items():
            connections.append(Connection(
                from_product=device.name,
                from_interface=interface.name,
                from_pin=pin,
                to_product=interface.connects_to.attached_to.name, # type:ignore
                to_interface=interface.connects_to.name, # type:ignore
                to_pin=pin,
                signal=signal
            ))

for cable in cables:
    for interface in cable.interfaces:
        if interface.connects_to is None:
            continue

        for pin, signal in interface.pins.items():
            connections.append(Connection(
                from_product=cable.name,
                from_interface=interface.name,
                from_pin=pin,
                to_product=interface.connects_to.attached_to.name, # type:ignore
                to_interface=interface.connects_to.name,
                to_pin=pin,
                signal=signal
            ))



# Generate device list file
print("Generating device list file...")

with open(output_filename, "w") as fp:
    for device in devices:
        # print(device)
        for interface in device.interfaces:
            fp.write(f"+{location}+{device.name}.{interface.name},{interface.part_number}\n")

    for cable in cables:
        # print(cable)

        for interface in cable.interfaces:
            fp.write(f"+{location}+{cable.name}.{interface.name},{interface.part_number}\n")
            


# Generate connection list file
print("Generating connection list file...")

#  From Product | From Pin | To Product | To Pin | Signal

output_connection_filename = "sample_connections.txt"
output_connection_filename = os.path.join(os.path.dirname(__file__), output_connection_filename)
with open(output_connection_filename, "w") as fp:
    for conn in connections:
        fp.write(f"{conn.from_product},{conn.from_interface},{conn.from_pin},"
                 f"{conn.to_product},{conn.to_interface},{conn.to_pin},{conn.signal}\n")