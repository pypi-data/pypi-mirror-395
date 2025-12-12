import gzip
import csv
import os
import logging
import re
from pathlib import Path
from Bio import SeqIO
from tqdm import tqdm
from datetime import datetime

# ----------------------------------------------------------------------
# Date Parsing Helpers
# ----------------------------------------------------------------------


def parse_genbank_date(date_str):
    """
    Parses the standard GenBank LOCUS date format (e.g., '28-OCT-2024').
    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%d-%b-%Y")
    except ValueError:
        return None


def parse_cli_date(date_str):
    """
    Parses CLI input date (YYYY-MM-DD).
    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def parse_collection_date(date_str):
    """
    Parses the 'collection_date' qualifier.
    GenBank collection dates vary: 'YYYY', 'YYYY-MM', or 'YYYY-MM-DD'.
    We normalize incomplete dates to the first of the month/year for comparison.
    """
    if not date_str:
        return None

    # Try YYYY-MM-DD
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        pass

    # Try YYYY-MM (default to 1st of month)
    try:
        return datetime.strptime(date_str, "%Y-%m")
    except ValueError:
        pass

    # Try YYYY (default to Jan 1st)
    try:
        return datetime.strptime(date_str, "%Y")
    except ValueError:
        pass

    return None


# ----------------------------------------------------------------------
# Filtering Logic
# ----------------------------------------------------------------------


def check_filters(meta, filters, stats):
    """
    Evaluates a metadata dictionary against a dictionary of filters.
    Updates stats in place.
    Returns True if passed, False if rejected.
    """

    # 1. Organism
    if filters.get("organism", "all").lower() != "all":
        if filters["organism"].lower() not in meta["organism"].lower():
            stats["filtered_by_organism"] += 1
            return False

    # 2. TaxID
    if filters.get("taxid", "all").lower() != "all":
        if meta["taxid"] != filters["taxid"]:
            stats["filtered_by_taxid"] += 1
            return False

    # 3. Topology
    if filters.get("topology", "all").lower() != "all":
        if meta["topology"].lower() != filters["topology"].lower():
            stats["filtered_by_topology"] += 1
            return False

    # 4. String Filters
    # (Strain, Isolate, Host, Plasmid Name, Geo Location, Isolation Source)
    string_checks = [
        "strain",
        "isolate",
        "host",
        "plasmid_name",
        "geo_loc_name",
        "isolation_source",
    ]
    for field in string_checks:
        filter_val = filters.get(field)
        if filter_val:
            # Case-insensitive substring match
            if filter_val.lower() not in meta.get(field, "").lower():
                stats[f"filtered_by_{field}"] += 1
                return False

    # 5. Length Filter (GBFF Check)
    # If sequence_length is 0 (Master record), we pass it here and filter
    # strictly during the FASTA step.
    length = meta.get("sequence_length", 0)
    if length > 0:
        if filters.get("min_length") and length < filters["min_length"]:
            stats["filtered_by_length"] += 1
            return False
        if filters.get("max_length") and length > filters["max_length"]:
            stats["filtered_by_length"] += 1
            return False

    # 6. Record Update Date Filter (LOCUS date)
    if filters.get("min_date") or filters.get("max_date"):
        record_date_obj = parse_genbank_date(meta.get("date", ""))
        if record_date_obj:
            if filters.get("min_date"):
                min_d = parse_cli_date(filters["min_date"])
                if min_d and record_date_obj < min_d:
                    stats["filtered_by_date"] += 1
                    return False
            if filters.get("max_date"):
                max_d = parse_cli_date(filters["max_date"])
                if max_d and record_date_obj > max_d:
                    stats["filtered_by_date"] += 1
                    return False

    # 7. Collection Date Filter (Metadata qualifier)
    if filters.get("min_collection_date") or filters.get("max_collection_date"):
        coll_date_obj = parse_collection_date(meta.get("collection_date", ""))

        # Dropped if record has no collection date but filter is active.
        if not coll_date_obj:
            stats["filtered_by_collection_date"] += 1
            return False

        if filters.get("min_collection_date"):
            min_c = parse_cli_date(filters["min_collection_date"])
            if min_c and coll_date_obj < min_c:
                stats["filtered_by_collection_date"] += 1
                return False
        if filters.get("max_collection_date"):
            max_c = parse_cli_date(filters["max_collection_date"])
            if max_c and coll_date_obj > max_c:
                stats["filtered_by_collection_date"] += 1
                return False

    return True


# ----------------------------------------------------------------------
# File Processing
# ----------------------------------------------------------------------


def get_filtered_metadata(gbff_path, filters, stats):
    """
    Parses a GBFF file and returns a DICTIONARY of valid accessions.
    """
    valid_records = {}

    try:
        opener = gzip.open if str(gbff_path).endswith(".gz") else open
        logging.info(f"Parsing metadata from {gbff_path.name}...")

        with opener(gbff_path, "rt") as handle:
            iterator = tqdm(
                SeqIO.parse(handle, "genbank"),
                desc="Reading GenBank Records",
                unit="rec",
            )

            for record in iterator:
                stats["total_gbff_records"] += 1

                # Extract Fields
                meta = {
                    "accession": record.id,
                    "definition": record.description,
                    "organism": record.annotations.get("organism", ""),
                    "taxonomy": "; ".join(record.annotations.get("taxonomy", [])),
                    "topology": record.annotations.get("topology", "linear"),
                    "date": record.annotations.get("date", ""),
                    "sequence_length": len(record.seq) if record.seq else 0,
                    "source_file": Path(gbff_path).name,
                    # Placeholders
                    "strain": "",
                    "isolate": "",
                    "host": "",
                    "plasmid_name": "",
                    "geo_loc_name": "",
                    "collection_date": "",
                    "isolation_source": "",
                    "biosample": "",
                    "bioproject": "",
                    "taxid": "",
                }

                # Parse features
                for feat in record.features:
                    if feat.type == "source":
                        q = feat.qualifiers
                        meta["plasmid_name"] = q.get("plasmid", [""])[0]
                        meta["strain"] = q.get("strain", [""])[0]
                        meta["isolate"] = q.get("isolate", [""])[0]
                        meta["host"] = q.get("host", [""])[0]
                        meta["geo_loc_name"] = q.get("geo_loc_name", [""])[0]
                        meta["collection_date"] = q.get("collection_date", [""])[0]
                        meta["isolation_source"] = q.get("isolation_source", [""])[0]

                        if "db_xref" in q:
                            for x in q["db_xref"]:
                                if x.startswith("taxon:"):
                                    meta["taxid"] = x.split(":")[1]
                                elif x.startswith("BioSample:"):
                                    meta["biosample"] = x.split(":")[1]
                                elif x.startswith("BioProject:"):
                                    meta["bioproject"] = x.split(":")[1]

                # Check Filters
                if check_filters(meta, filters, stats):
                    stats["kept_gbff_records"] += 1
                    valid_records[meta["accession"]] = meta

    except Exception as e:
        logging.error(f"Error reading GBFF {gbff_path}: {e}")

    return valid_records


def generate_summary_report(output_dir, stats, filters):
    report_path = os.path.join(output_dir, "refseq_plasmids_dl_report.csv")
    try:
        with open(report_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])

            # Write Filters
            for k, v in filters.items():
                if v:
                    writer.writerow([f"Filter: {k}", v])

            writer.writerow([])
            writer.writerow(["Total GBFF Files Scanned", stats["total_gbff_files"]])
            writer.writerow(
                ["Total Metadata Records Found", stats["total_gbff_records"]]
            )

            # Write Rejection Stats dynamically
            for k in sorted(stats.keys()):
                if k.startswith("filtered_by_"):
                    writer.writerow(
                        [f"Records {k.replace('_', ' ').title()}", stats[k]]
                    )

            writer.writerow(["Kept Metadata Records", stats["kept_gbff_records"]])
            writer.writerow(["Sequences Written to FASTA", stats["sequences_written"]])

            diff = stats["kept_gbff_records"] - stats["sequences_written"]
            if diff != 0:
                writer.writerow(["Discrepancy (Missing FASTA data)", diff])

        logging.info(f"Summary report written to: {report_path}")
    except Exception as e:
        logging.error(f"Failed to write summary report: {e}")


def process_files(input_dir, output_dir, filters):
    input_path = Path(input_dir) / "refseq_plasmids"

    # Allow looking in root input_dir if subdir doesn't exist (flexibility)
    if not input_path.exists():
        input_path = Path(input_dir)

    if not input_path.exists():
        logging.error(f"Input directory does not exist: {input_path}")
        return

    gbff_files = sorted(input_path.glob("*.gbff.gz"))
    if not gbff_files:
        logging.error(f"No .gbff.gz files found in {input_path}")
        return

    fasta_out_path = os.path.join(output_dir, "refseq_plasmids_dl.fasta")
    csv_out_path = os.path.join(output_dir, "refseq_plasmids_dl_metadata.csv")

    # Init Stats
    stats = {
        "total_gbff_files": 0,
        "total_gbff_records": 0,
        "kept_gbff_records": 0,
        "sequences_written": 0,
        # Filter Counters
        "filtered_by_organism": 0,
        "filtered_by_taxid": 0,
        "filtered_by_topology": 0,
        "filtered_by_strain": 0,
        "filtered_by_isolate": 0,
        "filtered_by_host": 0,
        "filtered_by_plasmid_name": 0,
        "filtered_by_geo_loc_name": 0,
        "filtered_by_isolation_source": 0,
        "filtered_by_length": 0,
        "filtered_by_date": 0,
        "filtered_by_collection_date": 0,
    }

    logging.info(f"Found {len(gbff_files)} GBFF master files. Starting processing...")

    fieldnames = [
        "accession",
        "definition",
        "organism",
        "taxonomy",
        "topology",
        "date",
        "strain",
        "isolate",
        "host",
        "plasmid_name",
        "geo_loc_name",
        "collection_date",
        "isolation_source",
        "biosample",
        "bioproject",
        "taxid",
        "sequence_length",
        "source_file",
    ]

    with (
        open(fasta_out_path, "w") as f_out,
        open(csv_out_path, "w", newline="", encoding="utf-8") as csv_file,
    ):
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for gbff_path in gbff_files:
            stats["total_gbff_files"] += 1

            # 1. Build Whitelist (Metadata Filter)
            valid_metadata_map = get_filtered_metadata(gbff_path, filters, stats)
            if not valid_metadata_map:
                continue

            # 2. Identify Sequence Files
            # Expecting filename format: plasmid.1.genomic.gbff.gz -> plasmid.1.1.genomic.fna.gz
            # Helper to find matching FNA file
            base_name = gbff_path.name.replace(".gbff.gz", "")

            # Attempt exact match first (standard NCBI structure)
            fna_candidates = list(input_path.glob(f"{base_name}*.fna.gz"))

            # If standard naming fails, try the group prefix method
            if not fna_candidates:
                match = re.search(r"(plasmid\.\d+)", gbff_path.name)
                if match:
                    group_prefix = match.group(1)
                    fna_candidates = sorted(input_path.glob(f"{group_prefix}*.fna.gz"))

            # 3. Stream FASTAs
            for fna_path in fna_candidates:
                try:
                    with gzip.open(fna_path, "rt") as handle:
                        fasta_iter = tqdm(
                            SeqIO.parse(handle, "fasta"),
                            desc=f"Scanning {fna_path.name}",
                            unit="seq",
                            leave=False,
                        )
                        for record in fasta_iter:
                            if record.id in valid_metadata_map:
                                meta = valid_metadata_map[record.id]

                                # Update length if missing (common in master records)
                                seq_len = len(record.seq)
                                if meta["sequence_length"] == 0:
                                    meta["sequence_length"] = seq_len

                                # RE-CHECK LENGTH FILTER
                                # (Crucial for master records where length was 0 in GBFF)
                                if (
                                    filters.get("min_length")
                                    and seq_len < filters["min_length"]
                                ):
                                    stats["filtered_by_length"] += 1
                                    continue
                                if (
                                    filters.get("max_length")
                                    and seq_len > filters["max_length"]
                                ):
                                    stats["filtered_by_length"] += 1
                                    continue

                                SeqIO.write(record, f_out, "fasta")
                                writer.writerow(meta)
                                stats["sequences_written"] += 1
                except Exception as e:
                    logging.error(f"Error reading FASTA {fna_path.name}: {e}")

    generate_summary_report(output_dir, stats, filters)
    logging.info(f"Done. Processed and saved {stats['sequences_written']} sequences.")
