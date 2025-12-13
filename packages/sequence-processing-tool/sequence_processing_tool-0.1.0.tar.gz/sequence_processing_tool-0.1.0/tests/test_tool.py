import unittest
from io import StringIO
from SequenceTool.SeqProcessingTool import SeqProcessingTool

class TestSeqProcessingTool(unittest.TestCase):

    def setUp(self):
        self.tool = SeqProcessingTool()

    def test_isDNA(self):
        self.assertTrue(self.tool.isDNA("ATCGNNNN"))
        self.assertFalse(self.tool.isDNA("MKRQW"))

    def test_codon_table(self):
        codon_table = self.tool.condon_table()
        self.assertEqual(codon_table["AUG"], "M")
        self.assertEqual(codon_table["UUU"], "F")
        self.assertEqual(codon_table["UAG"], "*")

    def test_fastq2fasta_and_fasta_qc(self):
        fake_fastq = StringIO("@seq1\nATCG\n+\IIII\n")
        temp_fasta_path = self.tool.fastq2fasta(fake_fastq)

        with open(temp_fasta_path) as f:
            result = self.tool.fasta_qc(f)
        # print("result keys:", list(result.keys()))
        # print("result values:", result)

        self.assertEqual(result[">seq1"], "ATCG")

    def test_match_convert_codon(self):
        self.tool.data = {
            ">seq1": "GTAGCATAA",
            ">seq2": "GCCGACTAA"
        }

        aa_result = self.tool.match_convert(mode="condon")
        expected = {
            ">seq1": "VA*",
            ">seq2": "AD*"
        }

        self.assertEqual(aa_result, expected)

    def test_match_convert_barcode(self):
        self.tool.data = {
            ">seq1": "ATCGGATCGGCTATCCTCT",
            ">seq2": "GTAAGGAGTCGATCGATCG"
        }
        self.tool.quality = {
            ">seq1": "IIIIIIIIIIIIIIIIIIII",
            ">seq2": "IIIIIIIIIIIIIIIIIIII"
        }

        barcode_result = self.tool.match_convert(mode="barcode")

        first_barcode = self.tool.barcode()[0]
        seq1_result = barcode_result[first_barcode][0][">seq1"]

        self.assertEqual(seq1_result, "ATCGGATCGGC")

    def test_count(self):
        self.tool.data = {
            ">seq1": "ACCDXX",
            ">seq2": "MCNPQX"
        }

        result = self.tool.count()
        self.assertEqual(result["A"], 1)
        self.assertEqual(result["C"], 3)
        self.assertIn("X", result)
        self.assertEqual(list(result.keys())[-1], "X")
        self.assertEqual(result["X"], 3)

if __name__ == "__main__":
    unittest.main()