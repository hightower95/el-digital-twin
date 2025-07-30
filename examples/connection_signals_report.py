from sideload_connections import project


# We want to generate a summary of signals in the project. This is useful for BW analysis and also debugging

# We can filter by specific connections, or have a summary of all connections

# Report will look like:
#     From         To            From Part Code       Connection Hash      SignalHash           Pin 1                      Pin 2
#   +C+W11.X1   +C+A1.X1    <Connector_Part_code>    <Connection Hash>                    <Signal_name> :: AWG      <Signal_name> :: AWG
#   +C+W11.X1   +C+A1.X1    <Connector_Part_code>    <Connection Hash>                   <minified_signal> :: AWG  <minified_signal> :: AWG
#   +C+A1.X1   +C+W11.X1    <Connector_Part_code>    <Connection Hash>                   <minified_signal> :: AWG  <minified_signal> :: AWG
#   +C+A1.X1   +C+W11.X1    <Connector_Part_code>    <Connection Hash>                    <Signal_name> :: AWG      <Signal_name> :: AWG

# Pick a random interface with a connection to start with
interface_selected = None
for interface in project.interfaces:
    if interface.signal_count > 0:
        interface_selected = interface
        break

if interface_selected is None:
    raise ValueError("No interfaces with signals found in the project.")

for signal in interface_selected.signals:
    print(signal)
    # print(f"Signal: {signal.name} - {signal.minified_name} - {signal.awg}")


# We can get a basic summary of connections in the project by using project.create_connection_summary(), uncomment the line below to see the output
# project.create_connection_summary()


