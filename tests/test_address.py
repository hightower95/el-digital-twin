import unittest
from el_analysis.core.address import Address

class TestAddress(unittest.TestCase):
    def setUp(self):
        self.addr_full = Address(location="C", product="A2", interface="X1", pin="13")
        self.addr_interface = Address(location="C", product="A2", interface="X1")
        self.addr_product = Address(location="C", product="A2")
        self.addr_location = Address(location="C")
        self.addr_empty = Address()

    def test_address_initialization(self):
        self.assertEqual(self.addr_full.location, "C")
        self.assertEqual(self.addr_full.product, "A2")
        self.assertEqual(self.addr_full.interface, "X1")
        self.assertEqual(self.addr_full.pin, "13")

    def test_address_as_tuple(self):
        self.assertEqual(self.addr_full.as_tuple(), ("C", "A2", "X1", "13"))
        self.assertEqual(self.addr_product.as_tuple(length=2), ("C", "A2", None, None))
        self.assertEqual(self.addr_location.as_tuple(length=1), ("C", None, None, None))
        with self.assertRaises(ValueError):
            self.addr_full.as_tuple(length=4)

    def test_address_repr(self):
        self.assertIsInstance(repr(self.addr_full), str)
        self.assertIn("13", repr(self.addr_full))

    def test_address_equality(self):
        addr_copy = Address(location="C", product="A2", interface="X1", pin="13")
        self.assertEqual(self.addr_full, addr_copy)
        self.assertNotEqual(self.addr_full, self.addr_interface)
        with self.assertRaises(TypeError):
            self.addr_full == "not an address"

    def test_address_is_properties(self):
        self.assertTrue(self.addr_location.is_location)
        self.assertTrue(self.addr_product.is_product)
        self.assertTrue(self.addr_interface.is_interface)
        self.assertTrue(self.addr_full.is_pin)
        self.assertFalse(self.addr_location.is_product)
        self.assertFalse(self.addr_product.is_interface)
        self.assertFalse(self.addr_interface.is_pin)

    def test_address_string_properties(self):
        self.assertIsInstance(self.addr_full.address_string, str)
        self.assertIsInstance(self.addr_full.pin_address_string, str)
        self.assertIsInstance(self.addr_full.interface_address_string, str)
        self.assertIsInstance(self.addr_full.product_address_string, str)
        self.assertIsInstance(self.addr_full.location_address_string, str)

    def test_address_from_string(self):
        addr = Address.from_string("C.A2.X1.13")
        self.assertEqual(addr, self.addr_full)
        addr2 = Address.from_string("C.A2")
        self.assertEqual(addr2, Address(location="C", product="A2"))
        addr3 = Address.from_string("C")
        self.assertEqual(addr3, Address(location="C"))
        addr4 = Address.from_string("C:A2:X1:13")
        self.assertEqual(addr4, self.addr_full)

    def test_address_from_tuple(self):
        t = ("C", "A2", "X1", "13")
        addr = Address.from_tuple(t)
        self.assertEqual(addr, self.addr_full)
        with self.assertRaises(ValueError):
            Address.from_tuple(("C", "A2", "X1"))

    def test_address_extend(self):
        addr = self.addr_location.extend(product="A2")
        self.assertEqual(addr, self.addr_product)
        addr2 = self.addr_product.extend(interface="X1")
        self.assertEqual(addr2, self.addr_interface)
        addr3 = self.addr_interface.extend(pin="13")
        self.assertEqual(addr3, self.addr_full)

    def test_address_union(self):
        addr1 = Address(location="C", product="A2")
        addr2 = Address(location="C", product="A2", interface="X1")
        union_addr = Address.union(addr1, addr2)
        self.assertEqual(union_addr, addr2)
        with self.assertRaises(ValueError):
            Address.union(Address(location="C"), Address(location="D"))

    def test_address_match_methods(self):
        addr1 = Address(location="C", product="A2", interface="X1", pin="13")
        addr2 = Address(location="C", product="A2", interface="X1", pin="14")
        addr3 = Address(location="C", product="A3", interface="X1")
        self.assertTrue(Address.location_match(addr1, addr2))
        self.assertTrue(Address.product_match(addr1, addr2))
        self.assertTrue(Address.interface_match(addr1, addr2))
        self.assertFalse(Address.pin_match(addr1, addr2))

        self.assertTrue(Address.location_match(addr1, addr3))
        self.assertFalse(Address.product_match(addr1, addr3))
        self.assertFalse(Address.interface_match(addr1, addr3))
        self.assertFalse(Address.pin_match(addr1, addr3))

    def test_address_invalid_init(self):
        with self.assertRaises(ValueError):
            Address(location="C", pin="13")
        with self.assertRaises(ValueError):
            Address(location="C", interface="X1")

    def test_address_empty_string(self):
        with self.assertRaises(ValueError):
            self.addr_empty.address_string

if __name__ == "__main__":
    unittest.main()