from el_analysis.signal_toolkit.signal import SignalGroup, Signal, SignalParserBase
from typing import Type, Dict
from el_analysis import logging

class DefaultSignalGroup(SignalGroup):
    """
    Default signal group that does nothing.
    This is used when no specific group is available for a signal.
    """
    
    def __init__(self, signal: Signal):
        super().__init__()
        self.add_signal(signal)

    @property
    def name(self) -> str:
        # if len(self.signals) == 1:
        #     return self.signals[0].name
        # else:
        #     return str(id(self))
        return str(id(self))
    
    @property
    def signal_count(self) -> int:
        """
        The number of signals in the group.
        """
        return len(self.signals)

    def add_signal(self, signal: Signal) -> bool:
        if signal.signal_type != self.signal_type:
            raise ValueError(f"Signal type '{signal.signal_type}' does not match group type '{self.signal_type}'")

        if len(self.signals) == 0:
            logging.debug(f"Setting signal type to {self.signal_type} for the first signal in the group.")
            self.signals.append(signal)
            signal.signal_group = self
            return True
        

        return False



class DefaultSignalGroupParser(SignalParserBase):
    """
    Default signal group that does nothing.
    This is used when no specific group is available for a signal.
    """
    signal_group = DefaultSignalGroup
    signal_type: str = signal_group.signal_type

    @staticmethod
    def parse_signal(signal_name: str) -> Signal:
        """
        Parse the signal and return it as is.
        
        Args:
            signal (str): The signal to parse.
        
        Returns:
            str: The original signal.
        """
        signal = Signal(signal_name)
        return signal

    @staticmethod
    def can_parse(signal_name: str) -> bool:
        """
        Always returns True as this is the default fallback parser.
        
        Args:
            signal_name (str): The name of the signal to check.
        
        Returns:
            bool: Always True.
        """
        return True
    
    @staticmethod
    def new_signal_group(signal: Signal) -> DefaultSignalGroup:
        """
        Create a new default signal group with the given signal.
        
        Args:
            signal (Signal): The signal to add to the group.
        
        Returns:
            DefaultSignalGroup: A new default signal group containing the signal.
        """
        return DefaultSignalGroup(signal)