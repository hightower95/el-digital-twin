from __future__ import annotations
from typing import TYPE_CHECKING, Optional

# from el_analysis.signal_toolkit.net import Net
if TYPE_CHECKING:
    from typing import List, Dict, Type, Union
    from el_analysis.models.physical.addressable import Addressable
    from el_analysis.signal_toolkit.net import Net

# I think that a channel is a good idea, particular effective when we have complicated electrical architectures that 
# (e.g. double twisted pairs, or twisting of pairs that are not typically twisted together)
# A channel gives us the ability to provide meta data to a SignalGroup that goes between two points.
# It also gives us the ability to fix issues when signals have note been allocated to a group signalgroup


# The logic is this:
# Channel Manager - Maps Destination to Channels
# Pipe - Maps Signal Type to Channel. A pipe is a collection of channels that go to a specific destination.
# Channels - Maps Signal Name to a list of nets
# Channel - Maps Signal Group Name to a list of nets

class Channel:
    # Represents a single channel for a specific signal type
    def __init__(self, signal_type: str, name: str):
        self.signal_type = signal_type
        self.name = name
        self.nets: List[Net] = []  # Maps signal name to list of nets

    def add_net(self, net: Net):
        if net not in self.nets:
            self.nets.append(net)

class Channels:
    # A channel is really a mirror of SignalGroup, but whereas a SignalGroup is an abstraction, a Channel is a physical 
    # instantion of a group of nets that carry that signal between two specific points.

    def __init__(self, signal_type: str):
        self.channel_map: Dict[str, Channel] = {}  # Maps signal name to list of nets
        self.signal_type = signal_type

    def add_net(self, net: Net):
        channel = self.channel_map.setdefault(net.signal.name, Channel(self.signal_type, net.signal.name))
        channel.add_net(net)

class Pipe:
    """
    Represents a destination for a channel, which can be an Addressable object.
    This is used to manage channels that may have multiple destinations.
    """

    def __init__(self, start: Addressable, end: Addressable):
        self.start = start
        self.end = end
        self.channels: Dict[str, Channels] = {}  # Maps signal type to Channel object

    def add_net(self, net: Net) -> Channels:
        """
        Add a net to the channel manager and return the channel it belongs to.
        If the channel does not exist, create a new one.
        """

        signal = net.signal
        signal_group = signal.signal_group if signal else None

        if signal_group is None:
            raise ValueError(f"Net {net.net_id} does not have an associated signal group. Unable to initiate channel")

        channel = self.channels.setdefault(signal_group.signal_type, Channels(signal_group.signal_type))
        channel.add_net(net)

        # channel_name = net.signal.name if net.signal else "default"
        # if channel_name not in self.channels:
        #     self.channels[channel_name] = Channels(channel_name)
        
        # self.channels[channel_name].add_net(net)
        return channel

class ChannelManager:

    def __init__(self, start: Addressable):
        # key is the destination address, value is a Channels object
        self.pipes: Dict[str, Pipe] = {}
        self.start: Addressable = start

    def _get_destination(self, net: Net) -> Addressable:
        if net.source.address.interface_address == self.start.address.interface_address:
            return net.destination
        elif net.destination.address.interface_address == self.start.address.interface_address:
            return net.source
        else:
            raise ValueError(f"Net {net.net_id} is not compatible with ChannelManager for start address {self.start.address}.")

    def add_net(self, net: Net) -> Channels:
        """
        Add a net to the channel manager and return the channel it belongs to.
        If the channel does not exist, create a new one.
        """
        # first select the correct Channels based on the net destination
        destination = self._get_destination(net)
        channels = self.pipes.setdefault(destination.address.interface_address_string, Pipe(self.start, destination))

        return channels.add_net(net)
    
    def print_summary(self):
        """
        Print a summary of the channels managed by this ChannelManager.
        """
        print(f"ChannelManager for {self.start.address.address_string} has {len(self.pipes)} pipes:")
        for destination, pipe in self.pipes.items():
            print(f"  Destination: {destination}, Channels: {len(pipe.channels)}")
            for signal_type, channels in pipe.channels.items():

                print(f"    Signal Type: {signal_type}, Nets: {len(channels.channel_map)}, Net Groups: {[[net.signal.name for net in net_group.nets] for net_group in channels.channel_map.values()]}")
