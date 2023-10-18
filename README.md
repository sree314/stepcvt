# STEP Converter

Tools to generate STL files for 3D printing from STEP files.

Built as a project in CSC293/Fall 2023 at the University of Rochester.

## Installation

For now, install in to the same environment that `cadquery` is installed in.

```
python3 -m pip install -r requirements-dev.txt
python3 setup.py develop
```

## Testing

This package uses `pytest` for testing. Please install pytest:

```
python3 -m pip install pytest
```

And run `pytest` as follows:

```
python3 -m pytest
```
