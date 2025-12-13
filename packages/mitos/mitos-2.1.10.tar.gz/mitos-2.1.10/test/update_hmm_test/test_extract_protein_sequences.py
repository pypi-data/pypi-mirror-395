from pathlib import Path
from typing import Dict, List
from unittest.mock import MagicMock, patch

import pytest

from mitos.scripts.update_hmm import extract_protein_sequences


# Helper function to create fake GenBank files
def make_fake_gb_file(tmp_path: Path, name: str) -> Path:
    gb_file = tmp_path / name
    gb_file.write_text("FAKE_GENBANK_CONTENT")
    return gb_file


@pytest.fixture
def tmp_log_dir(tmp_path):
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    return log_dir


@pytest.fixture
def gb_files(tmp_path):
    # Create two fake GenBank files
    return [make_fake_gb_file(tmp_path, f"file{i}.gb") for i in range(2)]


# normal extraction from multiple files
@patch("mitos.scripts.update_hmm.getfeatures")
def test_extract_protein_sequences_basic(mock_getfeatures, gb_files, tmp_log_dir):
    # Setup mock
    mock_getfeatures.parse_args.return_value = (MagicMock(), ["input.gb"])
    # Each Feature -> header|gene|start|stop \n sequence
    mock_getfeatures.run.side_effect = [
        "NC_043772|cox1|0|1535\nMLRWFFSTNHKDIG\nNC_043773|cox2|0|1000\nMSEQTESTAAA\n",
        "NC_043774|cox1|1000|2000\nMLPQKWLFSTNH\nNC_043775|cox3|0|800\nTTTGGGAAA\n",
    ]

    result: Dict[str, List[str]] = extract_protein_sequences(gb_files, tmp_log_dir)

    # Check that all genes were extracted
    assert set(result.keys()) == {"cox1", "cox2", "cox3"}
    # Check entries for cox1 contain both sequences
    cox1_entries = result["cox1"]
    assert len(cox1_entries) == 2
    assert any("NC_043772|cox1" in e for e in cox1_entries)
    assert any("NC_043774|cox1" in e for e in cox1_entries)
    # Check cox2 and cox3
    assert result["cox2"][0].startswith(">NC_043773|cox2")
    assert result["cox3"][0].startswith(">NC_043775|cox3")


# entries with empty translation are skipped
@patch("mitos.scripts.update_hmm.getfeatures")
def test_extract_protein_sequences_skip_empty_sequence(
    mock_getfeatures, gb_files, tmp_log_dir
):
    mock_getfeatures.parse_args.return_value = (MagicMock(), ["input.gb"])
    mock_getfeatures.run.return_value = (
        "NC_043772|cox1|0|1535\n\n"  # empty sequence
        "NC_043773|cox2|0|1000\nMSEQTESTAAA\n"
    )

    result: Dict[str, List[str]] = extract_protein_sequences([gb_files[0]], tmp_log_dir)

    assert "cox1" not in result  # skipped
    assert "cox2" in result
    assert result["cox2"][0].startswith(">NC_043773|cox2")


# getfeatures.run raises exception
@patch("mitos.scripts.update_hmm.getfeatures")
def test_extract_protein_sequences_handle_exception(
    mock_getfeatures, gb_files, tmp_log_dir
):
    mock_getfeatures.parse_args.return_value = (MagicMock(), ["input.gb"])
    mock_getfeatures.run.side_effect = Exception("mock error")

    result: Dict[str, List[str]] = extract_protein_sequences([gb_files[0]], tmp_log_dir)

    # All files fail → result should be empty
    assert result == {}


# empty output from getfeatures
@patch("mitos.scripts.update_hmm.getfeatures")
def test_extract_protein_sequences_empty_output(
    mock_getfeatures, gb_files, tmp_log_dir
):
    mock_getfeatures.parse_args.return_value = (MagicMock(), ["input.gb"])
    mock_getfeatures.run.return_value = ""  # no features

    result: Dict[str, List[str]] = extract_protein_sequences([gb_files[0]], tmp_log_dir)
    assert result == {}


# multiple entries for the same gene
@patch("mitos.scripts.update_hmm.getfeatures")
def test_extract_protein_sequences_multiple_entries_same_gene(
    mock_getfeatures, gb_files, tmp_log_dir
):
    mock_getfeatures.parse_args.return_value = (MagicMock(), ["input.gb"])
    mock_getfeatures.run.return_value = (
        "NC_043772|cox1|0|1535\nSEQ1\nNC_043774|cox1|1000|2000\nSEQ2\n"
    )

    result: Dict[str, List[str]] = extract_protein_sequences([gb_files[0]], tmp_log_dir)

    # Both sequences should be collected under 'cox1'
    assert "cox1" in result
    assert len(result["cox1"]) == 2
    assert result["cox1"][0].startswith(">NC_043772|cox1")
    assert result["cox1"][1].startswith(">NC_043774|cox1")
