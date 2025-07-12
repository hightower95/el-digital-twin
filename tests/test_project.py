import unittest
from el_analysis import Interface, Device, Address, Pin, Project

class TestProject(unittest.TestCase):
    """Test cases for the Project class in el_analysis."""
    def setUp(self):
        pass

    def test_default_location(self):
        project = Project("test_project")
        self.assertIsNotNone(project.default_location)


    def test_create_by_address_device(self):

        new_address = Address(location="C", product="A2")
        new_project = Project("test_project")

        device = new_project.search_by_address(new_address, create_if_not_exists=False)
        self.assertIsNone(device)

        device = new_project.search_by_address(new_address, create_if_not_exists=True)

        self.assertIsNotNone(device)
        self.assertIsInstance(device, Device)
        if device is not None:
            self.assertEqual(device.address, new_address)
            self.assertEqual(device.name, "A2")

    def test_create_by_address_interface(self):

        new_address = Address(location="C", product="A2", interface="X1")
        new_project = Project("test_project")

        interface = new_project.search_by_address(new_address, create_if_not_exists=False)
        self.assertIsNone(interface)

        interface = new_project.search_by_address(new_address, create_if_not_exists=True)

        self.assertIsNotNone(interface)
        if interface is not None:
            self.assertIsInstance(interface, Interface)
            self.assertEqual(interface.address, new_address)
            self.assertEqual(interface.name, "X1")


    def test_create_by_address_pin(self):

        new_address = Address(location="C", product="A2", interface="X1", pin="1")
        new_project = Project("test_project")

        pin = new_project.search_by_address(new_address, create_if_not_exists=False)
        self.assertIsNone(pin)

        pin = new_project.search_by_address(new_address, create_if_not_exists=True)
        self.assertIsNotNone(pin)
        self.assertIsInstance(pin, Pin)
        if pin is not None:
            self.assertEqual(pin.address, new_address)
            self.assertEqual(pin.name, "1")


if __name__ == "__main__":
    unittest.main()