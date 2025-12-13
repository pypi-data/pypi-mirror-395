import unittest
from io import StringIO
import sys
from biosynth.utils.output_utils import Logger

class TestLogger(unittest.TestCase):

    def setUp(self):
        # Capture stdout
        self.held_stdout = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_stdout

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.original_stdout

    def get_output(self):
        return self.held_stdout.getvalue()

    def test_log_info(self):
        Logger.log("Test info message", "INFO")
        output = self.get_output()
        self.assertIn("Test info message", output)
        self.assertTrue(output.startswith(Logger.COLORS["INFO"]))
        self.assertTrue(output.endswith(Logger.COLORS["ENDC"] + "\n"))

    def test_error(self):
        Logger.error("Test error message")
        output = self.get_output()
        self.assertIn("Error: Test error message", output)
        self.assertTrue(output.startswith(Logger.COLORS["ERROR"]))
        self.assertTrue(output.endswith(Logger.COLORS["ENDC"] + "\n"))

    def test_warning_shortcut(self):
        Logger.warning("Test warning")
        output = self.get_output()
        self.assertIn("Test warning", output)
        self.assertTrue(output.startswith(Logger.COLORS["WARNING"]))

    def test_debug_shortcut(self):
        Logger.debug("Debug message")
        output = self.get_output()
        self.assertIn("Debug message", output)
        self.assertTrue(output.startswith(Logger.COLORS["DEBUG"]))

    def test_notice_shortcut(self):
        Logger.notice("Notice message")
        output = self.get_output()
        self.assertIn("Notice message", output)
        self.assertTrue(output.startswith(Logger.COLORS["NOTICE"]))

    def test_critical_shortcut(self):
        Logger.critical("Critical message")
        output = self.get_output()
        self.assertIn("Critical message", output)
        self.assertTrue(output.startswith(Logger.COLORS["CRITICAL"]))

    def test_space(self):
        Logger.space()
        output = self.get_output()
        # It should just print an empty line
        self.assertEqual(output, f"{Logger.COLORS['INFO']}{Logger.COLORS['ENDC']}\n")

    def test_get_formated_text_wraps(self):
        long_text = "a" * 100
        wrapped = Logger.get_formated_text(long_text)
        self.assertTrue(all(len(line) <= Logger.MAX_WIDTH for line in wrapped.splitlines()))
