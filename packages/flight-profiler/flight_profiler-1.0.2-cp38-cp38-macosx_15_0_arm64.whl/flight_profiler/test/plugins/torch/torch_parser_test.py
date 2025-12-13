import unittest

from flight_profiler.plugins.torch.torch_parser import (
    TorchMemoryCommand,
    TorchProfileCommand,
    parse_torch_cmd,
)


class TorchParserTest(unittest.TestCase):

    def test_parse_profile_cmd(self):

        in_str = "profile __main__ hello"
        cmd: TorchProfileCommand = parse_torch_cmd(in_str)

        self.assertEqual(type(cmd), TorchProfileCommand)
        self.assertEqual("__main__", cmd.module_name)
        self.assertEqual("hello", cmd.method_name)
        self.assertIsNone(cmd.class_name)
        self.assertIsNotNone(cmd.filepath)

    def test_parse_memory_cmd(self):

        in_str = " memory -s"
        cmd: TorchMemoryCommand = parse_torch_cmd(in_str)

        self.assertEqual(type(cmd), TorchMemoryCommand)
        self.assertTrue(cmd.snapshot)
        self.assertIsNone(cmd.record)
        self.assertIsNotNone(cmd.filepath)
        self.assertTrue(cmd.filepath.endswith(".pickle"))

        in_str = "memory -r __main__ func"
        cmd: TorchMemoryCommand = parse_torch_cmd(in_str)

        self.assertEqual(type(cmd), TorchMemoryCommand)
        self.assertFalse(cmd.snapshot)
        self.assertEqual(cmd.module_name, "__main__")
        self.assertEqual(cmd.method_name, "func")
        self.assertIsNone(cmd.class_name)
        self.assertIsNotNone(cmd.filepath)

        in_str = "memory -r __main__ classA func"
        cmd: TorchMemoryCommand = parse_torch_cmd(in_str)

        self.assertEqual(type(cmd), TorchMemoryCommand)
        self.assertFalse(cmd.snapshot)
        self.assertEqual(cmd.module_name, "__main__")
        self.assertEqual(cmd.class_name, "classA")
        self.assertEqual(cmd.method_name, "func")
        self.assertIsNotNone(cmd.filepath)
