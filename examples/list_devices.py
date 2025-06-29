from el_analysis import Address, Device, Project, get_connector_by_part_number
import os

input_filename = "sample_device.txt"
input_filename = os.path.join(os.path.dirname(__file__), "sample_device.txt")
with open(input_filename, 'r') as file:
    content = [line.rstrip('\n') for line in file]
    print(content)

project = Project("Sample Project", default_location="C")

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



# 1 read connector address strings, part numbers from file
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
    print(f"New Address: {new_address}")
    
    cleaned_content.append([new_address, part_number])

# 2 generate products
def generate_products(cleaned_content):
    products = []
    for address, part_number in cleaned_content:
        product = project.get_device_by_address(address, create_if_not_exists=True)
        if product:
            products.append(product)
    return products
products = generate_products(cleaned_content)

# 3 add interfaces


def add_interfaces_to_products(cleaned_content):
    for address, part_number in cleaned_content:
        connector = get_connector_by_part_number(part_number)

        product = project.get_device_by_address(address)
        if product:
            new_interface = product.add_interface(address.interface, connector=connector)

            print(f"Added interface {new_interface.address} to product {product.name}")

add_interfaces_to_products(cleaned_content)