import unittest
import tempfile
import os
import sys
from pathlib import Path
from io import StringIO
from unittest.mock import patch, mock_open

from biosynth.utils.file_utils import (
    read_codon_freq_file, FileDataReader,
    SequenceReader, PatternReader, CodonUsageReader,
    create_dir, delete_dir, save_file, resource_path
)

class TestReadCodonFreqFile(unittest.TestCase):
    def test_valid_lines_with_dna_conversion(self):
        raw_lines = ["AUG 0.5", "UUU 1.0"]
        result = read_codon_freq_file(raw_lines, convert_to_dna=True)
        self.assertEqual(result, {"ATG": 0.5, "TTT": 1.0})

    def test_valid_lines_without_conversion(self):
        raw_lines = ["AUG 0.5"]
        result = read_codon_freq_file(raw_lines, convert_to_dna=False)
        self.assertEqual(result, {"AUG": 0.5})

    def test_invalid_format_line(self):
        raw_lines = ["AUG"]  # missing frequency
        with self.assertRaises(SystemExit) as cm:
            read_codon_freq_file(raw_lines)
        self.assertEqual(cm.exception.code, 2)

    def test_invalid_frequency_value(self):
        raw_lines = ["AUG not_a_number"]
        with self.assertRaises(SystemExit) as cm:
            read_codon_freq_file(raw_lines)
        self.assertEqual(cm.exception.code, 2)

    def test_invalid_codon_length(self):
        raw_lines = ["ATGC 0.2"]  # 4 letters, invalid
        with self.assertRaises(SystemExit) as cm:
            read_codon_freq_file(raw_lines)
        self.assertEqual(cm.exception.code, 2)

    def test_invalid_codon_characters(self):
        raw_lines = ["AXG 0.1"]  # X is not valid base
        with self.assertRaises(SystemExit) as cm:
            read_codon_freq_file(raw_lines)
        self.assertEqual(cm.exception.code, 2)


class TestFileDataReader(unittest.TestCase):
    def test_read_lines_success(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write("line1\nline2\n")
            tmp_path = tmp.name
        reader = FileDataReader(tmp_path)
        lines = reader.read_lines()
        self.assertEqual(lines, ["line1\n", "line2\n"])
        os.remove(tmp_path)

class TestSequenceReader(unittest.TestCase):
    def test_read_sequence_success(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write("\n\nACTG\n")
            tmp_path = tmp.name
        reader = SequenceReader(tmp_path)
        seq = reader.read_sequence()
        self.assertEqual(seq, "ACTG")
        os.remove(tmp_path)

    def test_read_sequence_file_not_set(self):
        reader = SequenceReader(None)
        with self.assertRaises(SystemExit) as cm:
            reader.read_sequence()
        self.assertEqual(cm.exception.code, 2)

    def test_read_sequence_empty(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write("\n\n")
            tmp_path = tmp.name
        reader = SequenceReader(tmp_path)
        with self.assertRaises(SystemExit) as cm:
            reader.read_sequence()
        self.assertEqual(cm.exception.code, 2)
        os.remove(tmp_path)

    def test_read_sequence_multiple_lines(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write("\nACTG\nTGCA\n")
            tmp_path = tmp.name
        reader = SequenceReader(tmp_path)
        with self.assertRaises(SystemExit) as cm:
            reader.read_sequence()
        self.assertEqual(cm.exception.code, 2)
        os.remove(tmp_path)

class TestPatternReader(unittest.TestCase):
    def test_read_patterns_file_not_set(self):
        reader = PatternReader(None)
        with self.assertRaises(SystemExit) as cm:
            reader.read_patterns()
        self.assertEqual(cm.exception.code, 2)

    def test_read_patterns_invalid_with_spaces_and_commas(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write("AAA,CCC\n GGG, TTT\n")  # invalid: contains commas and spaces
            tmp_path = tmp.name

        reader = PatternReader(tmp_path)

        with self.assertRaises(SystemExit) as cm:
            reader.read_patterns()

        # Verify exit code
        self.assertEqual(cm.exception.code, 2)

        os.remove(tmp_path)

    def test_read_patterns_valid(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write("AAA\nCCC\nGGG\nTTT\n")
            tmp_path = tmp.name

        reader = PatternReader(tmp_path)
        patterns = reader.read_patterns()

        self.assertEqual(patterns, {"AAA", "CCC", "GGG", "TTT"})
        os.remove(tmp_path)

class TestCodonUsageReader(unittest.TestCase):
    def test_read_codon_usage_success(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write("AUG 0.5\nUUU 1.0\n")
            tmp_path = tmp.name
        reader = CodonUsageReader(tmp_path)
        usage = reader.read_codon_usage()
        self.assertEqual(usage, {"ATG": 0.5, "TTT": 1.0})
        os.remove(tmp_path)

    def test_read_codon_usage_file_not_set(self):
        reader = CodonUsageReader(None)
        with self.assertRaises(SystemExit) as cm:
            reader.read_codon_usage()
        self.assertEqual(cm.exception.code, 2)

    def test_get_filename(self):
        reader = CodonUsageReader("/path/to/file.txt")
        self.assertEqual(reader.get_filename(), "file.txt")


class TestFileOperations(unittest.TestCase):
    def test_create_and_delete_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "subdir")
            create_dir(path)
            self.assertTrue(os.path.isdir(path))
            delete_dir(path)
            self.assertFalse(os.path.exists(path))

    def test_create_dir_failure(self):
        # Pass a file path instead of a directory
        with tempfile.NamedTemporaryFile() as tmp:
            result = create_dir(tmp.name)
            self.assertIn("failed", result)

class TestSaveFile(unittest.TestCase):
    def test_save_file_with_custom_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = save_file("content", "test.txt", tmp)
            expected_file = Path(tmp) / "BioSynth-Outputs" / "test.txt"
            self.assertTrue(expected_file.exists())
            self.assertIn(str(expected_file), result)

    def test_save_file_default_downloads(self):
        # Temporarily redirect home dir
        with tempfile.TemporaryDirectory() as tmp_home:
            old_home = os.environ.get("HOME")
            os.environ["HOME"] = tmp_home
            result = save_file("content", "default.txt")
            expected_file = Path(tmp_home) / "Downloads" / "BioSynth-Outputs" / "default.txt"
            self.assertTrue(expected_file.exists())
            os.environ["HOME"] = old_home if old_home else ""
            self.assertIn(str(expected_file), result)

    def test_save_file_with_invalid_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            # simulate ':' in filename
            result = save_file("content", "invalid:name.txt", tmp)
            self.assertIn("_", result)  # ':' replaced with '_'

    def test_save_file_permission_error(self):
        with patch("builtins.open", mock_open()) as mocked_open:
            mocked_open.side_effect = PermissionError("Permission denied")
            result = save_file("content", "test.txt", "/some/path")
        self.assertIn("An error occurred while saving the file - Permission denied", result)


class TestResourcePath(unittest.TestCase):
    def test_resource_path_normal(self):
        relative = "file.txt"
        path = resource_path(relative)
        self.assertTrue(path.endswith("file.txt"))

    def test_resource_path_with_meipass(self):
        sys._MEIPASS = "/tmp/fake_meipass"
        path = resource_path("file.txt")
        self.assertEqual(path, "/tmp/fake_meipass/file.txt")
        del sys._MEIPASS