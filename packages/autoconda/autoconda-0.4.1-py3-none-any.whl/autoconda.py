#!/usr/bin/env python

import argparse
import os
import subprocess
import sys
from pathlib import Path

import yaml

__version__ = "0.4.1"

parser = argparse.ArgumentParser(prog="autoconda")
parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
parser.add_argument(
    "--path",
    "-p",
    help="path to start searching for environment.yml or environment.yaml (defaults to current directory)",
    default=os.getcwd(),
    type=Path,
)
parser.add_argument("command", nargs="+", help="Command and arguments to run")


def autoconda(path: Path, command: list[str]):
    env_name = _get_conda_environment_name(path)

    if env_name is None:
        print(
            "Error: No environment.yml or environment.yaml file found or no environment name specified in the file.",
            file=sys.stderr,
        )
        sys.exit(1)

    result = subprocess.run(["conda", "run", "-n", env_name, "--no-capture-output", *command])
    sys.exit(result.returncode)


def _get_conda_environment_name(start_path: Path) -> str | None:
    env_file = _find_environment_file(start_path)
    if env_file is None:
        return None

    try:
        with open(env_file) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError:
        return None

    return data.get("name")


def _find_environment_file(current_path: Path) -> Path | None:
    while True:
        for ext in ["yml", "yaml"]:
            env_file = current_path / f"environment.{ext}"
            if env_file.exists():
                return env_file
        if current_path == current_path.parent:
            return None
        current_path = current_path.parent


def main():
    args = parser.parse_args()
    autoconda(**vars(args))


if __name__ == "__main__":
    main()
