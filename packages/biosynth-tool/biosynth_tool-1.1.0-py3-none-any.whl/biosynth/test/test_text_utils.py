import unittest
from unittest.mock import patch, MagicMock
import sys

from biosynth.utils import text_utils
from biosynth.utils.text_utils import OutputFormat, set_output_format, format_text_bold_for_output, handle_critical_error

class TestOutputUtils(unittest.TestCase):

    def setUp(self):
        # Reset output_format before each test
        text_utils.output_format = OutputFormat.NONE

    def test_set_output_format_valid(self):
        set_output_format(OutputFormat.TERMINAL)
        self.assertEqual(text_utils.output_format, OutputFormat.TERMINAL)

        set_output_format(OutputFormat.GUI)
        self.assertEqual(text_utils.output_format, OutputFormat.GUI)

    def test_format_text_bold_for_output_terminal(self):
        text_utils.output_format = OutputFormat.TERMINAL
        result = format_text_bold_for_output("Hello")
        self.assertEqual(result, "\033[1mHello\033[0m")

    def test_format_text_bold_for_output_test(self):
        text_utils.output_format = OutputFormat.TEST
        result = format_text_bold_for_output("World")
        self.assertEqual(result, "\033[1mWorld\033[0m")

    def test_format_text_bold_for_output_gui(self):
        text_utils.output_format = OutputFormat.GUI
        result = format_text_bold_for_output("HelloGUI")
        self.assertEqual(result, "<b>HelloGUI</b>")

    def test_handle_critical_error_gui_raises(self):
        text_utils.output_format = OutputFormat.GUI
        with self.assertRaises(ValueError) as cm:
            handle_critical_error("Critical GUI Error")
        self.assertIn("Critical GUI Error", str(cm.exception))

    @patch.object(text_utils.Logger, "error")
    @patch.object(text_utils.Logger, "space")
    @patch("sys.exit")
    def test_handle_critical_error_terminal(self, mock_exit, mock_space, mock_error):
        text_utils.output_format = OutputFormat.TERMINAL
        handle_critical_error("Critical Terminal Error")
        mock_error.assert_called_once_with("Critical Terminal Error")
        mock_space.assert_called_once()
        mock_exit.assert_called_once_with(2)

    @patch("sys.exit")
    def test_handle_critical_error_none(self, mock_exit):
        text_utils.output_format = OutputFormat.NONE
        handle_critical_error("Critical None Error")
        mock_exit.assert_called_once_with(2)