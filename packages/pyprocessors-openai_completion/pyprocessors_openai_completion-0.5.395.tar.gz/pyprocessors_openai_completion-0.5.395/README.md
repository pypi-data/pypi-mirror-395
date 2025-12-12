## Requirements

- Python 3.8+
- Flit to put Python packages and modules on PyPI
- Pydantic for the data parts.

## Installation
```
pip install flit
pip install pymultirole-plugins
```

## Publish the Python Package to PyPI
- Increment the version of your package in the `__init__.py` file:
```
"""An amazing package!"""

__version__ = 'x.y.z'
```
- Publish
```
flit publish
```
