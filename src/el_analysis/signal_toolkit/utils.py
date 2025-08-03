from el_analysis.signal_toolkit.signal import Signal, SignalGroup
from el_analysis.models.physical.pin import Pin
from el_analysis.signal_toolkit.net import Net
from typing import List, Dict

def group_signal_list_by_signal_type(signal_list: List[Signal]) -> Dict[str, List[Signal]]:
    # group by signal type and then group name
    grouped_signals = {}
    for signal in signal_list:
        signal_group = grouped_signals.setdefault(signal.signal_type, {})
        group_name = "unknown" if signal.signal_group is None else signal.signal_group.name
        signal_group.setdefault(group_name, []).append(signal)

    return grouped_signals

def net_list_to_channels(net_list: List[Net]) -> Dict[str, List[str]]:
    """
    Convert a list of nets into a dictionary of channels.
    Each channel is represented by its name and contains a list of signal names.
    """
    channels = {}
    for net in net_list:
        signal = net.signal
        if signal:
            channel_name = signal.name
            if channel_name not in channels:
                channels[channel_name] = []
            channels[channel_name].append(signal.name)
    
    return channels
