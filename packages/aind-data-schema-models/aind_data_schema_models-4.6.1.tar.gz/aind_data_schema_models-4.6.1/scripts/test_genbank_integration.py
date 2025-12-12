"""Integration test for GenBank data retrieval and parsing."""

import sys

from aind_data_schema_models.gene import Gene


def main():
    """Main function to test GenBank integration"""
    accession_id = "LN515608"
    try:
        nucleotide = Gene.from_genbank_accession_id(accession_id)
    except Exception as e:
        print(f"Failed to fetch GenBank record: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"Name: {nucleotide.name}")
    print(f"Description: {nucleotide.description}")
    print(f"Registry: {nucleotide.registry}")
    print(f"Registry Identifier: {nucleotide.registry_identifier}")
    assert "Synthetic construct for Aequorea victoria partial gfp gene for GFP." in nucleotide.description
    assert nucleotide.name == "gfp"
    print("Integration test passed.")


if __name__ == "__main__":
    main()
