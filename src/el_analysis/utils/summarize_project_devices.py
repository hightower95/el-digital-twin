from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List
import csv
from io import StringIO
import re

# filepath: c:\Users\peter\OneDrive\Documents\Coding\bw\toolkit\src\el_analysis\utils\summarize_project_devices.py
if TYPE_CHECKING:
    from el_analysis.core import Project


def _summarize_interfaces(devices):
    all_interfaces = set([interface.name for device in devices for interface in device.interfaces])

    # Sort interfaces first by the letter prefix, then by the numeric part
    def interface_sort_key(name):
        match = re.match(r"([A-Za-z]+)(\d+)", name)
        if match:
            letter, number = match.groups()
            return (letter, int(number))
        else:
            return (name, 0)
    all_interfaces = sorted(all_interfaces, key=interface_sort_key)

    return all_interfaces


def _build_data_rows(project: Project):
    """
    Builds data rows for a summary of devices in the project.
    """
    print(f"Device Summary for {project.name}:")
    # Get all non-cable devices
    devices = [d for d in project.devices if not d.is_cable]

    all_interfaces = _summarize_interfaces(devices)

    # Build header
    header = ["Device Name", ]
    
    row_headers = []
    interface_header_mapping: Dict[str, int] = {}
    for i, interface in enumerate(all_interfaces, start=0):
        row_headers.append(f"{interface} - Part Number")
        row_headers.append(f"{interface} - Part Type")
        row_headers.append(f"{interface} - Connects To")
        interface_header_mapping[interface] = i * 3

    header.extend(row_headers)
    
    all_data_rows = []
    for device in devices:
        data_row = [""] * (len(row_headers) + 3)  # +3 for Device Name, Part Number, Part Type
        data_row[0] = device.name
        
        for interface in device.interfaces:
            index = interface_header_mapping.get(interface.name, None)
            if index is None:
                raise ValueError(f"Interface {interface.name} not found in header mapping.")

            data_row[index + 1] = interface.connector.part_number if interface.connector else "N/A"
            data_row[index + 2] = interface.connector.part_type if interface.connector else "N/A"
            # data_row[index + 5] = interface.address.interface.device.name if interface.address and interface.address.interface else "N/A"
        # 
        all_data_rows.append(data_row)
    header.extend(row_headers)
    return header, all_data_rows


def get_device_summary(project: Project, do_print: bool = True):
    """
    Creates a summary of devices in the project.
    """
    header, data_rows = _build_data_rows(project)
    
    # Pretty print as a table
    col_widths = [len(h) for h in header]
    for row in data_rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def format_row(row):
        return " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))

    if do_print:
        print(format_row(header))
        print("-+-".join("-" * w for w in col_widths))
        for row in data_rows:
            print(format_row(row))
    
    return header, data_rows