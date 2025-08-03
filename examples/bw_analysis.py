from dataclasses import dataclass
from typing import List
from el_analysis import BWAnalysis

# @dataclass(frozen=True)
# class ProjectDocs:
#     short_name: str
#     device_list_filename: str
#     connection_list_filename: str
    
# C_project_docs = ProjectDocs(short_name="C", device_list_filename="device_list.txt", connection_list_filename="connection_list.txt")
# D_project_docs = ProjectDocs(short_name="D", device_list_filename="device_list_D.txt", connection_list_filename="connection_list_D.txt")

# project = Project("Project Name", default_location="C")

# project.load_from_device_list_file(C_project_docs.device_list_filename, default_location=C_project_docs.short_name)
# project.load_from_connection_list_file(C_project_docs.connection_list_filename, default_location=C_project_docs.short_name)

# project.load_from_device_list_file(D_project_docs.device_list_filename, default_location=D_project_docs.short_name)
# project.load_from_connection_list_file(D_project_docs.connection_list_filename, default_location=D_project_docs.short_name)

from sideload_connections import project

project.create_connection_summary()
project.create_device_summary()

connections = project.interfaces

# 1. Check pallitability

# There are specialized summaries to enable specific analysis tasks
new_project.create_summary_for_bw_analysis(
    connections =[("CW100.X1", "PDU.X1"),
                  ("CW100.X2", "PDU.X2"),
                  ("CW100.X3", "PDU.X3")]
)