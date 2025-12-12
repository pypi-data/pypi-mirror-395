import argparse
import sys
import logging
import importlib.metadata

from . import downloader
from . import processor

# --- Get Version Dynamically ---
try:
    __version__ = importlib.metadata.version("refseq-plasmid-dl")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
# -------------------------------


def main(args=None):
    """
    The main entry point for the refseq-plasmid-dl command.
    """

    # ----------------------------------------------------
    # Argument Parsing
    # ----------------------------------------------------
    cli_parser = argparse.ArgumentParser(
        description="Download, curate, and filter plasmid sequences from the NCBI RefSeq database.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    cli_parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the program version and exit.",
    )

    cli_parser.add_argument(
        "--outdir",
        "-o",
        type=str,
        default="refseq_plasmids",
        help="Directory to save FASTA files, reports, and final multi-FASTA (default: refseq_plasmids).",
    )

    cli_parser.add_argument(
        "--indir",
        "-i",
        type=str,
        help="Directory where FASTA and GBFF files have already been downloaded. If provided, skips the download step.",
    )

    # --- General Filters ---
    cli_parser.add_argument(
        "--dev-mode",
        "-d",
        action="store_true",
        help="Enables development mode: fetches only a single test file group.",
    )

    cli_parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download of files even if they already exist locally.",
    )

    tax_group = cli_parser.add_argument_group("Taxonomy Filters")
    tax_group.add_argument(
        "--organism",
        "-s",
        type=str,
        default="all",
        help='Filter by species/organism (e.g. "Salmonella"). Case-insensitive substring match. Default: all',
    )
    tax_group.add_argument(
        "--taxid",
        "-t",
        type=str,
        default="all",
        help='Filter by NCBI Taxonomy ID (e.g. "28901"). Default: all',
    )

    # --- Metadata Filters ---
    meta_group = cli_parser.add_argument_group("Metadata Filters")
    meta_group.add_argument(
        "--strain", type=str, help="Filter by Strain (substring match)."
    )

    meta_group.add_argument(
        "--isolate", type=str, help="Filter by Isolate (substring match)."
    )

    meta_group.add_argument(
        "--host",
        type=str,
        help='Filter by Host (substring match, e.g. "Homo sapiens").',
    )

    meta_group.add_argument(
        "--plasmid-name", type=str, help="Filter by Plasmid Name (substring match)."
    )

    meta_group.add_argument(
        "--geo_loc_name",
        type=str,
        help="Filter by Geographic Location Name (substring match).",
    )

    meta_group.add_argument(
        "--isolation_source",
        type=str,
        help="Filter by Isolation Source (substring match).",
    )

    # --- Sequence Properties Filters ---
    seq_group = cli_parser.add_argument_group("Sequence Properties Filters")
    seq_group.add_argument(
        "--min-length", type=int, help="Minimum sequence length (bp)."
    )

    seq_group.add_argument(
        "--max-length", type=int, help="Maximum sequence length (bp)."
    )

    seq_group.add_argument(
        "--topology",
        choices=["circular", "linear", "all"],
        default="circular",
        help="Filter by topology (circular or linear). Default: circular",
    )

    # --- Date Filters ---
    date_group = cli_parser.add_argument_group("Date Filters")
    date_group.add_argument(
        "--min-date", type=str, help="Include only records updated after YYYY-MM-DD."
    )

    date_group.add_argument(
        "--max-date", type=str, help="Include only records updated before YYYY-MM-DD."
    )
    date_group.add_argument(
        "--min-collection-date",
        type=str,
        help="Include only records collected after YYYY-MM-DD.",
    )

    date_group.add_argument(
        "--max-collection-date",
        type=str,
        help="Include only records collected before YYYY-MM-DD.",
    )

    args = cli_parser.parse_args(args)

    logging.info("Starting refseq-plasmid-dl workflow")
    logging.info(f"Working Directory: {args.outdir}")
    if args.indir:
        logging.info(f"Input Directory (skip download): {args.indir}")

    if args.dev_mode:
        logging.info("Development mode enabled.")

    if args.force:
        logging.info("Force re-download enabled.")
        if args.indir:
            logging.warning("Force re-download flag ignored when using --indir.")
    if args.organism != "all":
        logging.info(f"Organism filter: {args.organism}")
    if args.taxid != "all":
        logging.info(f"Taxonomy ID filter: {args.taxid}")
    if args.strain:
        logging.info(f"Strain filter: {args.strain}")
    if args.isolate:
        logging.info(f"Isolate filter: {args.isolate}")
    if args.host:
        logging.info(f"Host filter: {args.host}")
    if args.plasmid_name:
        logging.info(f"Plasmid Name filter: {args.plasmid_name}")
    if args.geo_loc_name:
        logging.info(f"Geographic Location Name filter: {args.geo_loc_name}")
    if args.isolation_source:
        logging.info(f"Isolation Source filter: {args.isolation_source}")
    if args.min_length:
        logging.info(f"Minimum length filter: {args.min_length} bp")
    if args.max_length:
        logging.info(f"Maximum length filter: {args.max_length} bp")
    if args.topology != "all":
        logging.info(f"Topology filter: {args.topology}")
    if args.min_date:
        logging.info(f"Minimum date filter: {args.min_date}")
    if args.max_date:
        logging.info(f"Maximum date filter: {args.max_date}")
    if args.min_collection_date:
        logging.info(f"Minimum collection date filter: {args.min_date}")
    if args.max_collection_date:
        logging.info(f"Maximum collection date filter: {args.max_date}")

    # 1. Download Stage
    if not args.indir:
        try:
            downloader.run_download(args)
        except Exception as e:
            logging.fatal(f"FATAL: Download stage failed: {e}. Exiting script.")
            sys.exit(1)
    else:
        logging.info(
            f"Skipping download stage and using files in {args.indir} instead."
        )

    # 2. Parsing and Filtering Stage
    # Pack filters into a clean dictionary
    filters = {
        "organism": args.organism,
        "taxid": args.taxid,
        "strain": args.strain,
        "isolate": args.isolate,
        "host": args.host,
        "plasmid_name": args.plasmid_name,
        "geo_loc_name": args.geo_loc_name,
        "isolation_source": args.isolation_source,
        "min_length": args.min_length,
        "max_length": args.max_length,
        "topology": args.topology,
        "min_date": args.min_date,
        "max_date": args.max_date,
        "min_collection_date": args.min_collection_date,
        "max_collection_date": args.max_collection_date,
    }

    try:
        processor.process_files(
            input_dir=args.indir if args.indir else args.outdir,
            output_dir=args.outdir,
            filters=filters,
        )
    except Exception as e:
        logging.fatal(f"FATAL: Processing stage failed: {e}. Exiting script.")
        sys.exit(1)

    logging.info("Workflow successfully completed.")


if __name__ == "__main__":
    main()
