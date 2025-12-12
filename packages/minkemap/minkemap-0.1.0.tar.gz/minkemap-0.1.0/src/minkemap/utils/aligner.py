import mappy as mp
import logging

logger = logging.getLogger(__name__)


def get_mappy_preset(seq_type: str) -> str:
    seq_type = seq_type.lower()
    mapping = {
        "nanopore": "map-ont",
        "pacbio": "map-pb",
        "hifi": "map-hifi",
        "illumina": "sr",
        "illumina_paired_end": "sr",
        "fasta": "asm5",
        "assembly": "asm5",
    }
    return mapping.get(seq_type, "asm5")


def map_sample(reference_path: str, sample_obj, min_identity=0.0, min_coverage=0.0):
    preset = get_mappy_preset(sample_obj.seq_type)
    logger.info(f"   -> Aligning {sample_obj.name} ({preset})...")

    try:
        aligner = mp.Aligner(reference_path, preset=preset)
    except Exception as e:
        logger.error(f"Failed to load reference: {e}")
        return

    if not aligner:
        logger.error(f"Failed to initialize aligner for {reference_path}")
        return

    for name, seq, qual in mp.fastx_read(sample_obj.file_path):
        hits = aligner.map(seq)
        query_len = len(seq)

        for hit in hits:
            identity = hit.mlen / hit.blen if hit.blen > 0 else 0
            if identity < min_identity:
                continue

            aligned_len = hit.q_en - hit.q_st
            coverage = aligned_len / query_len if query_len > 0 else 0
            if coverage < min_coverage:
                continue

            yield {
                "query_name": name,
                "ref_name": hit.ctg,
                "ref_start": hit.r_st,
                "ref_end": hit.r_en,
                "strand": hit.strand,
                "identity": identity,
                "coverage": coverage,
            }
