
from el_analysis.bw_toolkit.breakout_wire import BreakoutWire
from typing import List
from el_analysis.models.physical.coupling import Coupling

class BWAnalysis:

    def __init__(self, project):
        self.breakout_wires: List[BreakoutWire] = []

    def create_breakout_wires(self, couplings: List[Coupling], allow_merging: bool = False):
        """
        Creates breakout wires for the given couplings.
        
        Args:
            couplings (List[Coupling]): List of couplings to create breakout wires for.
        """
        for coupling in couplings:
            wire = BreakoutWire.from_coupling(coupling)
            self.breakout_wires.append(wire)
            print(f"Created BreakoutWire: {wire.name} with ID: {wire.connection_id}")

    def import_breakout_wires(self, filename: str):
        """
        Imports breakout wires into the analysis.
        
        Args:
            filename (str): The name of the file to import breakout wires from.
        """
        raise NotImplementedError("Import functionality is not implemented yet.")


