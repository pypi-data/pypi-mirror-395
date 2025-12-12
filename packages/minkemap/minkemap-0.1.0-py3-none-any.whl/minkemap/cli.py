import argparse
import sys
import os
import logging
from minkemap.utils.parser import parse_inputs
from minkemap.utils.aligner import map_sample
from minkemap.genomering import GenomeRing
from minkemap import __version__

# Initial basic config (will be updated after outdir is created)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("MinkeMap")


def main():
    parser = argparse.ArgumentParser(
        description="MinkeMap: Circular Genome Visualization Tool"
    )

    # Meta
    parser.add_argument(
        "-v", "--version", action="version", version=f"MinkeMap v{__version__}"
    )

    # Input / Output
    parser.add_argument(
        "-r", "--reference", required=True, help="Reference genome (FASTA or GenBank)"
    )
    parser.add_argument(
        "-i", "--input", nargs="+", help="Input sequencing files (FASTQ/FASTA)"
    )
    parser.add_argument(
        "-f", "--input-file", help="Manifest CSV file (cols: sample,read1,read2,type)"
    )
    parser.add_argument(
        "-o", "--output", default="minkemap_plot.png", help="Output filename"
    )
    parser.add_argument(
        "--outdir",
        default="minkemap_results",
        help="Directory to save all output files",
    )

    # Aesthetics
    parser.add_argument(
        "--track-width",
        type=float,
        default=6,
        help="Width of each track ring (default: 6)",
    )
    parser.add_argument(
        "--track-gap", type=float, default=4, help="Gap between tracks (default: 4)"
    )
    parser.add_argument("--palette", default="whale", help="Color palette")
    parser.add_argument("--dpi", type=int, default=300, help="Image resolution")
    parser.add_argument("--title", help="Plot title")
    parser.add_argument(
        "--no-legend", action="store_true", help="Hide the sample legend"
    )
    parser.add_argument(
        "--no-backbone", action="store_true", help="Hide the black reference backbone"
    )
    parser.add_argument(
        "--label-size", type=int, default=6, help="Font size for gene/annotation labels"
    )

    # Features
    parser.add_argument(
        "--annotations",
        help="CSV file for custom regions (cols: reference,start,stop,label,color)",
    )
    parser.add_argument(
        "--highlights",
        help="CSV file for background wedges (cols: start,end,color,label)",
    )
    parser.add_argument(
        "--gc-skew", action="store_true", help="Add a GC Skew track to the center"
    )
    parser.add_argument(
        "--no-save-data", action="store_true", help="Do not generate BED/CSV data files"
    )

    # Filters
    parser.add_argument(
        "--min-identity", type=float, default=0, help="Minimum identity %% (0-100)"
    )
    parser.add_argument(
        "--min-coverage",
        type=float,
        default=0,
        help="Minimum query coverage %% (0-100)",
    )
    parser.add_argument(
        "--exclude-genes",
        help="Comma-separated list of terms to exclude from gene track (e.g. 'hypothetical,putative')",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    min_id_decimal = args.min_identity / 100.0
    min_cov_decimal = args.min_coverage / 100.0
    should_save = not args.no_save_data

    # 1. Create Output Directory & Log File
    try:
        os.makedirs(args.outdir, exist_ok=True)
        # Add File Handler to log to disk
        log_path = os.path.join(args.outdir, "minkemap.log")
        file_handler = logging.FileHandler(log_path, mode="w")
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(file_handler)

        if args.outdir != ".":
            logger.info(f"Output directory: {args.outdir}/")
            logger.info(f"Log file: {log_path}")

    except OSError as e:
        logger.error(f"Error creating directory {args.outdir}: {e}")
        sys.exit(1)

    # 2. Parse Inputs
    samples = parse_inputs(args.input, args.input_file)
    if not samples:
        logger.error("No inputs provided. Use -i or -f.")
        sys.exit(1)

    total_tracks = len(samples)
    if args.gc_skew:
        total_tracks += 1
    total_tracks += 1  # Genes
    if args.annotations:
        total_tracks += 1

    # 3. Init Ring
    ring = GenomeRing(
        args.reference,
        outdir=args.outdir,
        track_width=args.track_width,
        track_gap=args.track_gap,
        palette=args.palette,
        total_tracks=total_tracks,
        no_backbone=args.no_backbone,  # <--- New Arg
        label_size=args.label_size,  # <--- New Arg
    )

    logger.info(f"Reference loaded. Mapping {len(samples)} samples...")
    if args.min_identity > 0 or args.min_coverage > 0:
        logger.info(
            f"   (Filters: Identity >= {args.min_identity}%, Coverage >= {args.min_coverage}%)"
        )

    # 4. Features
    if args.highlights:
        ring.add_highlights(args.highlights)

    if args.gc_skew:
        ring.add_gc_skew_track()

    # 5. Map & Draw
    for sample in samples:
        hits = map_sample(
            ring.ref_path,
            sample,
            min_identity=min_id_decimal,
            min_coverage=min_cov_decimal,
        )

        is_reads = sample.seq_type.lower() in [
            "nanopore",
            "illumina",
            "illumina_paired_end",
            "pacbio",
            "hifi",
        ]
        plot_mode = "coverage" if is_reads else "rect"

        ring.add_track(
            sample.name,
            hits,
            plot_type=plot_mode,
            min_identity=min_id_decimal,
            min_coverage=min_cov_decimal,
            save_data=should_save,
        )

    # 6. Genes (with filtering)
    exclude_list = (
        [x.strip() for x in args.exclude_genes.split(",")] if args.exclude_genes else []
    )
    ring.add_genes_track(exclude_list=exclude_list)

    if args.annotations:
        ring.add_custom_track(args.annotations)

    # 7. Save
    ring.save(args.output, dpi=args.dpi, title=args.title, no_legend=args.no_legend)

    full_output_path = os.path.join(args.outdir, args.output)
    logger.info(f"Done! Saved to {full_output_path}")


if __name__ == "__main__":
    main()
