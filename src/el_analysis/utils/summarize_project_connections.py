
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from el_analysis.core import Project
    from el_analysis.models.physical.interface import Interface
    from el_analysis.connector_toolkit.connector import Connector
    from el_analysis import Address

from dataclasses import dataclass

def _gather_interfaces(project: Project) -> List[Interface]:
    all_interfaces = project.interfaces
    return all_interfaces

@dataclass(frozen=True)
class ReportDataRow:
    from_address: Address
    from_connector: Connector
    to_address: Optional[Address]
    to_connector: Optional[Connector]

_report_headers = [
    [
    "Connector 1", "", "", "",
    "Connector 2", "", "", "",
    "Connection"
    ],
    ["Address", "Part Number", "Part Type", "Signal Count", "Address", "Part Number", "Part Type", "Signal Count", "Connection Hash"],
]

def _build_data(interfaces):
    """
    Builds data rows for a summary of connections in the project.
    """
    data_rows = []
    for interface in interfaces:
        connected_interfaces = interface.connected_to

        row = [
            interface.address.address_string,
            interface.connector.part_number if interface.connector else None,
            interface.connector.part_code if interface.connector else None,
            interface.signal_count if interface else "",
        ]
        if connected_interfaces:
            row.extend([
                connected_interfaces.address.address_string,
                connected_interfaces.connector.part_number,
                connected_interfaces.connector.part_code,
                connected_interfaces.signal_count if connected_interfaces else "",
                interface.coupling.connection_hash if interface.coupling else None,
            ])
        else:
            row.extend([None, None, None, None])
        data_rows.append(row)
    return data_rows


def _print_table(data_rows: List[ReportDataRow]):
    """
    Builds a printable report from the data rows.
    """
    from tabulate import tabulate

    full_table = _report_headers + data_rows
    print(tabulate(full_table, tablefmt="grid", headers="")) # type:ignore


def get_connection_summary(project: Project) -> str:
    """
    Summarizes the connections in the given project.

    Args:
        project (Project): The project to summarize.

    Returns:
        str: A summary of the project's connections.
    """
    summary = []
    interfaces = _gather_interfaces(project)

    data_rows = _build_data(interfaces)

    _print_table(data_rows)
    return ""