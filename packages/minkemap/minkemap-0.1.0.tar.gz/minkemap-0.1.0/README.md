<div align="center">
  <img src="assets/logo.png" alt="MinkeMap Logo" width="220">
  <h1>MinkeMap</h1>

  <a href="https://pypi.org/project/daisyblast/">
    <img src="https://img.shields.io/pypi/v/minkemap?color=blue&label=pypi%20package" alt="PyPI version">
  </a>
  <a href="https://github.com/erinyoung/minkemap/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  </a>
</div>

<br>

---

## Overview

**MinkeMap** is a command-line tool designed to map sequencing data (FASTQ/FASTA) against a reference genome and visualize coverage and identity statistics in a concentric ring layout. It is heavily inspired by [BRIG](https://github.com/happykhan/BRIG) (BLAST Ring Image Generator).

### Key Features
* **Fast Mapping:** Uses `mappy` ([minimap2](https://github.com/lh3/minimap2)) for rapid alignment of Reads or Assemblies.
* **Dynamic Scaling:** Automatically adjusts track width and gaps to fit the canvas, whether you have 3 tracks or 30.
* **Rich Annotations:** Supports GenBank (`.gbk`) features, custom user annotations, and highlight "wedges".
* **Focused on Visuals:** Exports to `.png`, `.svg`, and `.pdf` with customizable DPI and palettes.
* **Data Transparency:** Automatically generates a `summary.csv` and detailed `.bed` coverage files for every run.

## Installation

### Mappy Dependencies
MinkeMap relies on [mappy](https://pypi.org/project/mappy/) (a Python wrapper for [minimap2](https://github.com/lh3/minimap2)), which requires a C compiler and zlib development headers to build. If you encounter errors during installation, ensure these are installed:

Ubuntu/Debian
```bash
sudo apt-get install build-essential zlib1g-dev
```
CentOS/Fedora
```bash
sudo yum install gcc zlib-devel
```

### MinkeMap Installation

From pip

```bash
pip install minkemap
```

From bioconda

```bash
conda install -c bioconda minkemap
```

From source

```bash
git clone https://github.com/yourusername/minkemap.git
cd minkemap
pip install .
```

## Quick Start

1. Basic usage with a GenBank reference and a few samples:

```bash
minkemap \
  -r reference.gbk \
  -i sample1.fastq sample2.fasta \
  --gc-skew \
  --outdir results
```

2. Advanced usage with a manifest for FASTQ files and custom styling

```bash
minkemap \
  -r reference.gbk \
  -f manifest.csv \
  --annotations custom_regions.csv \
  --highlights background_wedges.csv \
  --palette viridis \
  --min-identity 90 \
  --min-coverage 50 \
  --output my_figure.svg
```

## Input Formats

### 1. The Manifest File (`-f`)
Only FASTA files can be read in to MinkeMap with `-i`. For FASTQ files, a csv that lists a desired name for the track, input files (FASTA or FASTQ), and the type of file is required.

```
sample,read1,read2,type
SampleA,data/s1_R1.fq.gz,data/s1_R2.fq.gz,illumina
SampleB,data/s2.fasta,,fasta
SampleC,data/s3.fastq,,nanopore
```

*Supported types:* `illumina`, `nanopore`, `pacbio`, `hifi`, `fasta`, `assembly`.

### 2. Custom Annotations (`--annotations`)
An annotaitons file can be used to draw specific regions of interest on the outermost ring of the plot.

An annotations file is a csv file that lists the reference, start position in relation to the reference, stop position in relation to the reference, a label (optional), and color (optional).

```
reference,start,stop,label,color
3,15000,22000,Coolio region,#eb5c4b
3,35000,38000,Other coolio region,
3,45000,48000,,#357cb0
```

### 3. Highlight Wedges (`--highlights`)

A file for highlights can be supplied. These are semi-transparent "pizza slices" behind all tracks to highlight regions.

```
start,end,color,label
10000,20000,#ffcccc,Important Region
45000,48000,#ccffcc,Another Region
```
## Command Line Options

### Input / Output
* `-r, --reference`: Reference genome (GenBank `.gbk` required for gene arrows, or `.fasta`).
* `-i, --input`: List of input FASTA files.
* `-f, --input-file`: Path to manifest CSV.
* `-o, --output`: Output filename (default: `minkemap_plot.png`). Supports `.svg` and `.pdf`.
* `--outdir`: Directory to save images, logs, and summaries (default: `minkemap_results`).

### Aesthetics
* `--palette`: Color scheme. Accepts presets (`whale`, `viridis`, `plasma`, etc.) or comma-separated hex codes (`#ff0000,#0000ff`).
* `--track-width`: Width of each ring (default: 6). Auto-scales if space is low.
* `--track-gap`: Gap between rings (default: 4). Auto-scales if space is low.
* `--dpi`: Resolution for images (default: 300).
* `--no-backbone`: Hides the central black reference axis.
* `--no-legend`: Hides the legends.
* `--label-size`: Font size for gene labels (default: 6).
* `--title`: Add a title to the top of the plot.

### Features
* `--gc-skew`: Adds a GC Skew track (Blue+/Orange-) in the center.
* `--annotations`: Path to custom annotations CSV.
* `--highlights`: Path to background highlights CSV.
* `--exclude-genes`: Comma-separated list of keywords to hide from the gene track (e.g., `hypothetical,putative`).

### Filters
* `--min-identity`: Minimum % identity (0-100) to display an alignment block.
* `--min-coverage`: Minimum % query coverage (0-100) required to include a read/contig.

## Outputs

Check your output directory for:
1.  **`minkemap_plot.png`**: The circular visualization.
2.  **`summary.csv`**: Detailed metrics for every track (Coverage %, Average Depth, Gene Counts).
3.  **`*.bed` / `*.coverage.csv`**: Raw data files for every track plotted.
4.  **`minkemap.log`**: Full execution log for reproducibility.

**Note:** While MinkeMap streamlines the circular plotting process, it does not aim to replicate the exhaustive customization options of libraries like [PyCirclize](https://github.com/moshi4/pyCirclize) or [BRIG](https://github.com/happykhan/BRIG). Therefore, MinkeMap exports all calculated metrics (coverage, identity, skew) as raw data files (CSV/BED), allowing for downstream workflows or other visualization platforms.

## Gallery & Examples

| Description | Command Used | Output |
| :--- | :--- | :---: |
| Standard visualization of Nanopore reads mapped against a FASTA reference. | `minkemap -r tests/data/3670018.fasta -i tests/data/*fasta` | <img src="assets/example_basic.png" width="300" /> |
| Standard visualization of Nanopore reads mapped against a GenBank reference. | `minkemap -r tests/data/3670018.gbk -i tests/data/*fasta` | <img src="assets/example_basic_gbk.png" width="300" /> |
| Adding a **GC Skew** track (center) and filtering to the rings with **>90% coverage**. | `minkemap -r ./tests/data/3670018.gbk -i tests/data/*fasta --min-coverage 90 --gc-skew` | <img src="assets/example_analytics.png" width="300" /> |
| Removing the black reference backbone for a cleaner look, applying the `viridis` palette, and hiding "hypothetical" proteins from the gene track. | `minkemap -r ./tests/data/3670018.gbk -i tests/data/*fasta --no-backbone --palette viridis --exclude-genes "hypothetical"` | <img src="assets/example_clean.png" width="300" /> |
| Uses a **CSV Manifest** to map multiple samples simultaneously and a **Highlights** file to mark regions of interest (e.g., AMR genes). | `minkemap -r ./tests/data/3670018.gbk -f tests/data/manifest.csv --highlights tests/data/highlights.csv` | <img src="assets/example_complex.png" width="300" /> |

## Why "MinkeMap"

The visual identity of MinkeMap draws inspiration from a local Salt Lake City landmark: the 'Out of the Blue' [whale sculpture](https://en.wikipedia.org/wiki/Out_of_the_Blue_(sculpture)) situated at the 9th and 9th roundabout. There is a natural geometric parallel between the circular traffic intersection and the concentric rings typical of genomic visualizations (such as [BRIG plots](https://github.com/happykhan/BRIG)). MinkeMap leverages this connection, mirroring the roundabout's form and the sculpture's vibrancy to bring a unique aesthetic to circular genome analysis.

And, yes, we are aware the sculpture is of a Humpback whale. We simply couldn't resist the alliteration of Minke with [Minimap2](https://github.com/lh3/minimap2), the alignment tool powering this package.

## AI Acknowledgement
MinkeMap was developed with the assistance of Google's Gemini for code refactoring, test suite generation, and CI/CD configuration. All AI-generated code has been reviewed, tested, and validated by the authors.

## License

Distributed under the MIT License. See `LICENSE` for more information.
