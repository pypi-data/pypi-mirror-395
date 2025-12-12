import mappy as mp
from pycirclize import Circos
import numpy as np
import sys
import csv
import os
import logging
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from minkemap.utils import stats
from minkemap.utils.parser import (
    parse_reference,
    parse_custom_annotations,
    parse_highlights,
)

logger = logging.getLogger(__name__)


class GenomeRing:
    """
    Circular genome visualization for reference genomes and alignments.
    """

    def __init__(
        self,
        reference_path,
        outdir=".",
        track_width=6,
        track_gap=4,
        palette="whale",
        total_tracks=0,
        no_backbone=False,
        label_size=6,
    ):
        self.outdir = outdir
        self.ref_path, self.gbk_records = parse_reference(reference_path)
        self.sectors = {}
        self.summary_data = []
        self.legend_handles = []

        # Aesthetics
        self.track_width = track_width
        self.gap = track_gap
        self.label_size = label_size
        self.colors = self._get_palette(palette)

        self.count = 0
        self.global_min_identity = 0.0

        # --- DYNAMIC RESIZING ---
        start_r = 20
        max_r = 98
        available = max_r - start_r

        needed = total_tracks * (track_width + track_gap)

        if total_tracks > 0 and needed > available:
            scale = available / needed
            self.track_width = max(0.5, track_width * scale)
            self.gap = max(0.2, track_gap * scale)
            logger.warning(
                f"Auto-scaling tracks: Width {track_width}->{self.track_width:.2f}, Gap {track_gap}->{self.gap:.2f}"
            )
        else:
            self.track_width = track_width
            self.gap = track_gap

        try:
            for name, seq, _ in mp.fastx_read(self.ref_path):
                self.sectors[name] = len(seq)
        except Exception as e:
            logger.error(f"Error reading reference FASTA: {e}")
            sys.exit(1)

        if not self.sectors:
            logger.error(f"No sequences found in {self.ref_path}")
            sys.exit(1)

        self.circos = Circos(self.sectors, space=5)

        # Backbone
        bb_thick = max(1, self.track_width * 0.15)
        ref_start = start_r - 5
        ref_end = ref_start + bb_thick

        total_size = sum(self.sectors.values())
        tick_interval = stats.get_tick_interval(total_size)

        for sector in self.circos.sectors:
            track = sector.add_track((ref_start, ref_end))

            # --- FIX: Hide backbone if requested ---
            if no_backbone:
                track.axis(fc="none", ec="none", lw=0)
            else:
                track.axis(fc="black", ec="black", lw=0, alpha=1.0)

            track.xticks_by_interval(
                interval=tick_interval,
                label_size=6,
                label_orientation="vertical",
                outer=False,
                tick_length=2,
                label_formatter=self._format_tick_label,
            )

        self.current_r = start_r

    def _format_tick_label(self, value):
        if value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.1f} Gb"
        elif value >= 1_000_000:
            return f"{value / 1_000_000:.1f} Mb"
        elif value >= 1_000:
            return f"{value / 1_000:.0f} kb"
        return f"{value} bp"

    def _get_palette(self, name_or_list):
        whale_palette = [
            "#acdbef",
            "#f6ac49",
            "#9e6586",
            "#9285b3",
            "#265984",
            "#e87451",
            "#357cb0",
            "#e3d371",
            "#eb5c4b",
            "#eba9c3",
            "#5b7c46",
            "#d6cb4d",
            "#b68386",
            "#4fa4a5",
            "#dcc5a5",
        ]
        if name_or_list == "whale":
            return whale_palette
        if "," in name_or_list or name_or_list.startswith("#"):
            return [c.strip() for c in name_or_list.split(",")]
        try:
            cmap = matplotlib.colormaps.get_cmap(name_or_list)
            return [
                matplotlib.colors.to_hex(cmap(i)) for i in np.linspace(0.1, 0.9, 15)
            ]
        except ValueError:
            logger.warning(
                f"Palette '{name_or_list}' not found. Using default 'whale'."
            )
            return whale_palette

    def add_highlights(self, csv_file):
        if not csv_file:
            return
        highlights = parse_highlights(csv_file)
        if not highlights:
            return

        logger.info("   Plotting Highlight Wedges...")
        largest_sector_name = max(self.sectors, key=self.sectors.get)
        sector = self.circos.get_sector(largest_sector_name)
        track = sector.add_track((0, 100))
        track.axis(fc="none", ec="none", lw=0)

        for h in highlights:
            track.rect(h.start, h.end, color=h.color, alpha=0.3, ec="none", zorder=0)
            label = h.label if h.label else "Region of Interest"
            self.legend_handles.append(
                mpatches.Patch(color=h.color, alpha=0.3, label=label)
            )

    def add_gc_skew_track(self):
        if self.current_r + self.track_width > 99:
            logger.warning("Skipping GC Skew (Out of space)")
            return

        logger.info("   Plotting GC Skew...")
        r_inner, r_outer = self.current_r, self.current_r + self.track_width

        skew_data = stats.calculate_gc_skew(self.ref_path)
        all_vals = []
        for _, (_, y) in skew_data.items():
            all_vals.extend(y)

        abs_max = float(np.max(np.abs(all_vals))) if all_vals else 0.1
        if abs_max == 0:
            abs_max = 0.1

        largest = max(self.sectors, key=self.sectors.get)
        self.circos.get_sector(largest).text(
            "GC Skew", r=r_inner - (self.gap / 2), size=self.label_size, color="black"
        )

        for sector in self.circos.sectors:
            track = sector.add_track((r_inner, r_outer))
            track.axis(fc="none", ec="grey", lw=0.5, alpha=0.3)
            if sector.name in skew_data:
                x, y = skew_data[sector.name]
                y = np.nan_to_num(y)
                track.fill_between(
                    x,
                    np.maximum(y, 0),
                    0,
                    vmin=-abs_max,
                    vmax=abs_max,
                    color="#265984",
                    alpha=0.8,
                )
                track.fill_between(
                    x,
                    np.minimum(y, 0),
                    0,
                    vmin=-abs_max,
                    vmax=abs_max,
                    color="#e87451",
                    alpha=0.8,
                )

        self.current_r += self.track_width + self.gap
        self.count += 1

        self.legend_handles.append(mpatches.Patch(color="#265984", label="GC Skew (+)"))
        self.legend_handles.append(mpatches.Patch(color="#e87451", label="GC Skew (-)"))

        self.summary_data.append(
            {
                "Track": "GC Skew",
                "Type": "Metric",
                "Color": "Blue/Orange",
                "Status": "Reference",
                "Ref_Covered_Pct": 100,
                "Avg_Depth": "",
                "Avg_Identity": "",
                "Gene_Count": "",
            }
        )

    def add_track(
        self,
        sample_name,
        hits,
        plot_type="rect",
        min_identity=0.0,
        min_coverage=0.0,
        save_data=True,
    ):
        self.global_min_identity = min_identity

        if self.current_r + self.track_width > 99:
            logger.warning(f"Skipping {sample_name} (Out of space)")
            return

        all_hits = list(hits)

        if not all_hits:
            status = (
                "Filtered Out"
                if (min_identity > 0 or min_coverage > 0)
                else "No Mapping"
            )
            logger.warning(f"      Skipping {sample_name} ({status})")
            type_label = (
                "Coverage (FASTQ)" if plot_type == "coverage" else "Identity (FASTA)"
            )
            self.summary_data.append(
                {
                    "Track": sample_name,
                    "Type": type_label,
                    "Color": "None",
                    "Status": status,
                    "Ref_Covered_Pct": "0",
                    "Avg_Depth": "0",
                    "Avg_Identity": "0",
                    "Gene_Count": "",
                }
            )
            return

        logger.info(f"   Plotting {sample_name} as '{plot_type}'...")
        r_inner, r_outer = self.current_r, self.current_r + self.track_width
        color = self.colors[self.count % len(self.colors)]

        sample_tracks = {}
        for sector in self.circos.sectors:
            track = sector.add_track((r_inner, r_outer))
            track.axis(fc="none", ec="grey", lw=0.5, alpha=0.3)
            sample_tracks[sector.name] = track

        total_genome_len = sum(self.sectors.values())
        total_bases_covered = 0
        metric_accumulator = 0
        metric_denom = 0

        if plot_type == "coverage":
            if save_data:
                filename = os.path.join(self.outdir, f"{sample_name}.coverage.csv")
                with open(filename, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["chrom", "start", "end", "avg_depth"])
                    for s_name, s_len in self.sectors.items():
                        x, y, _, _, _ = stats.calculate_depth(all_hits, s_len, s_name)
                        if x is not None:
                            for i, val in enumerate(y):
                                writer.writerow(
                                    [
                                        s_name,
                                        int(x[i] - 250),
                                        int(x[i] + 250),
                                        f"{val:.2f}",
                                    ]
                                )
                logger.info(f"      Exported coverage data to {filename}")

            for s_name, s_len in self.sectors.items():
                x, y, count, covered, total_depth = stats.calculate_depth(
                    all_hits, s_len, s_name
                )
                total_bases_covered += covered
                metric_accumulator += total_depth

                if x is not None and count > 0:
                    track = sample_tracks[s_name]
                    track.fill_between(x, y, color=color, alpha=0.9)
                    track.line(x, y, color=color, lw=0.5)

            self.legend_handles.append(
                mpatches.Patch(color=color, label=f"{sample_name} (Cov)")
            )

            pct_covered = (total_bases_covered / total_genome_len) * 100
            avg_depth = metric_accumulator / total_genome_len

            self.summary_data.append(
                {
                    "Track": sample_name,
                    "Type": "Coverage (FASTQ)",
                    "Color": color,
                    "Status": "Pass",
                    "Ref_Covered_Pct": f"{pct_covered:.2f}",
                    "Avg_Depth": f"{avg_depth:.2f}x",
                    "Avg_Identity": "",
                    "Gene_Count": "",
                }
            )

        else:
            if save_data:
                filename = os.path.join(self.outdir, f"{sample_name}.bed")
                with open(filename, "w") as f:
                    f.write("#chrom\tstart\tend\tname\tidentity\n")
                    for hit in all_hits:
                        f.write(
                            f"{hit['ref_name']}\t{hit['ref_start']}\t{hit['ref_end']}\t{sample_name}\t{hit['identity']:.4f}\n"
                        )
                logger.info(f"      Exported BED data to {filename}")

            for hit in all_hits:
                if hit["ref_name"] in sample_tracks:
                    alpha_val = stats.get_dynamic_alpha(hit["identity"], min_identity)
                    sample_tracks[hit["ref_name"]].rect(
                        hit["ref_start"],
                        hit["ref_end"],
                        color=color,
                        alpha=alpha_val,
                        ec="none",
                    )

            for s_name, s_len in self.sectors.items():
                covered, weighted_id, aligned_len = stats.calculate_identity_stats(
                    all_hits, s_len, s_name
                )
                total_bases_covered += covered
                metric_accumulator += weighted_id
                metric_denom += aligned_len

            self.legend_handles.append(
                mpatches.Patch(color=color, label=f"{sample_name} (ID)")
            )

            pct_covered = (total_bases_covered / total_genome_len) * 100
            avg_ident = (
                (metric_accumulator / metric_denom * 100) if metric_denom > 0 else 0
            )

            self.summary_data.append(
                {
                    "Track": sample_name,
                    "Type": "Identity (FASTA)",
                    "Color": color,
                    "Status": "Pass",
                    "Ref_Covered_Pct": f"{pct_covered:.2f}",
                    "Avg_Depth": "",
                    "Avg_Identity": f"{avg_ident:.2f}%",
                    "Gene_Count": "",
                }
            )

        largest = max(self.sectors, key=self.sectors.get)
        self.circos.get_sector(largest).text(
            sample_name, r=r_inner - (self.gap / 2), size=self.label_size, color="black"
        )
        self.current_r += self.track_width + self.gap
        self.count += 1

    # --- UPDATED: exclude_list ---
    def add_genes_track(self, exclude_list=[]):
        if not self.gbk_records:
            return
        logger.info("   Plotting Gene Annotations...")
        if self.current_r + self.track_width > 99:
            logger.warning("Skipping Annotations (Out of space)")
            return

        r_inner, r_outer = self.current_r, self.current_r + self.track_width
        gene_count = 0
        for sector in self.circos.sectors:
            if sector.name not in self.gbk_records:
                continue
            track = sector.add_track((r_inner, r_outer))
            track.axis(fc="none", ec="none", lw=0)

            # --- FEATURE FILTERING LOGIC ---
            all_cds = [
                f for f in self.gbk_records[sector.name].features if f.type == "CDS"
            ]
            filtered_cds = []

            for f in all_cds:
                # Get qualifiers (gene name, product, etc)
                product = f.qualifiers.get("product", [""])[0].lower()
                gene = f.qualifiers.get("gene", [""])[0].lower()

                # Check if any forbidden term is in the product or gene name
                is_excluded = False
                for term in exclude_list:
                    if term.lower() in product or term.lower() in gene:
                        is_excluded = True
                        break

                if not is_excluded:
                    filtered_cds.append(f)

            gene_count += len(filtered_cds)

            if filtered_cds:
                track.genomic_features(
                    filtered_cds, plotstyle="arrow", color="black", lw=0.5
                )

        self.summary_data.append(
            {
                "Track": "Annotations",
                "Type": "Genes",
                "Color": "Black",
                "Status": "Reference",
                "Ref_Covered_Pct": "",
                "Avg_Depth": "",
                "Avg_Identity": "",
                "Gene_Count": str(gene_count),
            }
        )
        largest = max(self.sectors, key=self.sectors.get)
        self.circos.get_sector(largest).text(
            "Genes", r=r_inner - (self.gap / 2), size=self.label_size, color="black"
        )
        self.current_r += self.track_width + self.gap

    def add_custom_track(self, annotation_file):
        if not annotation_file:
            return
        annotations = parse_custom_annotations(annotation_file)
        if not annotations:
            return

        logger.info("   Plotting Custom Annotations...")
        if self.current_r + self.track_width > 99:
            logger.warning("Skipping Custom Track (Out of space)")
            return

        r_inner, r_outer = self.current_r, self.current_r + self.track_width
        grouped = {}
        for ann in annotations:
            if ann.chrom not in grouped:
                grouped[ann.chrom] = []
            grouped[ann.chrom].append(ann)

        found_any = False
        genome_ids = list(self.sectors.keys())
        csv_ids = list(grouped.keys())
        for s_name in genome_ids:
            if s_name in grouped:
                found_any = True

        if not found_any:
            logger.warning("CUSTOM ANNOTATION MISMATCH!")
            logger.warning(f"   Your Genome IDs are: {genome_ids}")
            logger.warning(f"   Your CSV IDs are:    {csv_ids}")
            logger.warning(
                "   Please update the 'reference' column in your CSV to match the Genome IDs exactly."
            )

        for sector in self.circos.sectors:
            track = sector.add_track((r_inner, r_outer))
            track.axis(fc="none", ec="none", lw=0)
            if sector.name in grouped:
                for ann in grouped[sector.name]:
                    track.rect(
                        ann.start, ann.end, color=ann.color, alpha=1.0, ec="none"
                    )
                    if ann.label:
                        mid = (ann.start + ann.end) / 2
                        track.text(
                            ann.label,
                            x=mid,
                            r=r_outer + 1.5,
                            size=self.label_size,
                            color=ann.color,
                            orientation="horizontal",
                            va="bottom",
                            ha="center",
                        )

        largest = max(self.sectors, key=self.sectors.get)
        self.circos.get_sector(largest).text(
            "Custom", r=r_inner - (self.gap / 2), size=self.label_size, color="black"
        )
        self.current_r += self.track_width + self.gap
        self.summary_data.append(
            {
                "Track": "Custom Annotations",
                "Type": "User Regions",
                "Color": "Various",
                "Status": "Included",
                "Ref_Covered_Pct": "",
                "Avg_Depth": "",
                "Avg_Identity": "",
                "Gene_Count": str(len(annotations)),
            }
        )

    def save(self, output_filename, dpi=300, title=None, no_legend=False):
        full_path = os.path.join(self.outdir, output_filename)
        logger.info(f"Saving plot to {full_path}...")
        if full_path.endswith(".svg"):
            matplotlib.rcParams["svg.fonttype"] = "none"

        fig = self.circos.plotfig()
        if title:
            fig.suptitle(title, fontsize=16, y=1.05)

        if not no_legend:
            baseline = max(self.global_min_identity, 0.70)
            points = sorted(
                list(set([0.99, (0.99 + baseline) / 2, baseline])), reverse=True
            )
            id_handles = [
                mpatches.Patch(
                    color="grey",
                    alpha=stats.get_dynamic_alpha(pt, self.global_min_identity),
                    label="100% Identity" if pt >= 0.99 else f"{int(pt*100)}% Identity",
                )
                for pt in points
            ]
            l1 = fig.legend(
                handles=id_handles,
                loc="upper right",
                bbox_to_anchor=(1.02, 1.0),
                title="Identity Map",
                frameon=False,
            )
            fig.add_artist(l1)

            if self.legend_handles:
                fig.legend(
                    handles=self.legend_handles,
                    loc="upper left",
                    bbox_to_anchor=(1.02, 0.8),
                    title="Tracks",
                    frameon=False,
                )

        fig.savefig(full_path, dpi=dpi, bbox_inches="tight", pad_inches=0.5)

        csv_path = os.path.join(self.outdir, "summary.csv")
        logger.info(f"Saving summary table to {csv_path}...")
        cols = [
            "Track",
            "Type",
            "Status",
            "Color",
            "Ref_Covered_Pct",
            "Avg_Depth",
            "Avg_Identity",
            "Gene_Count",
        ]
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=cols)
            writer.writeheader()
            writer.writerows(self.summary_data)
