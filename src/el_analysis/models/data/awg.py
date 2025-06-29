from enum import Enum

class AWG(Enum):
    """Enum for American Wire Gauge (AWG) sizes."""
    AWG_0000 = 0
    AWG_000 = 1
    AWG_00 = 2
    AWG_0 = 3
    AWG_1 = 4
    AWG_2 = 5
    AWG_3 = 6
    AWG_4 = 7
    AWG_5 = 8
    AWG_6 = 9
    AWG_7 = 10
    AWG_8 = 11
    AWG_9 = 12
    AWG_10 = 13
    AWG_11 = 14
    AWG_12 = 15
    AWG_13 = 16
    AWG_14 = 17
    AWG_15 = 18
    AWG_16 = 19
    AWG_17 = 20
    AWG_18 = 21
    AWG_19 = 22
    AWG_20 = 23
    AWG_21 = 24
    AWG_22 = 25
    AWG_23 = 26
    AWG_24 = 27
    AWG_25 = 28
    AWG_26 = 29


if __name__ == "__main__":
    # Example usage
    print(AWG.AWG_10)  # Output: AWG_10
    print(AWG.AWG_10.value)  # Output: 10
    print(AWG.AWG_10.name)  # Output: AWG_10
    print(list(AWG))  # Output: List of all AWG sizes
    print(AWG.AWG_10 in AWG)  # Output: True