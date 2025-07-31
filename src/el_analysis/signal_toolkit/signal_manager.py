
from typing import Optional, List, Dict
from el_analysis.signal_toolkit.signal import Signal, SignalParserBase, SignalGroup
from .signal_parsers import _SIGNAL_PARSERS
from el_analysis.signal_toolkit.signal_parsers.base import DefaultSignalGroupParser, DefaultSignalGroup
from el_analysis import logging
# All signals exist within a group. That group may be a single signal, or a group of signals that are related.



class SignalManager:
    def __init__(self):
        # signal name -> Signal object
        self._signals: Dict[str, Signal] = {}
        self.signal_groups: Dict[str, List[SignalGroup]] = {}

    def _identify_parser(self, signal_name: str) -> type[SignalParserBase]:
        """
        Identify the appropriate parser for the signal based on its name.
        If no specific parser is found, use the default parser.
        """
        selected_parser: Optional[SignalParserBase] = None
        for parser in _SIGNAL_PARSERS:
            if parser.can_parse(signal_name):
                return parser
        
        # If no specific parser found, use the default parser
        return DefaultSignalGroupParser

    def add_signal(self, signal_name, awg) -> Optional[Signal]:

        # When we create a signal, we are also interested in the group it belongs to.
        # So whilst we return a signal, behind the scenes we are also managing the signal group

        # Does the signal already exist?
        if signal_name in self._signals:
            return self._signals[signal_name]

        # Find Parser
        signal_parser = self._identify_parser(signal_name)
        logging.debug(f"Identified parser '{signal_parser.__name__}' for signal '{signal_name}'")

        # Build signal object
        signal_type = signal_parser.signal_type
        _signal = signal_parser.parse_signal(signal_name)


        # Now lets assign it to an existing signal group
        signal_group: Optional[SignalGroup] = None
        same_type_signal_groups = self.signal_groups.get(signal_type, [])
        if not same_type_signal_groups:
            # If no groups available, create a new one
            signal_group = signal_parser.new_signal_group(_signal)
            self.signal_groups[signal_type] = [signal_group]
            logging.debug(f"First signal parsed for signal type '{signal_type}' with signal '{_signal.name}'")
        else:
            # If groups are available, check if the signal can be added to an existing group
            for group in same_type_signal_groups:
                if group.add_signal(_signal):
                    if _signal.signal_group is None:
                        raise ValueError(f"Signal group for {_signal.name} is None after adding to group {group.name}, group type: {group.signal_type}")
                    logging.debug(f"Added signal '{_signal.name}' to existing group '{group.name}'")
                    break
            else:
                # If the signal cannot be added, create a new group
                signal_group = signal_parser.new_signal_group(_signal)
                same_type_signal_groups.append(signal_group)
                self.signal_groups[signal_type] = same_type_signal_groups
                logging.debug(f"Created new signal group for type '{signal_type}' with signal '{_signal.name}'")

        self._signals[signal_name] = _signal
        return _signal

    def get_signal(self, signal_name) -> Optional[Signal]:
        signal_data = self._signals.get(signal_name, None)
        return signal_data

    def list_signals(self):
        return list(self._signals.keys())