import pytest
import os
import sys
import gzip
import csv
import textwrap
from pathlib import Path
from datetime import datetime

from refseq_plasmid_dl import processor

# ----------------------------------------------------------------------
# 1. Fixtures (Data Setup)
# ----------------------------------------------------------------------


@pytest.fixture
def mock_gbff_content():
    """
    A strictly formatted GenBank MASTER RECORD (CON division).
    REALITY CHECK: These files do NOT contain the sequence (ORIGIN block).
    They only contain metadata. The sequence is in the FASTA file.

    NOTE: We include an empty 'ORIGIN' tag. Biopython's parser requires
    a block terminator (ORIGIN, CONTIG, etc.) to exit the FEATURES table
    cleanly. Without it, it throws "Premature end of features table".
    """
    return textwrap.dedent(
        """\
    LOCUS       NZ_JBIHTS010000002          40 bp    DNA     linear  CON 28-OCT-2024
    DEFINITION  Pseudomonas aeruginosa strain PJK40 map unlocalized plasmid pPJK40
                GCLEKMFL_2, whole genome shotgun sequence.
    ACCESSION   NZ_JBIHTS010000002 NZ_JBIHTS010000000
    VERSION     NZ_JBIHTS010000002.1
    DBLINK      BioProject: PRJNA224116
                BioSample: SAMN44340155
                Assembly: GCF_043949555.1
    KEYWORDS    WGS; RefSeq.
    SOURCE      Pseudomonas aeruginosa
      ORGANISM  Pseudomonas aeruginosa
                Bacteria; Pseudomonadati; Pseudomonadota; Gammaproteobacteria;
                Pseudomonadales; Pseudomonadaceae; Pseudomonas.
    FEATURES             Location/Qualifiers
         source          1..40
                         /organism="Pseudomonas aeruginosa"
                         /mol_type="genomic DNA"
                         /strain="PJK40"
                         /plasmid="pPJK40"
                         /db_xref="taxon:287"
                         /collection_date="2023-05-01"
    ORIGIN
    //
    """
    )


@pytest.fixture
def setup_processor_data(tmp_path, mock_gbff_content):
    """
    Sets up the file structure required by processor.process_files.
    """
    input_dir = tmp_path / "refseq_plasmids"
    input_dir.mkdir()

    # 1. Create GBFF (Master Record, No Sequence)
    gbff_path = input_dir / "plasmid.1.genomic.gbff.gz"
    with gzip.open(gbff_path, "wt") as f:
        f.write(mock_gbff_content)

    # 2. Create matching FASTA (Contains the REAL Sequence)
    # The ID must match the GBFF Version
    fna_path = input_dir / "plasmid.1.1.genomic.fna.gz"
    with gzip.open(fna_path, "wt") as f:
        f.write(
            ">NZ_JBIHTS010000002.1 Pseudomonas aeruginosa plasmid\nATGCATGCATATGCATGCATATGCATGCATATGCATGCAT\n"
        )

    return tmp_path  # Return the root temp dir


# ----------------------------------------------------------------------
# 2. Unit Tests (Logic Verification)
# ----------------------------------------------------------------------


def test_parse_genbank_date():
    # Test valid date
    dt = processor.parse_genbank_date("28-OCT-2024")
    assert dt == datetime(2024, 10, 28)

    # Test invalid format
    assert processor.parse_genbank_date("2024-10-28") is None
    assert processor.parse_genbank_date("") is None


def test_check_filters_logic():
    """
    Tests the check_filters function specifically.
    """
    # Mock Metadata
    meta = {
        "organism": "Pseudomonas aeruginosa",
        "taxid": "287",
        "topology": "linear",
        "strain": "PJK40",
        "sequence_length": 1000,
        "date": "28-OCT-2024",
        "collection_date": "2023-01-01",
    }

    # Mock Stats Dictionary
    stats = {
        k: 0
        for k in [
            "filtered_by_organism",
            "filtered_by_taxid",
            "filtered_by_topology",
            "filtered_by_strain",
            "filtered_by_length",
            "filtered_by_date",
            "filtered_by_collection_date",
        ]
    }

    # Case 1: Pass all filters
    filters_pass = {"organism": "Pseudomonas", "min_length": 500}
    assert processor.check_filters(meta, filters_pass, stats) is True

    # Case 2: Fail Organism
    filters_fail_org = {"organism": "E. coli"}
    assert processor.check_filters(meta, filters_fail_org, stats) is False
    assert stats["filtered_by_organism"] == 1

    # Case 3: Fail Length
    filters_fail_len = {"min_length": 2000}
    assert processor.check_filters(meta, filters_fail_len, stats) is False
    assert stats["filtered_by_length"] == 1

    # Case 4: Fail Date (Min Date)
    # Meta is Oct 2024, Filter requires Jan 2025
    filters_fail_date = {"min_date": "2025-01-01"}
    assert processor.check_filters(meta, filters_fail_date, stats) is False
    assert stats["filtered_by_date"] == 1


# ----------------------------------------------------------------------
# 3. Integration Test (Full Pipeline)
# ----------------------------------------------------------------------


def test_process_files_end_to_end(setup_processor_data):
    """
    Runs the full process_files function on the temp directory
    and verifies output files.
    """
    input_dir = setup_processor_data
    output_dir = input_dir / "output"
    output_dir.mkdir()

    # Define filters that should MATCH our mock data
    filters = {"organism": "Pseudomonas", "strain": "PJK40", "min_length": 10}

    # Run the processor
    processor.process_files(input_dir, output_dir, filters)

    # --- ASSERTIONS ---

    # 1. Check FASTA output
    fasta_out = output_dir / "refseq_plasmids_dl.fasta"
    assert fasta_out.exists()

    with open(fasta_out, "r") as f:
        content = f.read()
        # Ensure header and sequence are present
        assert ">NZ_JBIHTS010000002.1" in content
        assert "ATGC" in content

    # 2. Check CSV Metadata output
    csv_out = output_dir / "refseq_plasmids_dl_metadata.csv"
    assert csv_out.exists()

    with open(csv_out, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 1
        row = rows[0]

        # Check specific fields
        assert row["accession"] == "NZ_JBIHTS010000002.1"
        assert row["strain"] == "PJK40"
        assert row["plasmid_name"] == "pPJK40"

    # 3. Check Report generation
    report_out = output_dir / "refseq_plasmids_dl_report.csv"
    assert report_out.exists()
