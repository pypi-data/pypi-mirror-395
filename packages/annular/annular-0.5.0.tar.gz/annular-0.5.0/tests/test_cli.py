import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

import annular.cli


@pytest.mark.integration
def test_cli_can_be_called():
    """Test that '--help' can be successfully called for annular and annular run."""
    result = subprocess.run(["annular", "--help"])
    assert result.returncode == 0

    result = subprocess.run(["annular", "run", "--help"])
    assert result.returncode == 0


@pytest.mark.integration
def test_cli_missing_file():
    """Test that calling 'annular run' fails if not given any (valid) file."""
    result = subprocess.run(["annular", "run", "/does/not/exist"])
    assert result.returncode != 0

    result = subprocess.run(["annular", "run"])
    assert result.returncode != 0


@pytest.mark.parametrize(
    "config_files",
    [["/path/to/A"], ["/path/to/A", "/path/to/B"], ["/path/to/A", "/path/to/B", "/path/to/C", "/path/to/D"]],
)
def test_cli_main_called_per_config_file(monkeypatch, config_files):
    """Test that `main` is called once for each given config file."""
    monkeypatch.setattr(sys, "argv", ["annular", "run", *config_files])
    with patch("annular.cli.run") as main_func:  # patch `main` as imported by `cli`
        annular.cli.cli_main()
        assert len(main_func.mock_calls) == len(config_files)


def test_cli_results_paths(monkeypatch):
    """Test that a result path can be given and is correctly passed in."""
    monkeypatch.setattr(sys, "argv", ["annular", "run", "/config/path", "-o", "/my/results/"])
    with patch("annular.cli.run") as main_func:  # patch `main` as imported by `cli`
        annular.cli.cli_main()
        main_func.assert_called_with(Path("/config/path"), Path("/my/results/"))


def test_cli_default_results_path(monkeypatch):
    """Test that the default results path is used when not specified."""
    monkeypatch.setattr(sys, "argv", ["annular", "run", "/config/path"])
    with patch("annular.cli.run") as main_func:  # patch `main` as imported by `cli`
        annular.cli.cli_main()
        main_func.assert_called_with(Path("/config/path"), Path("results/"))
