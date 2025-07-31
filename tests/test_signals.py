# 1 Create a new project, load one example interface 

# several signals, expected output and their minified name.
# AWG20, +28V Power - Signal Name: +28 Power, AWG: AWG20, Minified Name: +28V Power_AWG20

import unittest
from el_analysis import Interface, Device, Address, Pin, Project

class TestSignals(unittest.TestCase):
    def setUp(self):
        self.project = Project("test_project")

    def test_signal_class(self):
        from el_analysis.signal_toolkit.signal import Signal
        signal_name = "+28 Power"
        awg = "AWG20"
        minified_name = "+28 Power_AWG20"

        # Simulate adding a signal
        signal = Signal(signal_name, awg=awg)

        # Check if the signal was created correctly
        self.assertIsNotNone(signal)
        self.assertEqual(signal.name, signal_name)
        self.assertEqual(signal.awg, awg)
        self.assertEqual(signal.minified_name, minified_name)

    def test_signal_manager_identify_parser(self):
        from el_analysis.signal_toolkit.signal_manager import SignalManager
        from el_analysis.signal_toolkit.signal_parsers.base import DefaultSignalGroupParser
        manager = SignalManager()

        parser = manager._identify_parser("+28 Power")
        self.assertIsNotNone(parser)
        self.assertEqual(parser, DefaultSignalGroupParser)
        self.assertTrue(parser.can_parse("+28 Power"))
        self.assertEqual(parser.signal_type, "default")

    def test_default_signal_group_parser(self):
        from el_analysis.signal_toolkit.signal_parsers.base import DefaultSignalGroupParser, DefaultSignalGroup
        parser = DefaultSignalGroupParser()

        signal_name = "+28 Power"
        signal = parser.parse_signal(signal_name)
        signal_group = signal.signal_group

        self.assertIsNone(signal_group)
        self.assertEqual(signal.name, signal_name)
        self.assertTrue(parser.can_parse(signal_name))
        self.assertEqual(signal.signal_type, DefaultSignalGroup.signal_type)

    def test_signal_manager_add_default_signal(self):
        from el_analysis.signal_toolkit.signal_manager import SignalManager
        manager = SignalManager()

        signal_name = "+28 Power"
        awg = "AWG20"

        # Add the signal to the manager
        signal = manager.add_signal(signal_name, awg)

        # Check if the signal was added correctly
        self.assertIsNotNone(signal)
        if not signal:
            self.fail("Signal should not be None")
        self.assertEqual(signal.name, signal_name)
        self.assertTrue(hasattr(signal, 'signal_group'))
        self.assertIsNotNone(signal.signal_group)
        if not signal.signal_group:
            self.fail("Signal group should not be None")
        self.assertEqual(signal.signal_group.signal_count, 1)

    def test_signal_manager_add_multiple_default_signals(self):
        from el_analysis.signal_toolkit.signal_manager import SignalManager
        manager = SignalManager()

        signals = [
            ("+28 Power", "AWG20"),
            ("-12 Power", "AWG21"),
            ("Signal A", "AWG22")
        ]

        object_ids = []
        for signal_name, awg in signals:
            signal = manager.add_signal(signal_name, awg)
            self.assertIsNotNone(signal)
            if not signal:
                self.fail(f"Signal {signal_name} should not be None")
            self.assertEqual(signal.name, signal_name)
            self.assertTrue(hasattr(signal, 'signal_group'))
            self.assertIsNotNone(signal.signal_group)
            if not signal.signal_group:
                self.fail("Signal group should not be None")
            self.assertEqual(signal.signal_group.signal_count, 1)
            object_ids.append(id(signal))

        # Check if all object IDs are unique
        self.assertEqual(len(object_ids), len(set(object_ids)))

    def test_add_signal_with_same_name(self):
        from el_analysis.signal_toolkit.signal_manager import SignalManager
        manager = SignalManager()

        signal_name = "+28 Power"
        awg = "AWG20"

        # Add the signal to the manager
        signal1 = manager.add_signal(signal_name, awg)
        self.assertIsNotNone(signal1)

        # Add the same signal again
        signal2 = manager.add_signal(signal_name, awg)
        self.assertIsNotNone(signal2)

        # Check if both signals are the same instance
        self.assertIs(signal1, signal2)

    def test_signal_manager_get_signal(self):
        from el_analysis.signal_toolkit.signal_manager import SignalManager
        manager = SignalManager()

        signal_name = "+28 Power"
        awg = "AWG20"

        # Add the signal to the manager
        signal = manager.add_signal(signal_name, awg)

        # Retrieve the signal
        retrieved_signal = manager.get_signal(signal_name)

        # Check if the retrieved signal matches the original
        self.assertIsNotNone(retrieved_signal)
        self.assertEqual(retrieved_signal.name, signal_name)

    