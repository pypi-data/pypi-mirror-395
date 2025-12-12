import pytest
import sys
import os
from unittest.mock import patch
from minkemap.cli import main


def test_full_pipeline_gbk_manifest(data_dir, reference_gbk, manifest_path, tmp_path):
    """
    Runs the full pipeline using:
    - Real GenBank file (3670018.gbk)
    - Real Manifest (manifest.csv)
    - Output to a temporary folder created by pytest
    """

    # Define output paths
    output_dir = tmp_path / "results"

    # Construct command line arguments
    test_args = [
        "minkemap",
        "-r",
        str(reference_gbk),
        "-f",
        str(manifest_path),
        "--outdir",
        str(output_dir),
        "--title",
        "Integration Test Plot",
        "--gc-skew",
        "--no-backbone",  # Testing the option you added
        "--verbose",
    ]

    # Patch sys.argv to simulate command line execution
    with patch.object(sys, "argv", test_args):
        # We wrap this in a try/except because main() uses sys.exit(1) on failure
        try:
            main()
        except SystemExit as e:
            # If it exits with 0, that's fine (help menu or version).
            # If it exits with 1, the test failed.
            assert e.value.code == 0

    # --- VERIFICATION ---

    # 1. Check if the plot was created
    expected_plot = output_dir / "minkemap_plot.png"
    assert expected_plot.exists(), "Plot image was not generated"
    assert expected_plot.stat().st_size > 0, "Plot image is empty"

    # 2. Check if the log was created
    expected_log = output_dir / "minkemap.log"
    assert expected_log.exists()

    # 3. Check if Summary CSV was created
    expected_csv = output_dir / "summary.csv"
    assert expected_csv.exists()


def test_cli_version_flag():
    """Test that -v / --version runs without crashing."""
    with patch.object(sys, "argv", ["minkemap", "--version"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
