import unittest
from unittest.mock import patch
import sys
from io import StringIO
from biosynth.utils.input_utils import ArgumentParser, VERSION

class TestCommandLineParser(unittest.TestCase):
    def setUp(self):
        self.parser = ArgumentParser()

    def test_parse_all_arguments(self):
        sys.argv = ["test.py", "-p", "p_file.txt", "-s", "s_file.txt", "-c", "c_file.txt",
                    "-o", "out_dir", "-a", "2.0", "-b", "3.0", "-w", "200.0"]
        gui, s_file, p_file, c_file, o_file, alpha, beta, w = self.parser.parse_args(sys.argv[1:])
        self.assertEqual((gui, s_file, p_file, c_file, o_file, alpha, beta, w),
                         (False, "s_file.txt", "p_file.txt", "c_file.txt", "out_dir", 2.0, 3.0, 200.0))

    def test_parse_minimal_arguments(self):
        sys.argv = ["test.py", "-p", "p_file.txt", "-s", "s_file.txt", "-c", "c_file.txt"]
        gui, s_file, p_file, c_file, o_file, alpha, beta, w = self.parser.parse_args(sys.argv[1:])
        self.assertEqual((gui, s_file, p_file, c_file, o_file, alpha, beta, w),
                         (False, "s_file.txt", "p_file.txt", "c_file.txt", None, None, None, None))

    def test_gui_flag(self):
        sys.argv = ["test.py", "-g"]
        gui, s_file, p_file, c_file, o_file, alpha, beta, w = self.parser.parse_args(sys.argv[1:])
        self.assertTrue(gui)
        self.assertIsNone(s_file)
        self.assertIsNone(p_file)
        self.assertIsNone(c_file)
        self.assertIsNone(o_file)

    @patch('sys.exit')
    @patch('biosynth.utils.output_utils.Logger.help')
    def test_help_option(self, mock_logger_help, mock_exit):
        sys.argv = ["test.py", "-h"]
        self.parser.parse_args(sys.argv[1:])
        mock_exit.assert_called_with(1)
        self.assertTrue(mock_logger_help.called)

    @patch('sys.exit')
    @patch('biosynth.utils.output_utils.Logger.info')
    def test_version_option(self, mock_logger_info, mock_exit):
        sys.argv = ["test.py", "-v"]
        self.parser.parse_args(sys.argv[1:])
        mock_exit.assert_called_with(0)
        mock_logger_info.assert_called_with(f"BioSynth version {VERSION}")

    def test_float_arguments(self):
        sys.argv = ["test.py", "-p", "p_file.txt", "-s", "s_file.txt", "-c", "c_file.txt",
                    "-a", "1.5", "-b", "2.5", "-w", "50.0"]
        gui, s_file, p_file, c_file, o_file, alpha, beta, w = self.parser.parse_args(sys.argv[1:])
        self.assertEqual(alpha, 1.5)
        self.assertEqual(beta, 2.5)
        self.assertEqual(w, 50.0)

    def test_out_dir_argument(self):
        sys.argv = ["test.py", "-p", "p_file.txt", "-s", "s_file.txt", "-c", "c_file.txt",
                    "-o", "/tmp/output"]
        gui, s_file, p_file, c_file, o_file, alpha, beta, w = self.parser.parse_args(sys.argv[1:])
        self.assertEqual(o_file, "/tmp/output")

    @patch('sys.exit')
    @patch('biosynth.utils.output_utils.Logger.error')
    def test_invalid_argument(self, mock_logger_error, mock_exit):
        mock_exit.side_effect = SystemExit  # prevent the function from continuing
        sys.argv = ["test.py", "-x"]  # Invalid argument

        with self.assertRaises(SystemExit):
            self.parser.parse_args(sys.argv[1:])

        mock_logger_error.assert_called()  # Logger.error should be called
        mock_exit.assert_called_with(2)  # sys.exit should be called with 2


