"""Tests classes in protocols module"""

import unittest

from aind_data_schema_models.protocols import Protocols


class TestProtocols(unittest.TestCase):
    """Tests methods in Protocols class"""

    def test_from_doi(self):
        """Tests protocol can be constructed from DOI"""
        # Use a known DOI from the generated models
        # Replace with a real DOI string present in your generated Protocols
        example_doi = next(iter(Protocols.doi_map.keys()))
        self.assertEqual(Protocols.doi_map[example_doi], Protocols.from_doi(example_doi))

    def test_from_url(self):
        """Tests protocol can be constructed from DOI URL"""
        # Use a known DOI and build a URL
        example_doi = next(iter(Protocols.doi_map.keys()))
        url = f"https://dx.doi.org/{example_doi}"
        self.assertEqual(Protocols.doi_map[example_doi], Protocols.from_url(url))


if __name__ == "__main__":
    unittest.main()
