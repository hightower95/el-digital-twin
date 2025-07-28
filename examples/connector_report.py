
from sideload_devices import project

"""In this example, we will explore the connectors used in the project."""


print("Connector Report")
print("=============")
# How many varieties of connectors do we have?

print(f"Total number of interfaces: {len(project.interfaces)}")
# project.create_interface_summary()

all_connectors = project.connectors
print(f"Total connector variants: {len(all_connectors)}")
print(f"All connectors: {all_connectors}")

# group by material
connectors_by_material = {}
for connector in all_connectors:
    material = connector.component.values.get("material", connector.part_type) if connector.component else "unknown"
    if not isinstance(material, str):
        material = str(material)
    existing_list = connectors_by_material.get(material, [])
    existing_list.append(connector)
    connectors_by_material[material] = existing_list


if False: # change to True to see the output
    print("Connectors grouped by material:")
    for material, connectors in connectors_by_material.items():
        print(f"Material: {material}, Count: {len(connectors)}")
        for connector in connectors:
            print(f"  - {connector.part_code} ({connector.part_number})")

# we might also want to group by Size:
connectors_by_size = {}
for connector in all_connectors:
    size = connector.component.values.get("size", connector.part_type) if connector.component else "unknown"
    if not isinstance(size, str):
        size = str(size)
    existing_list = connectors_by_size.get(size, [])
    existing_list.append(connector)
    connectors_by_size[size] = existing_list

if False: # change to True to see the output
    print("Connectors grouped by size:")
    for size, connectors in connectors_by_size.items():
        print(f"Size: {size}, Count: {len(connectors)}")
        for connector in connectors:
            print(f"  - {connector.part_code} ({connector.part_number})")

# If we exclude material information - maybe we decided that a certain material is no longer desirable. How many variants could we eliminate?

connectors_by_minified_part_code = {}
for connector in all_connectors:
    minified_code = connector.minified_part_code
    existing_list = connectors_by_minified_part_code.get(minified_code, [])
    existing_list.append(connector)
    connectors_by_minified_part_code[minified_code] = existing_list

print(f"There are {len(connectors_by_minified_part_code)} unique minified part codes - this is the minimum number of connector variants required when removing material as a factor ")

for minified_code, connectors in connectors_by_minified_part_code.items():
    print(f"Minified Part Code: {minified_code}, Count: {len(connectors)}")
    for connector in connectors:
        print(f"  - {connector.part_code} ({connector.part_number}), where used: {', '.join([str(use.address) for use in connector.used_in]) if connector.used_in else 'No uses'}")


# todo:
# project.connector_report - connectors, breakdown all factors 
# connector utilization