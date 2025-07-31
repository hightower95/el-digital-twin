
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from el_analysis.core import Project
    from el_analysis.signal_toolkit.signal import Signal
    from el_analysis.models.physical.net import Net

from dataclasses import dataclass

@dataclass
class ReportDataRow:
    signal: Signal
    connections: Optional[List[Net]]


def _build_report_data(project: Project) -> List[ReportDataRow]:
    data_rows = []
    signals = {}
    for signal in project.signals:
        # we want to trace a path for each signal, connector to connector
        data_row = ReportDataRow(signal, list())

        for net in signal.connections:
            if data_row.connections is None:
                data_row.connections = []
            data_row.connections.append(net)

        data_rows.append(data_row)

    return data_rows

def _print_table(data_rows: List[ReportDataRow]):
    from tabulate import tabulate

    headers = ["Signal Name", "Signal Type", "Group", "Connections"]
    table = []

    for row in data_rows:
        connections = ", ".join(net.connection_id for net in row.connections) if row.connections else "None"
        table.append([row.signal.name, row.signal.signal_type, "", connections])

    print(tabulate(table, headers=headers, tablefmt="grid"))


def get_signal_summary(project: Project):
    """
    Summarizes the signals in the project by their names and the devices they are associated with.

    Args:
        project (Project): The project to summarize signals for.

    Returns:
        Dict[str, List[str]]: A dictionary where the keys are signal names and the values are lists of device names.
    """
    report_data = _build_report_data(project)

    _print_table(report_data)



