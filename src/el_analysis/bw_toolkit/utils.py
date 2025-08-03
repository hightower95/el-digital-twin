from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional

from el_analysis.signal_toolkit.net import Net
if TYPE_CHECKING:
    from el_analysis.models import Interface
    from el_analysis.models.physical.coupling import Coupling
    from el_analysis.bw_toolkit.breakout_wire import BreakoutWire, Compatibility

from el_analysis import logging

def check_interfaces_for_awg_mismatches(interfaces: List[Interface]) -> List[Interface]:
    mismatches = set()
    for interface in interfaces:
        if interface.connected_to is None:
            continue

        interface_a = interface
        interface_b = interface.connected_to

        # Get list of pin names for both interfaces
        all_pins = interface_a.pins + interface_b.pins
        pin_names = {pin.name for pin in all_pins}

        # 2. Check that all pins have matching AWGs
        for pin_name in pin_names:
            pin_a = interface_a.get_pin(pin_name)
            pin_b = interface_b.get_pin(pin_name)

            if pin_a is None or pin_b is None:
                continue

            if pin_a.awg != pin_b.awg:
                mismatches.add(interface)
                print(f"Warning AWG Mismatch: Pin '{pin_a.address}' has awg {pin_a.awg} and '{pin_b.address}' has awg {pin_b.awg}")

    return list(mismatches)


def check_for_interface_signal_mismatches(interfaces):
    raise NotImplementedError("This function is not implemented yet.")

def all_pin_names(coupling: Coupling) -> List[str]:
    """Returns a list of all pin names in the coupling."""
    pin_names = set()
    for interface in [coupling.source, coupling.destination]:
        if not isinstance(interface, Interface):
            logging.warning(f"Expected Interface, got {type(interface)} in coupling {coupling}")
            raise TypeError(f"Expected Interface, got {type(interface)} in coupling {coupling}")
        for pin in interface.pins:
            pin_names.add(pin.name)
    return list(pin_names)

def get_coupling_channels_reduced(coupling: Coupling) -> dict[str, List[Net]]:
    """
    Returns a dictionary of channels for the given coupling.
    Each channel is represented by its name and contains a list of signal names.
    """
    channels = {}
    for pin_name in all_pin_names(coupling):
        if not isinstance(coupling.source, Interface) or not isinstance(coupling.destination, Interface):
            logging.warning(f"Expected Interface, got {type(coupling.source)} and {type(coupling.destination)} in coupling {coupling}")
            raise TypeError(f"Expected Interface, got {type(coupling.source)} and {type(coupling.destination)} in coupling {coupling}")

        pin_a = coupling.source.get_pin(pin_name)
        pin_b = coupling.destination.get_pin(pin_name)

        if pin_a is not None and pin_a.signal is not None:
            channel_name = pin_a.signal.name
            if channel_name not in channels:
                channels[channel_name] = []
            channels[channel_name].append(pin_a.signal)
    
    return channels


def signal_compatible(bw: BreakoutWire, coupling: Coupling) -> Compatibility:
    """
    Determines if the breakout wire is compatible with the given coupling.
    
    Args:
        bw (BreakoutWire): The breakout wire to check.
        coupling (Coupling): The coupling to check against.
    
    Returns:
        Compatibility: An enum indicating the compatibility status.
    """
    bw_channnels = bw.get_channels()
    coupling_channels = coupling.get_channels()

    if bw.compatible_with_interface(coupling.interface):
        return Compatibility.COMPATIBLE
    else:
        return Compatibility.NO_MATCH
    
def connector_compatible(bw: BreakoutWire, coupling: Coupling, ignore_keying=False) -> Compatibility:
    """
    Determines if the breakout wire is compatible with the given connector.
    
    Args:
        bw (BreakoutWire): The breakout wire to check.
        connector (Connector): The connector to check against.
    
    Returns:
        Compatibility: An enum indicating the compatibility status.
    """
    if coupling.get_connection_hash(minified=True, minify_keying=ignore_keying) == bw.get_connection_hash(minified=True, minify_key=ignore_keying):
        return Compatibility.COMPATIBLE
    else:
        return Compatibility.NO_MATCH
