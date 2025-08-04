
from __future__ import annotations
from typing import TYPE_CHECKING, List, Union

from el_analysis.signal_toolkit.net import Net

class Channel:
    # A channel is really a mirror of SignalGroup, but whereas a SignalGroup is an abstraction, a Channel is a physical 
    # instantion of a group of nets that carry that signal between two specific points.

    def __init__(self, name: str):
        self.contents: List[Union[Net, Channel]] = []  # List of nets or channels
        self.awg = str

    def add_net(self, net: Net):
        self.contents.append(net)

    def add_channel(self, channel: Channel):
        self.contents.append(channel)

    def get_contents(self) -> List[Union[Net, Channel]]:
        return self.contents