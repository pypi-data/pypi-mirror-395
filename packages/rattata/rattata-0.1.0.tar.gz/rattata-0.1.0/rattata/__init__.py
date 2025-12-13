"""
Rattata: Convert between Polars schemas and Python data structures.

Provides bidirectional conversion between Polars schemas and:
- dataclasses
- TypedDicts
- NamedTuples
"""

from .converters import (
    to_dataclass,
    to_typeddict,
    to_namedtuple,
    from_dataclass,
    from_typeddict,
    from_namedtuple,
)

from .errors import (
    RattataError,
    SchemaError,
    ConversionError,
    UnsupportedTypeError,
)

__version__ = "0.1.0"
__author__ = "Odos Matthews"
__email__ = "odosmatthews@gmail.com"

__all__ = [
    "to_dataclass",
    "to_typeddict",
    "to_namedtuple",
    "from_dataclass",
    "from_typeddict",
    "from_namedtuple",
    "RattataError",
    "SchemaError",
    "ConversionError",
    "UnsupportedTypeError",
]
