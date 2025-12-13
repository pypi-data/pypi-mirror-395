from pathlib import Path

import pytest

from autoconda import _get_conda_environment_name


@pytest.mark.parametrize("suffix", (".yml", ".yaml"))
def test_get_conda_environment_name_in_current_dir(suffix: str, tmp_path: Path):
    env_file = (tmp_path / "environment").with_suffix(suffix)
    env_file.write_text("name: test-env\n")

    assert _get_conda_environment_name(tmp_path) == "test-env"


def test_get_conda_environment_name_in_parent_dir(tmp_path: Path):
    env_file = tmp_path / "environment.yml"
    env_file.write_text("name: test-env\n")

    subdir = tmp_path / "subdir"
    subdir.mkdir()

    assert _get_conda_environment_name(tmp_path) == "test-env"


def test_get_conda_environment_name_not_found(tmp_path: Path):
    assert _get_conda_environment_name(tmp_path) is None


def test_get_conda_environment_name_success(tmp_path: Path):
    env_file = tmp_path / "environment.yml"
    env_file.write_text("name: integration-test-env\n")

    assert _get_conda_environment_name(tmp_path) == "integration-test-env"


def test_get_conda_environment_name_invalid_yaml(tmp_path: Path):
    env_file = tmp_path / "environment.yml"
    env_file.write_text("invalid: yaml: content: [[[")

    assert _get_conda_environment_name(tmp_path) is None
