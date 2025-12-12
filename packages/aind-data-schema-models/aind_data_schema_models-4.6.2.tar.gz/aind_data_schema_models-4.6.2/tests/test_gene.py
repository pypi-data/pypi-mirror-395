"""Unit tests for the Gene model, focusing on GenBank accession ID retrieval."""

import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from aind_data_schema_models.gene import Gene, NucleotideModel


class TestGene(unittest.TestCase):
    """Tests for Gene model"""

    def setUp(self):
        """Setup"""
        # Load the mock GenBank response from file
        resource_path = Path(__file__).parent / "resources" / "genbank_response.txt"
        with open(resource_path, "r") as f:
            self.mock_genbank_text = f.read()

    @patch("aind_data_schema_models.gene.requests.get")
    def test_from_genbank_accession_id(self, mock_get):
        """Test fetching nucleotide data from GenBank accession ID."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.mock_genbank_text
        mock_get.return_value = mock_response

        accession_id = "LN515608"
        nucleotide = Gene.from_genbank_accession_id(accession_id)
        self.assertIsInstance(nucleotide, NucleotideModel)
        self.assertIn("Synthetic construct for Aequorea victoria partial gfp gene for GFP.", nucleotide.description)
        self.assertEqual(nucleotide.registry_identifier, "LN515608")
        self.assertEqual(nucleotide.registry.name, "GENBANK")
        self.assertEqual(nucleotide.name, "gfp")

    @patch("aind_data_schema_models.gene.requests.get")
    def test_from_genbank_accession_id_blank_response_raises(self, mock_get):
        """Test that a blank GenBank response raises a ValueError."""
        # Setup mock response with blank text
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = ""
        mock_get.return_value = mock_response

        accession_id = "LN000000"
        with self.assertRaises(ValueError):
            Gene.from_genbank_accession_id(accession_id)

    @patch("aind_data_schema_models.gene.requests.get")
    def test_from_genbank_accession_id_missing_gene_name_raises(self, mock_get):
        """Test that missing gene name in GenBank response raises a ValueError."""
        # Setup mock response with DEFINITION but no gene name
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = (
            "DEFINITION  Synthetic construct for Aequorea victoria partial gfp gene for GFP."
            "\nACCESSION   LN515608\n"  # No gene="..." in text
        )
        mock_get.return_value = mock_response

        accession_id = "LN515608"
        with self.assertRaises(ValueError):
            Gene.from_genbank_accession_id(accession_id)


if __name__ == "__main__":
    unittest.main()
