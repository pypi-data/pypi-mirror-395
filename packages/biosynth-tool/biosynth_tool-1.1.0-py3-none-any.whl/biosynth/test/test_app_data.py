import unittest
from pathlib import Path
from biosynth.data import app_data  # replace with your actual module path


class TestDataClasses(unittest.TestCase):

    def test_input_data_defaults(self):
        self.assertIsNone(app_data.InputData.dna_sequence)
        self.assertIsNone(app_data.InputData.unwanted_patterns)
        self.assertIsNone(app_data.InputData.coding_indexes)
        self.assertIsNone(app_data.InputData.coding_positions)
        self.assertIsNone(app_data.InputData.coding_regions_list)
        self.assertIsNone(app_data.InputData.excluded_coding_indexes)
        self.assertIsNone(app_data.InputData.excluded_coding_positions)
        self.assertIsNone(app_data.InputData.excluded_regions_list)

    def test_input_data_reset(self):
        # Set some dummy values
        app_data.InputData.dna_sequence = "ATG"
        app_data.InputData.coding_indexes = [0, 1, 2]
        app_data.InputData.excluded_regions_list = [(0, 2)]

        # Reset
        app_data.InputData.reset()

        # All fields should be None
        self.assertIsNone(app_data.InputData.dna_sequence)
        self.assertIsNone(app_data.InputData.unwanted_patterns)
        self.assertIsNone(app_data.InputData.coding_indexes)
        self.assertIsNone(app_data.InputData.coding_positions)
        self.assertIsNone(app_data.InputData.coding_regions_list)
        self.assertIsNone(app_data.InputData.excluded_coding_indexes)
        self.assertIsNone(app_data.InputData.excluded_coding_positions)
        self.assertIsNone(app_data.InputData.excluded_regions_list)

    def test_cost_data_defaults(self):
        self.assertIsNone(app_data.CostData.codon_usage)
        self.assertIsNone(app_data.CostData.codon_usage_filename)
        self.assertEqual(app_data.CostData.alpha, 1.0)
        self.assertEqual(app_data.CostData.beta, 2.0)
        self.assertEqual(app_data.CostData.w, 100.0)
        self.assertEqual(app_data.CostData.stop_codon, float('inf'))

    def test_elimination_data_defaults(self):
        self.assertIsNone(app_data.EliminationData.info)
        self.assertIsNone(app_data.EliminationData.detailed_changes)
        self.assertIsNone(app_data.EliminationData.min_cost)

    def test_output_data_defaults(self):
        self.assertEqual(app_data.OutputData.output_path, Path.home() / 'Downloads')
        self.assertIsNone(app_data.OutputData.optimized_sequence)

    def test_input_data_mutation(self):
        app_data.InputData.dna_sequence = "ATGCGT"
        app_data.InputData.coding_positions = [0,1,2]
        self.assertEqual(app_data.InputData.dna_sequence, "ATGCGT")
        self.assertEqual(app_data.InputData.coding_positions, [0,1,2])

    def test_output_data_path_assignment(self):
        new_path = Path("/tmp")
        app_data.OutputData.output_path = new_path
        self.assertEqual(app_data.OutputData.output_path, new_path)

    def test_cost_data_numeric(self):
        self.assertGreaterEqual(app_data.CostData.alpha, 0)
        self.assertGreaterEqual(app_data.CostData.beta, 0)
        self.assertGreaterEqual(app_data.CostData.w, 0)
        self.assertTrue(app_data.CostData.stop_codon == float('inf'))



