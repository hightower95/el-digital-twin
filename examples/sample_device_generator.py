
import random
from typing import Set
import os

output_filename = "sample_device.txt"
random.seed(output_filename)
output_filename = os.path.join(os.path.dirname(__file__), "sample_device.txt")

def generate_part_numbers(count=10) -> Set[str]:
    numbers = set()
    for x in range(0, count):
        number1 = random.randint(1000,9999)
        number2 = random.randint(100,999)

        numbers.add(f"1234 {number1}-{number2}")

    return numbers
generated_part_numbers = list(generate_part_numbers())

print(generated_part_numbers)


devices = [
    "A2",
    "A3",
    "A4",
    "A5",
    "A12",
    "A123",
    "B21",
    "A6",
    "KA2",
]

min_connectors = 1
max_connectors = 7

location = "C"


with open(output_filename, "w") as fp:
    for device in devices:
        print(device)

        connector_count = random.randint(min_connectors, max_connectors)

        for x in range(1, connector_count):

            chosen_part_number = random.choice(generated_part_numbers)

            fp.write(f"+{location}+{device}.X{x},{chosen_part_number}\n")





