from __future__ import annotations
from typing import TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from el_analysis.core import Project
import csv
from io import StringIO
import re


def _summarize_interfaces(cables):
    all_interfaces = set([interface.name for cable in cables for interface in cable.interfaces])

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


def _build_data_rows(project: Project ):
    """
    Prints a summary of cables in the project.
    """
    print(f"Cable Summary for {project.name}:")
    # Prepare header dynamically based on the maximum number of interfaces found
    cables = [c for c in project.devices if c.is_cable]

    all_interfaces = _summarize_interfaces(cables)

    # Build header
    header = ["Cable Name"]
    
    row_headers = []
    interface_header_mapping: Dict[str, int] = {}
    for i, interface in enumerate(all_interfaces, start=0):
        row_headers.append(f"{interface} - Part Number")
        row_headers.append(f"{interface} - Part Type")
        row_headers.append(f"{interface} - Connects To")
        interface_header_mapping[interface] = i * 3

    all_data_rows = []
    for cable in cables:
        data_row = [""] * (len(row_headers) + 1)  # +1 for Cable Name
        data_row[0] = cable.name
        for interface in cable.interfaces:
            index = interface_header_mapping.get(interface.name, None)
            if index is None:
                raise ValueError(f"Interface {interface.name} not found in header mapping.")

            data_row[index + 1] = "N/A"
            data_row[index + 2] = "N/A"
            if interface.connector is not None:
                if interface.connector.part_number:
                    data_row[index + 1] = interface.connector.part_number

                if interface.connector.part_type:
                    data_row[index + 2] = interface.connector.part_type

        all_data_rows.append(data_row)

    # print(all_data_rows)

    header.extend(row_headers)
    return header, all_data_rows

def get_cable_summary(project: Project, do_print: bool = True):

    header, data_rows = _build_data_rows(project)
    # Pretty print as a table
    col_widths = [len(h) for h in header]
    for row in data_rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def format_row(row):
        return " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))

    print(format_row(header))
    print("-+-".join("-" * w for w in col_widths))
    for row in data_rows:
        print(format_row(row))
    return _build_data_rows(project)
