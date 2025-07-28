from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Tuple
import re

# filepath: c:\Users\peter\OneDrive\Documents\Coding\bw\toolkit\src\el_analysis\utils\summarise_project_connectors.py
if TYPE_CHECKING:
    from el_analysis.core import Project
    from el_analysis.models.physical.interface import Interface


def _gather_connectors(project: Project) -> List[Interface]:
    """
    Gathers all connectors from all devices in the project.
    """
    all_interfaces = []
    for device in project.devices:
        for interface in device.interfaces:
            if interface.connector:
                all_interfaces.append(interface)
    return all_interfaces


def _build_data_rows(project: Project) -> Tuple[List[str], List[List[str]]]:
    """
    Builds header and data rows for connector summary table.
    """
    # Gather all interfaces with connectors
    interfaces_with_connectors = _gather_connectors(project)
    
    # Build header
    header = [
        "Interface Address",
        "Device Name",
        "Connector Part Number",
        "Connector Part Type",
        "Connected To"
    ]
    
    # Build data rows
    data_rows = []
    for interface in interfaces_with_connectors:
        row = [
            str(interface.address) if interface.address else "N/A",
            interface.device.name if interface.device else "N/A",
            interface.connector.part_number if interface.connector else "N/A",
            interface.connector.part_code if interface.connector else "N/A",
            f"{interface.connected_to.address}" if interface.connected_to else "N/A"
        ]
        data_rows.append(row)
    
    # Sort by interface address
    data_rows.sort(key=lambda x: x[0])
    
    return header, data_rows


def get_connector_summary(project: Project, do_print: bool = True) -> Tuple[List[str], List[List[str]]]:
    """
    Generates and optionally prints a summary of all connectors in the project.
    
    Args:
        project: The project to summarize
        do_print: Whether to print the summary
        
    Returns:
        A tuple of (header, data_rows)
    """
    header, data_rows = _build_data_rows(project)
    
    if do_print:
        # Pretty print as a table
        col_widths = [len(h) for h in header]
        for row in data_rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        def format_row(row):
            return " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))

        print(f"Connector Summary for {project.name}:")
        print(format_row(header))
        print("-+-".join("-" * w for w in col_widths))
        for row in data_rows:
            print(format_row(row))
            
    return header, data_rows