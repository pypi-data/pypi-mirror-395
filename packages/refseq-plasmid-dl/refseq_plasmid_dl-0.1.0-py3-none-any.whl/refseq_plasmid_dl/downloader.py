import requests
from bs4 import BeautifulSoup
import os
import re
import time
import sys
from tqdm import tqdm
from urllib.parse import urljoin
import logging

# Configure logging to show information messages
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Helper Functions for Pattern and Counting ---


def get_file_pattern(dev_mode):
    """
    Returns the compiled regex pattern based on the development mode.
    """
    if dev_mode:
        # In dev mode, only target one specific file for quick testing.
        return re.compile(r"^plasmid\.1(\..+)?\.genomic\..*\.gz$")
    else:
        # In full mode, target all genomic fna.gz files.
        return re.compile(r"^plasmid\.\d+(\..+)?\.genomic\..*\.gz$")


def get_total_files_count(url, dev_mode, local_dir):
    """
    Fetches the HTML directory listing, counts files matching the pattern,
    and saves the HTML content to a local file.

    Returns (count, html_content). Returns (1, "") if a failure occurs.
    """
    logging.info("Attempting to count total files dynamically and fetch index...")
    try:
        # Fetch the HTML listing of the directory
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text  # Store content

        soup = BeautifulSoup(html_content, "html.parser")
        file_pattern = get_file_pattern(dev_mode)

        count = 0
        # Look for all links in the HTML
        for link in soup.find_all("a"):
            href = link.get("href")
            # Check if the link matches the file pattern
            if href and file_pattern.search(href):
                count += 1

        # 2. Save the HTML content (MOVED HERE from https_walk)
        html_filename = "plasmids_index.html"
        html_filepath = os.path.join(local_dir, html_filename)
        with open(html_filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        logging.info(f"Saved HTML index to: {html_filepath}")

        logging.info(f"Found {count} files matching the pattern.")
        return (count, html_content)  # Return count and content

    except requests.exceptions.RequestException as e:
        logging.error(f"ERROR accessing {url} for file count. Using 1 as estimate: {e}")
        # Fallback to a small estimate and empty content if counting/fetching fails
        return (1, "")
    except Exception as e:
        logging.error(f"ERROR during file counting/saving: {e}")
        return (1, "")


def download_file_https(url, local_path, force=False):
    """
    Downloads a single file using HTTPS requests.
    Args:
        url: Remote URL
        local_path: Local directory
        force: If True, re-download even if file exists.
    """
    filename = os.path.basename(url)
    full_local_path = os.path.join(local_path, filename)

    if not force and os.path.exists(full_local_path):
        logging.info(f"File already exists, skipping download: {filename}")
        return True

    logging.info(f"Downloading: {filename}")

    try:
        # Stream=True for large files
        with requests.get(url, stream=True) as r:
            r.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

            with open(full_local_path, "wb") as f:
                # Iterate over chunks to save memory
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"ERROR downloading {filename}: {e}", file=sys.stderr)
        # Clean up partial download
        if os.path.exists(full_local_path):
            os.remove(full_local_path)
        return False


def https_walk(url, local_dir, progress_bar, dev_mode, html_content, force=False):
    """
    Traverses the HTTPS directory listing and downloads matching files,
    using the pre-fetched HTML content.
    """
    # Use the centralized pattern logic
    file_pattern = get_file_pattern(dev_mode)

    try:
        # Use the pre-fetched content instead of making a new requests.get(url) call
        soup = BeautifulSoup(html_content, "html.parser")

        # The HTML saving part was moved to get_total_files_count

        # Look for all links in the HTML
        for link in soup.find_all("a"):
            href = link.get("href")
            if not href:
                continue

            full_remote_url = urljoin(url, href)

            # 1. Check if the link is a file we want to download
            if file_pattern.search(href):
                multifasta_dir = os.path.join(local_dir, "refseq_plasmids")
                # Only update the progress bar if the download was successful
                if download_file_https(full_remote_url, multifasta_dir, force):
                    progress_bar.update(1)
                time.sleep(1.0)

    except Exception as e:
        # Catch remaining exceptions during parsing/walking
        logging.error(f"Error during parsing/walking {url}: {e}", file=sys.stderr)


def run_download(args):
    """
    Establishes the base connection and initiates the download, supporting dev mode.

    total_files_estimate is now dynamic and the HTML content is cached.
    """
    outdir = args.outdir
    dev_mode = args.dev_mode
    base_url = "https://ftp.ncbi.nih.gov/genomes/refseq/plasmid/"
    logging.info(f"Starting HTTPS download from: {base_url}")
    os.makedirs(f"{outdir}/refseq_plasmids", exist_ok=True)

    try:
        # --- DYNAMIC COUNTING & FETCHING ---
        # Get count and the HTML content in one go.
        total_files, html_content = get_total_files_count(base_url, dev_mode, outdir)
        # --- END DYNAMIC COUNTING & FETCHING ---

        if total_files == 0:
            logging.warning(
                "No files found matching the criteria. Exiting.", file=sys.stderr
            )
            return

        with tqdm(
            total=total_files,
            desc="Downloading Files",
            unit="file",
            position=0,
            leave=True,
        ) as pbar:
            # Pass the pre-fetched HTML content to avoid a second network request
            https_walk(base_url, outdir, pbar, dev_mode, html_content, force=args.force)

        logging.info("HTTPS download stage finished.")

    except Exception as e:
        raise Exception(f"Download/Parsing Failure: {e}")
