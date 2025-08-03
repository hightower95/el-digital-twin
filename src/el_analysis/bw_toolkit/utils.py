from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
if TYPE_CHECKING:
    from el_analysis.models import Interface

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