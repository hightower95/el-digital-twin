from el_analysis.signal_toolkit.signal import Signal
from typing import List, Dict

def group_signal_list_by_signal_type(signal_list: List[Signal]) -> Dict[str, List[Signal]]:
    # group by signal type and then group name
    grouped_signals = {}
    for signal in signal_list:
        signal_group = grouped_signals.setdefault(signal.signal_type, {})
        group_name = "unknown" if signal.signal_group is None else signal.signal_group.name
        signal_group.setdefault(group_name, []).append(signal)

    return grouped_signals