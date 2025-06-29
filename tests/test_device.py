import unittest
from el_analysis import Device, Address

# todo disable logging for tests

class TestDevice(unittest.TestCase):
    def setUp(self):
        
        class MockParent:
            address = Address(location="C")
        
        self._expected_device_address = Address(location="C", product="A2")
        self._parent = MockParent()
        # self.device = Device(name="TestDevice", id=1)

    def test_device_initialization(self):
        device = Device("A2", parent=self._parent)
        self.assertIsNotNone(device)
        self.assertEqual(device.address, self._expected_device_address)

    def test_device_name(self):
        device = Device("A2", parent=self._parent)
        self.assertEqual(device.name, "A2")
        self.assertEqual(device.long_name, None)

    def test_device_long_name(self):
        device = Device("A2", parent=self._parent, long_name="Interface Unit")
        self.assertEqual(device.long_name, "Interface Unit")

    def test_device_repr(self):
        device = Device("A2", parent=self._parent)
        self.assertIn("A2", repr(device))

    # def test_device_equality(self):
    #     device1 = Device("A2", parent=self._parent)
    #     device1_2 = Device("A2", parent=self._parent)
    #     device2 = Device("A3", parent=self._parent)
        
    #     self.assertEqual(device1, device1_2)
    #     self.assertNotEqual(device1, device2)

    def test_device_add_standard_interface(self):
        device = Device("A2", parent=self._parent)
        interface_obj = device.add_interface("X1")
        self.assertIsNotNone(interface_obj)
        self.assertEqual(interface_obj.name, "X1")

    def test_device_add_multiple_standard_interfaces(self):
        interfaces = [
            "X1",
            "X2",
            "X303",
            "X40",
        ]
        device = Device("A2", parent=self._parent)
        for interface_name in interfaces:
            interface_obj = device.add_interface(interface_name)
            self.assertIsNotNone(interface_obj)

            interface_obj_2 = device.add_interface(interface_name)
            self.assertIsNotNone(interface_obj_2)
            self.assertEqual(interface_obj, interface_obj_2)

            self.assertIn(interface_name, device.list_interfaces())

        self.assertEqual(len(interfaces), device.interfaceCount)

    

if __name__ == "__main__":
    unittest.main()