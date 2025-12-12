# refseq-plasmid-dl

**refseq-plasmid-dl** is a Python command-line tool for downloading, parsing, filtering, and curating plasmid sequences from the NCBI RefSeq database. It provides flexible metadata filtering, sequence property filtering, and generates comprehensive reports and curated multi-FASTA files.


This project was heavily inspired by the excellent [ncbi-genome-download tool](https://github.com/kblin/ncbi-genome-download), which is a staple for fetching bacterial assemblies. However, I found it difficult to specifically target and download only plasmid sequences using its existing filters. I built this tool to bridge that gap, providing a dedicated workflow for retrieving plasmid data from RefSeq without the overhead of filtering through full genome assemblies.

---

## Features

* **Download Plasmid Sequences**: Recursively fetches all gzipped FASTA files (*.fna.gz) and GenBank files (*.gbff.gz) from the NCBI RefSeq plasmid FTP/HTTPS directories.  
* **Metadata Extraction**: Parses GenBank files to extract organism, taxonomy, plasmid name, strain, host, collection date, and other key metadata.  
* **Flexible Filtering**: Filter sequences by:
  - Organism or Genus
  - NCBI Taxonomy ID
  - Strain, Isolate, Host, Plasmid Name, Geographic Location, Isolation Source
  - Sequence properties (minimum/maximum length, topology: circular/linear)
  - Record date or collection date
* **Combining & Output**: Generates a single curated multi-FASTA file and a CSV metadata table.  
* **Reporting**: Produces a detailed summary report with counts of total records, filtered records by reason, and sequences written.  
* **Development Mode**: Quick test download of a single file set for rapid testing.  
* **Reprocessing Existing Data**: Skip download and re-run filtering/reporting on already downloaded files.  

---

## Installation

### Prerequisites

* Python 3.9+
* Internet access required for downloads and NCBI Entrez queries.

### Using PyPI

```bash
pip install refseq-plasmid-dl
```

### Using Bioconda

```bash
conda install -c bioconda refseq-plasmid-dl
```

### From Source

```bash
git clone https://github.com/yourusername/refseq-plasmid-dl.git  
cd refseq-plasmid-dl  
pip install .
```

---

## Usage

The main command is:

```
refseq-plasmid-dl
```

### Basic Download and Report

Download all RefSeq plasmids and generate metadata/report:

```bash
refseq-plasmid-dl
```

### Curating Specific Organism or Topology

Download and retain **circular plasmids** for a specific organism, e.g., *Salmonella*:

```bash
refseq-plasmid-dl --outdir Salmonella_plasmids --organism Salmonella --topology circular
```

### Reprocessing Existing Files

Skip download and apply new filters to an existing directory:

```bash
refseq-plasmid-dl --indir existing_data --organism Escherichia --topology circular
```

---

## Command-Line Arguments


Argument | Shorthand | Default | Description
-------- | -------- | ------- | -----------
--outdir | -o | refseq_plasmids | Output directory for FASTA files, reports, and metadata.
--indir | -i | None | Use existing download directory, skip FTP/HTTPS download.
--dev-mode | -d | False | Development mode: download a single test file set.
--force |  | False | Force re-download of existing files.
--organism | -s | all | Filter by species/organism (substring match).
--taxid | -t | all | Filter by NCBI Taxonomy ID.
--strain |  | None | Filter by strain.
--isolate |  | None | Filter by isolate.
--host |  | None | Filter by host organism.
--plasmid-name |  | None | Filter by plasmid name.
--geo_loc_name |  | None | Filter by geographic location.
--isolation_source |  | None | Filter by isolation source.
--min-length |  | None | Minimum sequence length (bp).
--max-length |  | None | Maximum sequence length (bp).
--topology |  | circular | Filter by topology: circular, linear, or all.
--min-date |  | None | Include only records updated after YYYY-MM-DD.
--max-date |  | None | Include only records updated before YYYY-MM-DD.
--min-collection-date |  | None | Include only records collected after YYYY-MM-DD.
--max-collection-date |  | None | Include only records collected before YYYY-MM-DD.
--version | -v |  | Show program version.


---

## Output Directory Structure

```text
[OUTDIR]/  
├── plasmids_index.html                 # Saved HTML listing of NCBI plasmid directory  
├── refseq_plasmids/                    # Raw downloaded FASTA and GBFF files  
│   ├── plasmid.*.genomic.fna.gz  
│   └── plasmid.*.genomic.gbff.gz  
├── refseq_plasmids_dl.fasta            # Final curated multi-FASTA  
├── refseq_plasmids_dl_metadata.csv     # Full metadata for filtered plasmids
└── refseq_plasmids_dl_report.csv       # Summary report with filter  
```

---

## Examples

### Download all plasmids and generate report

```bash
refseq-plasmid-dl --topology all
```

### Filter by organism and circular topology

```bash
refseq-plasmid-dl --organism Escherichia --topology circular
```

### Skip download and reprocess existing data

```bash
refseq-plasmid-dl --indir refseq_plasmids --min-length 5000 --max-length 200000
```

### Note on AI Assistance
Parts of this codebase and documentation were drafted with the help of **Google Gemini**. The AI was used primarily for creating the project outline, writing development logic, and generating test cases. The final logic and implementation details have been verified manually.

---

## License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**. See the LICENSE file for full details.
