import unittest
from el_analysis import Interface, Device, Address

class TestInterface(unittest.TestCase):
    def setUp(self):
        class MockParent:
            address = Address(location="C", product="A2")
        self._parent = MockParent()
        self._expected_interface_address = Address(location="C", product="A2", interface="X1")

    def test_interface_initialization(self):
        interface = Interface("X1", parent=self._parent)
        self.assertIsNotNone(interface)
        self.assertEqual(interface.name, "X1")
        self.assertEqual(interface.address, self._expected_interface_address)
        self.assertEqual(interface.parent, self._parent)

    def test_interface_repr_and_device(self):
        device = Device("A2", parent=self._parent)
        interface = Interface("X1", parent=device)
        self.assertEqual(interface.device, device)

    def test_device_add_interface(self):
        device = Device("A2", parent=self._parent)
        interface = device.add_interface("X1")
        self.assertIsNotNone(interface)
        self.assertEqual(interface.name, "X1")
        self.assertIn("X1", device._interfaces)
        self.assertEqual(device._interfaces["X1"], interface)
        self.assertEqual(interface.parent, device)
        self.assertEqual(interface.address.product, device.name)

    def test_device_add_interface_and_add_pin(self):
        device = Device("A2", parent=self._parent)
        interface = device.add_interface("X1")
        self.assertIsNotNone(interface)
        pin = interface.add_pin("1")
        self.assertIsNotNone(pin)
        self.assertEqual(pin.name, "1")
        self.assertIn("1", interface._pins)
        self.assertEqual(interface._pins["1"], pin)
        self.assertEqual(pin.parent, interface)
        self.assertEqual(pin.address, interface.address.extend(pin="1"))

    def test_device_add_same_interface(self):
        device = Device("A2", parent=self._parent)
        interface1 = device.add_interface("X1")
        interface2 = device.add_interface("X1")
        self.assertIs(interface1, interface2)

    def test_interface_add_multiple_pins(self):
        interface = Interface("X1", parent=self._parent)
        pins = ["1", "2", "A", "B"]
        for pin_name in pins:
            pin_obj = interface.add_pin(pin_name)
            self.assertIsNotNone(pin_obj)
            self.assertEqual(pin_obj.name, pin_name)
            self.assertIn(pin_name, interface._pins)
            # Adding again returns the same object
            pin_obj2 = interface.add_pin(pin_name)
            self.assertEqual(pin_obj, pin_obj2)

    def test_interface_invalid_pin_name(self):
        interface = Interface("X1", parent=self._parent)
        with self.assertRaises(ValueError):
            interface.add_pin("")

    def test_interface_invalid_name(self):
        from el_analysis import config
        # Save and set config to not allow non-standard names
        old_validate = config.Interface.ValidateInterfaceName
        old_allow = config.Interface.AllowNonStandardInterfaceNames
        config.Interface.ValidateInterfaceName = True
        config.Interface.AllowNonStandardInterfaceNames = False
        try:
            with self.assertRaises(ValueError):
                Interface("BADNAME", parent=self._parent)
        finally:
            config.Interface.ValidateInterfaceName = old_validate
            config.Interface.AllowNonStandardInterfaceNames = old_allow

if __name__ == "__main__":
    unittest.main()