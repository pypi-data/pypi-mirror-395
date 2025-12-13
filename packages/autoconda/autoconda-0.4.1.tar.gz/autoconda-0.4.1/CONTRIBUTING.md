## Development

```
conda env create
conda activate autoconda-dev
pip install --group dev --editable .
```

## Publishing

```
export UV_PUBLISH_TOKEN=XXXXXXXX
uv build
uv publish
```
