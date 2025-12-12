import pytest
import numpy as np
from minkemap.utils import parser, stats

# --- PARSER TESTS ---


def test_parse_manifest(manifest_path):
    """Test parsing the CSV manifest from tests/data."""
    samples = parser.parse_inputs(input_files=None, manifest_file=str(manifest_path))

    # Based on your likely manifest structure
    assert len(samples) > 0
    # Check the first sample has fields populated
    assert samples[0].name
    assert samples[0].file_path
    assert samples[0].seq_type


def test_parse_highlights(highlights_path):
    """Test parsing the highlights CSV."""
    highlights = parser.parse_highlights(str(highlights_path))

    assert isinstance(highlights, list)
    if len(highlights) > 0:
        assert hasattr(highlights[0], "start")
        assert hasattr(highlights[0], "color")


def test_parse_inputs_missing_file():
    """Ensure system exits or errors on bad file path."""
    with pytest.raises(SystemExit):
        parser.parse_inputs(["ghost_file.fastq"], None)


# --- STATS TESTS ---


def test_get_dynamic_alpha():
    """Test transparency calculation."""
    assert stats.get_dynamic_alpha(1.0) == 1.0
    assert stats.get_dynamic_alpha(0.5) < 1.0
    assert stats.get_dynamic_alpha(0.99) == 1.0


def test_tick_interval():
    """Test logic for axis tick spacing."""
    assert stats.get_tick_interval(40000) == 2000
    assert stats.get_tick_interval(6000000) == 1000000
