import unittest

from Bio.Seq import Seq

from biosynth.utils.dna_utils import DNAUtils


class TestDNAHighlighter(unittest.TestCase):
    def test_get_coding_and_non_coding_regions(self):
        seq = Seq(
            "CGCGGTTTTGTAGAAGGTTAGGGGAATAGGTTAGATTGAGTGGCTTAAGAATGTAAATGCTTCTTGTGGAACTCGACAACGCAACAACGCGACGGATCTA"
            "CGTCACAGCGTGCATAGTGAAAACGGAGTTGCTGACGACGAAAGCGACATTGGGATCTGTCAGTTGTCATTCGCGAAAAACATCCGTCCCCGAGGCGGAC"
            "ACTGATTGAGCGTACAATGGTTTAGATGCCCTGA"
        )
        seq_str = str(seq)

        coding_positions, coding_indexes = DNAUtils.get_coding_and_non_coding_regions_positions(seq_str)

        expected_coding_indexes = [(56, 209)]

        expected_coding_positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     1, 2, -3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1,
                                     2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2,
                                     3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1,
                                     2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.assertEqual(coding_indexes, expected_coding_indexes)
        self.assertEqual(coding_positions, expected_coding_positions)

    def test_get_coding_and_non_coding_regions_contained(self):
        seq = Seq("TATAATGTACATACAGTAAATGATGTACATACAGATGATGTACATACAGATGTAATACATACAGATGATGTACATACAGATGTAATAA")
        seq_str = str(seq)

        coding_positions, coding_indexes = DNAUtils.get_coding_and_non_coding_regions_positions(seq_str)
        expected_coding_indexes = [(19, 55), (64, 85)]

        expected_coding_positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, -3, 1, 2, 3, 1, 2,
                                     3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, -3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3,
                                     1, 2, 3, 0, 0, 0]

        self.assertEqual(coding_indexes, expected_coding_indexes)
        self.assertEqual(coding_positions, expected_coding_positions)

    def test_find_overlapping_regions_with_overlap(self):
        seq = "ATGGCTAACGTTGACCTAAATGCGTACCGGATGATGTAGATGCCCGCTTCAAGGGTGA"  # Two overlapping ORFs
        has_overlap, overlaps = DNAUtils.find_overlapping_regions(seq)
        self.assertTrue(has_overlap)
        self.assertGreater(len(overlaps), 0)
        # Ensure overlaps are correctly reported as tuples
        for (start1, end1), (start2, end2) in overlaps:
            self.assertTrue(start1 < end1 and start2 < end2)

    def test_find_overlapping_regions_without_overlap(self):
        seq = "AAATGAAAATAA"  # Single valid ORF
        has_overlap, overlaps = DNAUtils.find_overlapping_regions(seq)
        self.assertFalse(has_overlap)
        self.assertEqual(overlaps, []) # pointer line should be present

    def test_get_coding_regions_list(self):
        seq = "AAATGAAATAAATGCCCCTAGGG"
        coding_indexes = [(3, 12), (12, 21)]
        coding_regions = DNAUtils.get_coding_regions_list(coding_indexes, seq)
        self.assertEqual(len(coding_regions), 2)
        self.assertEqual(coding_regions["1"], seq[3:12])
        self.assertEqual(coding_regions["2"], seq[12:21])

    def test_get_overlapping_regions_output(self):
        seq = "ATGGCTAACGTTGACCTAAATGCGTACCGGATGATGTAGATGCCCGCTTCAAGGGTGA"
        has_overlap, overlaps = DNAUtils.find_overlapping_regions(seq)
        info = DNAUtils.get_overlapping_regions(seq, overlaps, flank=5)

        self.assertIsInstance(info, str)
        self.assertIn("Shared Region", info)
        self.assertIn("^", info)  # Pointer line should be present
        self.assertIn("Context:", info)

    def test_get_coding_and_non_coding_regions_no_orf(self):
        seq = "AAACCCGGGTTT"  # No ATG or stop codons
        codon_positions, coding_indexes = DNAUtils.get_coding_and_non_coding_regions_positions(seq)

        self.assertTrue(all(pos == 0 for pos in codon_positions))
        self.assertEqual(coding_indexes, [])

    def test_get_coding_and_non_coding_regions_start_no_stop(self):
        seq = "AAATGCCCCCCCC"  # ATG but no stop codon
        codon_positions, coding_indexes = DNAUtils.get_coding_and_non_coding_regions_positions(seq)

        self.assertTrue(all(pos == 0 for pos in codon_positions))  # All non-coding
        self.assertEqual(coding_indexes, [])

    def test_get_coding_and_non_coding_regions_short_orf(self):
        # ATG + TAA only → length 6 < min_coding_region_length
        seq = "AAATGTAA"
        codon_positions, coding_indexes = DNAUtils.get_coding_and_non_coding_regions_positions(seq)

        self.assertTrue(all(pos == 0 for pos in codon_positions))
        self.assertEqual(coding_indexes, [])

    def test_get_coding_regions_list_empty(self):
        seq = "AAATGAAATAA"
        coding_regions = DNAUtils.get_coding_regions_list([], seq)
        self.assertEqual(coding_regions, {})

    def test_get_coding_regions_list_single(self):
        seq = "AAATGAAATAA"
        coding_indexes = [(2, 11)]
        coding_regions = DNAUtils.get_coding_regions_list(coding_indexes, seq)

        self.assertEqual(len(coding_regions), 1)
        self.assertEqual(coding_regions["1"], seq[2:11])

    def test_get_overlapping_regions_edge(self):
        seq = "ATGAAATAAATGAAAATGA"
        has_overlap, overlaps = DNAUtils.find_overlapping_regions(seq)
        info = DNAUtils.get_overlapping_regions(seq, overlaps, flank=3)

        self.assertIsInstance(info, str)
        self.assertIn("Target Sequence Length: 19", info)


