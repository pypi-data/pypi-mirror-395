import pandas as pd
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, Dict
from Bio import SeqIO
import tempfile
import os
import atexit
import sys
import logging

logger = logging.getLogger(__name__)


@dataclass
class Sample:
    name: str
    file_path: str
    read2_path: Optional[str] = None
    seq_type: str = "fasta"


@dataclass
class CustomAnnotation:
    chrom: str
    start: int
    end: int
    label: Optional[str] = None
    color: str = "black"


# --- NEW CLASS ---
@dataclass
class Highlight:
    start: int
    end: int
    color: str = "gray"
    label: Optional[str] = None


def parse_inputs(input_files: List[str], manifest_file: str) -> List[Sample]:
    samples = []

    # --- UPDATE THIS BLOCK ---
    if input_files:
        for f in input_files:
            if not os.path.exists(f):
                logger.error(f"Input file not found: {f}")
                sys.exit(1)
            samples.append(Sample(name=Path(f).stem, file_path=str(Path(f))))
    # -------------------------

    if manifest_file:
        if not os.path.exists(manifest_file):
            logger.error(f"Manifest file not found: {manifest_file}")
            sys.exit(1)

        try:
            df = pd.read_csv(manifest_file)
            for _, row in df.iterrows():
                r2 = row["read2"] if "read2" in row and pd.notna(row["read2"]) else None
                samples.append(
                    Sample(
                        name=row["sample"],
                        file_path=row["read1"],
                        read2_path=r2,
                        seq_type=row["type"],
                    )
                )
        except Exception as e:
            logger.error(f"Error parsing manifest: {e}")
            sys.exit(1)
    return samples


def parse_reference(reference_path: str) -> Tuple[str, Dict]:
    gbk_records = {}
    final_path = reference_path
    if reference_path.endswith((".gbk", ".gb", ".gbf", ".gbff")):
        logger.info("   Parsing GenBank features...")
        try:
            records = list(SeqIO.parse(reference_path, "genbank"))
            for r in records:
                gbk_records[r.id] = r
            fd, temp_path = tempfile.mkstemp(suffix=".fasta")
            os.close(fd)
            with open(temp_path, "w") as f:
                SeqIO.write(records, f, "fasta")
            final_path = temp_path
            atexit.register(
                lambda: os.unlink(temp_path) if os.path.exists(temp_path) else None
            )
        except Exception as e:
            logger.error(f"Error parsing GenBank file: {e}")
            sys.exit(1)
    return final_path, gbk_records


def parse_custom_annotations(csv_path: str) -> List[CustomAnnotation]:
    annotations = []
    if not csv_path:
        return annotations
    try:
        df = pd.read_csv(csv_path)
        df.columns = [c.lower().strip() for c in df.columns]
        required = {"reference", "start", "stop"}
        if not required.issubset(df.columns):
            logger.error(f"Custom annotation CSV must contain columns: {required}")
            sys.exit(1)
        for _, row in df.iterrows():
            label = (
                str(row["label"]) if "label" in row and pd.notna(row["label"]) else None
            )
            color = (
                str(row["color"])
                if "color" in row and pd.notna(row["color"])
                else "black"
            )
            annotations.append(
                CustomAnnotation(
                    chrom=str(row["reference"]),
                    start=int(row["start"]),
                    end=int(row["stop"]),
                    label=label,
                    color=color,
                )
            )
    except Exception as e:
        logger.error(f"Error parsing annotation file: {e}")
        sys.exit(1)
    return annotations


# --- NEW FUNCTION ---
def parse_highlights(csv_path: str) -> List[Highlight]:
    highlights = []
    if not csv_path:
        return highlights
    try:
        df = pd.read_csv(csv_path)
        df.columns = [c.lower().strip() for c in df.columns]
        required = {"start", "end"}
        if not required.issubset(df.columns):
            logger.error(f"Highlights CSV must contain columns: {required}")
            sys.exit(1)
        for _, row in df.iterrows():
            color = (
                str(row["color"])
                if "color" in row and pd.notna(row["color"])
                else "#ffe5e5"
            )  # Default light red
            label = (
                str(row["label"]) if "label" in row and pd.notna(row["label"]) else None
            )
            highlights.append(
                Highlight(
                    start=int(row["start"]),
                    end=int(row["end"]),
                    color=color,
                    label=label,
                )
            )
    except Exception as e:
        logger.error(f"Error parsing highlights file: {e}")
        sys.exit(1)
    return highlights
