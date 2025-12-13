# Autoconda

```
usage: autoconda [-h] [--version] [--path PATH] command [command ...]

positional arguments:
  command               Command and arguments to run

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --path PATH, -p PATH  path to start searching for environment.yml or environment.yaml (defaults to current directory)
```

Installation (for now):

```
uv tool install .
```

Usage:

```
autoconda python script.py
autoconda jupyter notebook
autoconda -- python --version
```
