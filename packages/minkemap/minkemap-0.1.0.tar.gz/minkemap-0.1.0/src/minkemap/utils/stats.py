import numpy as np
import mappy as mp


def get_tick_interval(total_size):
    """Determine tick interval based on total size."""
    if total_size < 50000:
        return 2000
    if total_size < 200000:
        return 10000
    if total_size < 1000000:
        return 50000
    if total_size < 5000000:
        return 200000
    return 1000000


def get_dynamic_alpha(identity, min_threshold=0.0):
    """Map identity to alpha for visualization."""
    if identity >= 0.99:
        return 1.0
    baseline = max(min_threshold, 0.70)
    if baseline >= 1.0:
        return 1.0
    normalized = (identity - baseline) / (1.0 - baseline)
    return max(0.2, min(normalized, 1.0))


def calculate_depth(hits, sector_length, sector_name, window=500):
    """
    Calculate binned depth coverage.
    Returns: x_coords, depth_binned, count, bases_covered, total_depth
    """
    depth_arr = np.zeros(sector_length, dtype=int)
    count = 0
    for hit in hits:
        if hit["ref_name"] == sector_name:
            # Clip coords to be safe
            s = max(0, hit["ref_start"])
            e = min(sector_length, hit["ref_end"])
            depth_arr[s:e] += 1
            count += 1

    bases_covered = np.count_nonzero(depth_arr)
    total_depth = np.sum(depth_arr)

    if count == 0:
        return None, None, 0, 0, 0

    limit = (len(depth_arr) // window) * window
    depth_binned = depth_arr[:limit].reshape(-1, window).mean(axis=1)
    x_coords = np.arange(0, limit, window) + (window / 2)
    return x_coords, depth_binned, count, bases_covered, total_depth


def calculate_identity_stats(hits, sector_length, sector_name):
    """
    Calculates exact coverage (handling overlaps) and weighted identity.
    Returns: bases_covered, weighted_id_sum, total_aligned_len
    """
    mask = np.zeros(sector_length, dtype=bool)
    weighted_id_sum = 0.0
    total_aligned_len = 0

    # Filter hits for this sector
    # (In a highly optimized tool we wouldn't loop hits every time, but for plasmids this is fine)
    hits_in_sector = [h for h in hits if h["ref_name"] == sector_name]

    for hit in hits_in_sector:
        s = max(0, hit["ref_start"])
        e = min(sector_length, hit["ref_end"])

        # Mark coverage mask
        mask[s:e] = True

        # Identity calc
        aln_len = e - s
        weighted_id_sum += hit["identity"] * aln_len
        total_aligned_len += aln_len

    bases_covered = np.count_nonzero(mask)
    return bases_covered, weighted_id_sum, total_aligned_len


def calculate_gc_skew(fasta_path, window_size=500, step_size=250):
    """Calculate GC Skew ((G-C)/(G+C)) in sliding windows."""
    skew_data = {}

    for name, seq, _ in mp.fastx_read(fasta_path):
        seq = seq.upper()
        skew_vals = []
        x_coords = []

        for i in range(0, len(seq) - window_size, step_size):
            subseq = seq[i : i + window_size]
            g = subseq.count("G")
            c = subseq.count("C")

            if g + c == 0:
                skew = 0.0
            else:
                skew = (g - c) / (g + c)

            skew_vals.append(skew)
            x_coords.append(i + (window_size / 2))

        skew_data[name] = (np.array(x_coords), np.array(skew_vals))

    return skew_data
