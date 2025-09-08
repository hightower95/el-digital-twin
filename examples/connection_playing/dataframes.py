from typing import Optional, List
import pandas as pd
from dataclasses import dataclass, field


@dataclass
class Bundle:
    name: str
    parent: Optional['Bundle'] = None
    connections: List[str] = field(default_factory=list)
    children: List['Bundle'] = field(default_factory=list)
    minified_name: Optional[str] = None

    def __post_init__(self):
        if self.name.startswith("TW"):
            self.minified_name = "TW"
        elif self.name.startswith("SH"):
            self.minified_name = "SH"

    @property
    def barcode(self) -> str:
        return f"{self.minified_name}-{','.join(self.connections)}"

    @property
    def top_bundle(self) -> 'Bundle':
        if self.parent is None:
            return self
        return self.parent.top_bundle

    def check_parents(self, condition) -> bool:
        if self.parent is None:
            return True
        if not condition(self.parent):
            return False
        return self.parent.check_parents(condition)

    def check_children(self, condition) -> bool:
        for child in self.children:
            if not condition(child):
                return False
            if not child.check_children(condition):
                return False
        return True

    def print_children(self, level=0):
        print('  ' * level + f"- {self.name} ({self.minified_name})")
        for child in self.children:
            child.print_children(level + 1)

    def print_children_one_liner(self):
        print(
            f"{self.name} ({self.minified_name}) -> {[child.name for child in self.children]}")

    def __repr__(self) -> str:
        return f"Bundle(name={self.name}, direct_connection={self.connections}, children={len(self.children)})"

    def is_compatible_with(self, other: 'Bundle') -> bool:
        print(
            f"Checking compatibility between {self.minified_name} ({[child.minified_name for child in self.children]}) and {other.minified_name} ({[child.minified_name for child in other.children]})")

        same_type = self.minified_name == other.minified_name

        same_connections = set(self.connections) == set(
            other.connections)  # have the same pins connected

        other_has_same_or_more_children = len(
            other.children) >= len(self.children)

        if not (same_type and same_connections and other_has_same_or_more_children):
            if not same_type:
                print(" - Incompatible due to type")
                print(f"   - {self.minified_name} vs {other.minified_name}")
            if not same_connections:
                print(" - Incompatible due to connections")
                print(f"   - {self.connections} vs {other.connections}")
            if not other_has_same_or_more_children:
                print(" - Incompatible due to child count")
                print(f"   - {len(self.children)} vs {len(other.children)}")
            return False

        # have to find a similar chi
        child_compatibility = {}
        for child in self.children:
            child_checked = False
            for other_child in other.children:
                if child.barcode == other_child.barcode:
                    child_compatible = child.is_compatible_with(other_child)
                    child_compatibility[child.barcode] = child_compatible
                    child_checked = True
            if not child_checked:
                print(
                    f" - Incompatible due to missing child {child.barcode} in other, got {[c.barcode for c in other.children]}")
                return False

        all_children_compatible = all(child_compatibility.values())
        if not all_children_compatible:
            print(" - Incompatible due to child compatibility")
            return False

        return same_type and same_connections and other_has_same_or_more_children and all_children_compatible


@dataclass
class ConnectionCharacteristic:
    pin_name: str
    signal: str
    awg: str
    bundles_string: str
    bundle: Optional[Bundle] = None
    connects_to: Optional[str] = None


@dataclass
class Connector:
    connections: list[ConnectionCharacteristic]
    # bundles: list[Bundle] = field(default_factory=list)
    bundle_dict: dict[str, Bundle] = field(default_factory=dict)

    @property
    def bundle(self) -> Optional[Bundle]:
        # Return the top-most bundle
        top_bundles = []
        for connection in self.connections:
            if connection.bundle:
                top_bundle = connection.bundle.top_bundle
                top_bundles.append(top_bundle)
        if not top_bundles:
            return None
        # Return the bundle with the most votes
        most_voted_bundle = max(top_bundles, key=lambda b: b.name)

        return most_voted_bundle

    @property
    def bundles(self) -> List[Bundle]:
        return list(self.bundle_dict.values())

    @property
    def pins(self) -> List[str]:
        return [conn.pin_name for conn in self.connections]

    def get_connection_by_pin(self, pin_name: str) -> Optional[ConnectionCharacteristic]:
        for connection in self.connections:
            if connection.pin_name == pin_name:
                return connection
        return None

    def summarise_bundles(self):
        start_bundle = self.bundle
        if not start_bundle:
            print("No bundles found")
            return

        bundle_stack = [start_bundle]
        while bundle_stack:
            current_bundle = bundle_stack.pop()
            if current_bundle.connections:
                print(
                    f"Bundle: {current_bundle.name} (direct connection: {current_bundle.connections})")
            else:
                print(f"Bundle: {current_bundle.name} (no direct connection)")
            for child in current_bundle.children:
                bundle_stack.append(child)
            # print("Stack now", bundle_stack)


def get_connector_from_connections(connections: list[ConnectionCharacteristic]) -> Connector:
    connector = Connector(connections=connections)

    def get_or_create_bundle(name: str) -> Bundle:
        if name in connector.bundle_dict:
            return connector.bundle_dict[name]
        new_bundle = Bundle(name=name)
        connector.bundle_dict[name] = new_bundle
        return new_bundle

    for connection in connections:

        current_bundles = []
        # The first token is the bottom-most bundle
        bundle_names = connection.bundles_string.split('.')
        bundle_names.reverse()
        # print(connection.pin_name, bundle_names)
        if connection.connects_to:
            if connection.connects_to in connector.bundle_dict:
                connector.bundle_dict[connection.connects_to].connections.append(
                    connection.pin_name)
            else:
                new_bundle = get_or_create_bundle(connection.connects_to)
                new_bundle.connections.append(connection.pin_name)

        # Remove bundles that are "CB1" or "SH1" as these are not real bundles
        # bundle_names = [
        #     name for name in bundle_names if name not in ("CB1", "SH1", "")]
        if not bundle_names or len(bundle_names) == 0:
            continue

        previous_bundle = None
        for name in bundle_names:
            bundle = get_or_create_bundle(name)
            if previous_bundle:
                if bundle not in previous_bundle.children:
                    previous_bundle.children.append(bundle)
                bundle.parent = previous_bundle
            previous_bundle = bundle
            current_bundles.append(bundle)

        last_bundle = current_bundles[-1] if current_bundles else None
        if last_bundle:
            if connection.connects_to is None:
                last_bundle.connections.append(connection.pin_name)
            connection.bundle = last_bundle

    # For demonstration, we can print the bundle hierarchy

    def print_bundles(bundle: Bundle, level=0):
        if len(bundle.connections) > 0:
            print('  ' * level +
                  f"- {bundle.name} ({bundle.minified_name}) ({','.join(bundle.connections)})")
        else:
            print('  ' * level + f"- {bundle.name} ({bundle.minified_name})")
        for child in bundle.children:
            print_bundles(child, level + 1)

    # Print all top-level bundles
    for bundle in connector.bundle_dict.values():
        if bundle.parent is None:
            print_bundles(bundle)

    return connector


simple_can = [
    ConnectionCharacteristic("A", "CAN B High", "AWG 24", "TW1.SH2.SH1.CB1"),
    ConnectionCharacteristic("B", "CAN B Low", "AWG 24", "TW1.SH2.SH1.CB1"),
    ConnectionCharacteristic("C", "CAN B Gnd", "",
                             "SH1.CB1", connects_to="SH2"),
]

simple_can_shifted = [
    ConnectionCharacteristic("B", "CAN B High", "AWG 24", "TW1.SH2.SH1.CB1"),
    ConnectionCharacteristic("D", "CAN B Low", "AWG 24", "TW1.SH2.SH1.CB1"),
    ConnectionCharacteristic("C", "CAN B Gnd", "",
                             "SH1.CB1", connects_to="SH2"),
]
# simple_can = get_connector_from_connections(simple_can)
# print(simple_can.bundle)
# simple_can.summarise_bundles()
# # print(simple_can)
# a = simple_can.get_connection_by_pin("A")
# print(a)
# print(a.bundle)

double_can = [
    ConnectionCharacteristic("A", "CAN B High", "AWG 24", "TW1.SH2.SH1.CB1"),
    ConnectionCharacteristic("B", "CAN B Low", "AWG 24", "TW1.SH2.SH1.CB1"),
    ConnectionCharacteristic("C", "CAN B GND", "",
                             "SH1.CB1", connects_to="SH2"),
    ConnectionCharacteristic("D", "CAN E High", "AWG 24", "TW2.SH3.SH1.CB1"),
    ConnectionCharacteristic("E", "CAN E Low", "AWG 24", "TW2.SH3.SH1.CB1"),
    ConnectionCharacteristic("F", "CAN E GND", "",
                             "SH1.CB1", connects_to="SH3"),
]
# double_can = get_connector_from_connections(double_can)
# print(double_can.bundle)
# double_can.summarise_bundles()
simple_rs422 = [
    ConnectionCharacteristic("A", "CAN B High", "AWG 24", "TW1.SH2.SH1.CB1"),
    ConnectionCharacteristic("B", "CAN B High", "AWG 24", "TW1.SH2.SH1.CB1"),
    ConnectionCharacteristic("C", "CAN B GND", "",
                             "SH1.CB1", connects_to="SH2"),
    ConnectionCharacteristic("D", "CAN E High", "AWG 24", "TW2.SH2.SH1.CB1"),
    ConnectionCharacteristic("E", "CAN E High", "AWG 24", "TW2.SH2.SH1.CB1")
]


simple_singles_conflict_can = [
    ConnectionCharacteristic("A", "SINGLE 1", "AWG 24", "SH1.CB1"),
    ConnectionCharacteristic("B", "SINGLE 2", "AWG 24", "SH1.CB1"),
]

simple_singles_no_conflict_can = [
    ConnectionCharacteristic("1", "SINGLE 1", "AWG 24", "SH1.CB1"),
    ConnectionCharacteristic("2", "SINGLE 2", "AWG 24", "SH1.CB1"),
]

complicated_1 = [
    ConnectionCharacteristic("A", "CAN B High", "AWG 24", "TW1.SH2.SH1.CB1"),
    ConnectionCharacteristic("B", "CAN B Low", "AWG 24", "TW1.SH2.SH1.CB1"),
    ConnectionCharacteristic("C", "CAN B GND", "",
                             "SH1.CB1", connects_to="SH2"),
    ConnectionCharacteristic("D", "CAN E High", "AWG 24", "TW2.SH3.SH1.CB1"),
    ConnectionCharacteristic("E", "CAN E Low", "AWG 24", "TW2.SH3.SH1.CB1"),
    ConnectionCharacteristic("F", "CAN E GND", "",
                             "SH1.CB1", connects_to="SH3"),
    ConnectionCharacteristic("G", "Something Power", "AWG 12", "SH4.SH1.CB1"),
    ConnectionCharacteristic("H", "Something Power", "AWG 12", "SH1.CB1"),
    ConnectionCharacteristic("I", "Something Power GND", "",
                             "SH1.CB1", connects_to="SH4"),
]


def create_connection_dataframe(connections: list[ConnectionCharacteristic],
                                interface_from="+C+W1.X1",
                                interface_to="+C+W1.X2") -> pd.DataFrame:
    device_connections = []

    for connection in connections:
        from_address_string = f"{interface_from}.{connection.pin_name}"
        to_address_string = f"{interface_to}.{connection.pin_name}"
        device_connections.append({
            "from": from_address_string,
            "to": to_address_string,
            "signal": connection.signal,
            "awg": connection.awg,
            "bundles": connection.bundles
        })

    df = pd.DataFrame(device_connections)
    return df


def check_compatibility(connections: list[ConnectionCharacteristic]) -> bool:
    signals = set()
    for connection in connections:
        if connection.signal in signals:
            return False
        signals.add(connection.signal)
    return True


def can_signals_from_a_go_into_b(connector_a: Connector, connector_b: Connector) -> bool:
    pins_to_check = connector_a.pins
    while pins_to_check:
        pin = pins_to_check.pop()
        conn_a = connector_a.get_connection_by_pin(pin)
        if not conn_a:
            # This should not happen
            raise ValueError(f"Pin {pin} not found in connector A")
        conn_b = connector_b.get_connection_by_pin(pin)
        if not conn_b:
            # This is not fine?
            print(
                f"Warning: {conn_a} has no matching connection in {connector_b}")
            continue
        # conn_a.bundle.minified_name == conn_b.bundle.minified_name
        if conn_a.bundle is None:
            print(f"Warning: {conn_a} has no bundle")
            continue
        if conn_b.bundle is None:
            print(f"Warning: {conn_b} has no bundle")
            continue

        if not conn_b.bundle.is_compatible_with(conn_a.bundle):
            print(
                f"Conflict on pin {pin}: {conn_a.bundle.minified_name} vs {conn_b.bundle.minified_name}")
        else:
            print(f"Pin {pin} is compatible: {conn_a.bundle.minified_name}")

    return True


def can_signals_from_a_go_into_b_pinwise(connector_a: Connector, connector_b: Connector) -> bool:
    for pin_a in connector_a.pins:

        pin_b = connector_b.get_pin(pin_a)
        # TW1   = TW
        pin_a.bundle == pin_b.bundle
        # TW.SH2 = TW.SH2
        pin_a.bundle.parent == pin_b.bundle.parent

        pin_a.bundle.parent.children == pin_b.bundle.parent.children


def can_signals_from_a_go_into_b_bundlewise(connector_a: Connector, connector_b: Connector) -> bool:
    # Go to the bottom levels, and then back to the first shield bundle.

    def _filter_bundles(bundle_list: List[Bundle]) -> List[Bundle]:
        filtered = []
        for bundle in bundle_list:
            if bundle.minified_name == "SH":
                if bundle.check_children(lambda x: x.minified_name != "SH"):
                    filtered.append(bundle)
            elif bundle.children == 0:
                # if no parent is a shield, then add it
                bundle.check_parents(lambda x: x.minified_name != "SH")
                if bundle.parent and bundle.parent.minified_name != "SH":
                    filtered.append(bundle)
        return filtered

    # Find all shield bundles. That dont contain a shield bundle inside them.
    # all_bundles_a = connector_a.bundles
    filtered_bundles_a = _filter_bundles(connector_a.bundles)
    filtered_bundles_b = _filter_bundles(connector_b.bundles)

    print("Filtered bundles A", filtered_bundles_a)
    bundle_compatibility = {}
    for bundle_a in filtered_bundles_a:
        bundle_handled = False
        for bundle_b in filtered_bundles_b:
            if bundle_a.barcode != bundle_b.barcode:
                continue

            if bundle_a.is_compatible_with(bundle_b):
                bundle_compatibility[bundle_a.barcode] = True
                print(
                    f"Bundle connector conn a's {bundle_a.name} is compatible with conn b's {bundle_b.name}")
            else:
                bundle_compatibility[bundle_a.barcode] = False
                print(
                    f"Bundle connector conn a's {bundle_a.name} is NOT compatible with conn b's {bundle_b.name}")
            bundle_handled = True
            break
        if not bundle_handled:
            print(
                f"Bundle connector conn a's {bundle_a.name} has no matching bundle in conn b")
            bundle_compatibility[bundle_a.barcode] = False

    all_bundles_compatible = all(bundle_compatibility.values())
    if not all_bundles_compatible:
        print(" - Incompatible due to bundle compatibility")
        return False
    else:
        print("All bundles compatible")
        return True


# def can_a_go_into_b(connector_a: Connector, connector_b: Connector) -> bool:
    # Bundle comparison

    # AWG comparison

conn_1 = get_connector_from_connections(complicated_1)
conn_2 = get_connector_from_connections(double_can)

# conn_1.summarise_bundles()

can_signals_from_a_go_into_b_bundlewise(conn_1, conn_2)
can_signals_from_a_go_into_b_bundlewise(conn_2, conn_1)
# can_signals_from_a_go_into_b_bundlewise(conn_2, conn_1)

# conn_2 = get_connector_from_connections(simple_rs422)
# conn_2.summarise_bundles()

# can_signals_from_a_go_into_b(conn_1, conn_2)
# can_signals_from_a_go_into_b(conn_2, conn_1)
