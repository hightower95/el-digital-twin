
# from el_analysis.signal_toolkit.net import Net
from typing import List, Dict, Type

# I think that a channel is a good idea, particular effective when we have complicated electrical architectures that 
# (e.g. double twisted pairs, or twisting of pairs that are not typically twisted together)
# A channel gives us the ability to provide meta data to a SignalGroup that goes between two points.
# It also gives us the ability to fix issues when signals have note been allocated to a group signalgroup

# class Channel:
#     # A channel is really a mirror of SignalGroup, but whereas a SignalGroup is an abstraction, a Channel is a physical 
#     # instantion of a group of nets that carry that signal between two specific points.

#     def __init__(self, name: str):
#         self.contents: List[Net | 'Channel'] = []  # List of nets or channels
#         self.awg = str

#     def add_net(self, net: Net):
#         self.contents.append(net)

#     def add_channel(self, channel: 'Channel'):
#         self.contents.append(channel)

#     def get_contents(self) -> List[Net | 'Channel']:
#         return self.contents
    
# class ChannelManager:

#     def __init__(self):
#         # mapping SiganlGroup name to Channel
#         self.channels: Dict[str, Channel] = {}

#     def add_net(self, net: Net) -> Channel:
#         """
#         Add a net to the channel manager and return the channel it belongs to.
#         If the channel does not exist, create a new one.
#         """
#         signal = net.signal
#         signal_group = signal.signal_group if signal else None

#         channel = self.channels.get(signal_group.name) 
#         channel.associate_net(net)

#         channel_name = net.signal.name if net.signal else "default"
#         if channel_name not in self.channels:
#             self.channels[channel_name] = Channel(channel_name)
        
#         self.channels[channel_name].add_net(net)
#         return self.channels[channel_name]