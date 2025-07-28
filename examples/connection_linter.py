from sideload_connections import project
from el_analysis.models.physical.interface import Interface
from dataclasses import dataclass

from typing import List, Optional
from enum import Enum as enum
from el_analysis.models.physical.coupling import Coupling


class LinterLevels(enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

@dataclass
class LintResult:
    level: LinterLevels
    source: Interface
    message: str
    destination: Optional[Interface] = None
    connection_hash: Optional[str] = None


# def linter_warning(source: Interface, destination: Interface, message: str):


def lint_interface_connection(interface: Interface) -> LintResult:
    """
    Lint an interface to check for common issues.
    """
    if not interface.connector:
        return LintResult(
            level=LinterLevels.WARNING,
            source=interface,
            message="Interface has no connector defined."
        )

    if not interface.address:
        return LintResult(
            level=LinterLevels.ERROR,
            source=interface,
            message="Interface address is not defined."
        )

    # TODO: implement coupling
    connection = interface.coupling
    if not isinstance(connection, Coupling):
        return LintResult(
            level=LinterLevels.INFO,
            source=interface,
            message="Interface is not coupled to another interface."
        )
    
    if not isinstance(connection, Coupling):
        raise TypeError("Connection must be of type Coupling.")
    if not isinstance(connection.source, Interface) or not isinstance(connection.destination, Interface):
        raise TypeError("Both source and destination of the connection must be of type Interface.")
    source_connector = connection.source.connector
    destination_connector = connection.destination.connector

    if not source_connector or not destination_connector:
        return LintResult(
            level=LinterLevels.ERROR,
            source=interface,
            message="One or both connectors in the connection are not defined."
        )

    if not source_connector.compatible_with(destination_connector):
        return LintResult(
            level=LinterLevels.ERROR,
            source=interface,
            destination=connection.destination, # type:ignore
            connection_hash=connection.connection_hash,
            message=f"Connectors {source_connector.part_number} ({source_connector.part_code}) and {destination_connector.part_code} ({destination_connector.part_type}) are not compatible."
        )
    

    return LintResult(
        level=LinterLevels.INFO,
        source=interface,
        message=f"Interface linted successfully. Connector {source_connector.part_number} ({source_connector.part_code}) is compatible with {destination_connector.part_code} ({destination_connector.part_type}).",
    )


all_lint_results: List[LintResult] = []
for interface in project.interfaces:
    # todo we will end up checking the same interface multiple times if it has multiple connections
    # so we should probably only check each interface once, or check the connections instead
    result = lint_interface_connection(interface)
    if result:
        all_lint_results.append(result)


for lint_result in all_lint_results:
    print(f"{lint_result.level.value.upper()}: {lint_result.source.address} - {lint_result.message}")
    if lint_result.destination:
        print(f"  Connected to: {lint_result.destination.address}")
    if lint_result.connection_hash:
        print(f"  Connection Hash: {lint_result.connection_hash}")
    print("-" * 40)