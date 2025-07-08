from el_analysis import Address, Device, Project, get_connector_from_part_number
import os

input_filename = "sample_device.txt"
input_filename = os.path.join(os.path.dirname(__file__), "sample_device.txt")
# This input file should contain lines formatted as:
# "connector_address_string, part_number"
# Example: "+C.A2.X1, 123-456-789"


# We need 4 main functions:
# 1. Read data from input file
# 2. Extract Address and Connector information and from data
# 3. Format that data into a format that el_analysis can use
# 4. Add devices to the project


# 1 Read data from input file
def read_input_file(input_filename):
    """Reads the input file and returns its content."""
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"The input file {input_filename} does not exist.")
    
    with open(input_filename, 'r') as file:
        content = [line.rstrip('\n') for line in file]
    
    return content



def get_products_from_content(content):
    """Extracts product names from the content."""
    product_addresses = set()
    for line in content:
        tokens = line.split(",")
        if len(tokens) > 1:
            product_name = tokens[1].strip()
            product_addresses.add(product_name)

    products = []
    for product_address in product_addresses:
        print(f"Product Address: {product_address}")
        new_device = project.get_device_by_address(product_address, create_if_not_exists=True)

        products.append(new_device)
    # products = [project.add_device(product) for product in product_addresses]

    return products

# 2. Extract Address and Connector information from data
project = Project("Sample Project", default_location="C")
content = read_input_file(input_filename)
product_addresses = set()
cleaned_content = []
for content_line in content:
    tokens = content_line.split(",")
    try:
        connector_address_string = tokens[0]
        part_number = tokens[1]
    except IndexError:
        print(f"Skipping line due to IndexError: {content_line}")
        continue

    new_address = Address.from_string(connector_address_string)
    # print(f"New Address: {new_address}")
    
    cleaned_content.append([new_address, part_number])

# 3. Format that data into a format that el_analysis can use
# We cheat a little bit here, and create the devices directly from the cleaned content.
def generate_products(cleaned_content):
    products = []
    for address, part_number in cleaned_content:
        product = project.get_device_by_address(address, create_if_not_exists=True)
        if product:
            products.append(product)
    return products
products = generate_products(cleaned_content)

# 4. Add connectors to the project
def add_interfaces_to_products(cleaned_content):
    for address, part_number in cleaned_content:
        connector = get_connector_from_part_number(part_number)

        product = project.get_device_by_address(address)
        if product:
            new_interface = product.add_interface(address.interface, connector=connector)

            # print(f"Added interface {new_interface.name} to product {product.name}")

add_interfaces_to_products(cleaned_content)


project.summarize()


for device in project.devices:
    print(f"Device: {device.name}, Address: {device.address}")
    for interface in device.interfaces:
        print(f"  Interface: {interface.name}, Address: {interface.address}, Connector: {interface.connector.part_number if interface.connector else 'No connector assigned'}")
        # for pin in interface.pins:
        #     print(f"    Pin: {pin.name}, Address: {pin.address}")
