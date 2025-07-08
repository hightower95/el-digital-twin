import el_analysis

from sideload_devices import project



# new_project = load_project_from_docs(short_name="project name",
#                                               device_list_filename=device_list_filename,
#                                               connection_list_filename=connection_list_filename,)



# We can generate a many different perspectives of the project

# Cable Summary
headers, data_rows = project.create_cable_summary()
print("Cable Summary:")
for row in data_rows:
    print(row)

# The output will look like this:
#  Cable Name |  X1 Part Number | X1 Part Type | Connects To |  X2 Part Number | X2 Part Type | Connects To
#  CW100      |  1234 123-123   |  Socket      | PDU_2.X1    |  124 123-124    |  Socket      | W99.X2

# Device Summary
headers, data_rows = project.create_device_summary()
print ("Device Summary:")
for row in data_rows:
    print(row)


# Connector Summary
headers, data_rows = project.create_interface_summary()
print ("Connector Summary:")
for row in data_rows:
    print(row)
# The output will look like this:
#  Connector Address |  Part Number  | Part Type | Connects To |  Signals
#   CW100.X1         |  1234 123-123 | Socket    | PDU_2.X1    |  Signal1, Signal2

# Connection Summary
# new_project.create_connection_summary()
# The output will look like this:
#   CW100.X1 - PDU_2.X1
#       A     Signal_Name   AWG_22 


# Signal summary
# new_project.create_signal_summary()


# There are specialized summaries to enable specific analysis tasks
# new_project.create_summary_for_bw_analysis(
#     connections =[("CW100.X1", "PDU.X1"),
#                   ("CW100.X2", "PDU.X2"),
#                   ("CW100.X3", "PDU.X3")]
# )