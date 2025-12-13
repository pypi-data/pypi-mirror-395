"""Type mappings between Polars and Python types."""

import polars as pl
from typing import Any, Dict, Type, Union, get_origin, get_args, Optional, TYPE_CHECKING
from datetime import date, datetime
from decimal import Decimal
from dataclasses import is_dataclass as _is_dataclass

from .errors import UnsupportedTypeError


def is_dataclass_type(obj: Any) -> bool:
    """Check if an object is a dataclass type (not instance)."""
    try:
        return _is_dataclass(obj) and isinstance(obj, type)
    except Exception:
        return False


if TYPE_CHECKING:
    from typing import List as TypingList, Dict as TypingDict, Tuple as TypingTuple
else:
    try:
        from typing import List as TypingList, Dict as TypingDict, Tuple as TypingTuple
    except ImportError:
        from typing_extensions import List as TypingList, Dict as TypingDict, Tuple as TypingTuple

# Polars to Python type mappings
POLARS_TO_PYTHON: Dict[Type, Type] = {
    pl.Int8: int,
    pl.Int16: int,
    pl.Int32: int,
    pl.Int64: int,
    pl.UInt8: int,
    pl.UInt16: int,
    pl.UInt32: int,
    pl.UInt64: int,
    pl.Float32: float,
    pl.Float64: float,
    pl.Boolean: bool,
    pl.String: str,
    pl.Utf8: str,
    pl.Date: date,
    # Note: pl.Datetime and pl.Decimal require parameters (time unit, precision/scale)
    # These are handled specially in conversion functions
    pl.Decimal: Decimal,
    pl.Binary: bytes,
    pl.Null: type(None),
    pl.Categorical: str,
    pl.Enum: str,
}

# Python to Polars type mappings (for primitive types)
PYTHON_TO_POLARS: Dict[Type, Type] = {
    int: pl.Int64,
    float: pl.Float64,
    bool: pl.Boolean,
    str: pl.String,
    date: pl.Date,
    datetime: pl.Datetime,
    Decimal: pl.Decimal,
    bytes: pl.Binary,
    type(None): pl.Null,
}


def get_python_type_from_polars(polars_type: Any) -> Any:
    """Convert a Polars type to a Python type."""
    # Handle List types - check if it's an instance of List
    if isinstance(polars_type, pl.List):
        inner_type = polars_type.inner
        python_inner: Any = get_python_type_from_polars(inner_type)
        return TypingList[python_inner]  # type: ignore[valid-type]

    # Handle Struct types - check if it's an instance of Struct
    if isinstance(polars_type, pl.Struct):
        # Structs will be converted to nested dataclasses/TypedDicts
        return dict  # Temporary, will be handled specially in converters

    # Check direct mapping first (for type classes)
    if polars_type in POLARS_TO_PYTHON:
        return POLARS_TO_PYTHON[polars_type]

    # Handle Datetime instances (pl.Datetime("us"), etc.) - must be after direct mapping check
    if isinstance(polars_type, pl.Datetime):
        return datetime

    # Handle Decimal instances (pl.Decimal(38, 10), etc.)
    if isinstance(polars_type, pl.Decimal):
        return Decimal

    # Handle Categorical instances
    if isinstance(polars_type, pl.Categorical):
        return str

    # Handle Enum instances
    if isinstance(polars_type, pl.Enum):
        return str

    # Check by name for compatibility (for type classes like pl.Categorical, pl.Enum)
    type_name = getattr(polars_type, "__name__", "")
    for pl_type, py_type in POLARS_TO_PYTHON.items():
        if getattr(pl_type, "__name__", "") == type_name:
            return py_type

    raise UnsupportedTypeError(f"Unsupported Polars type: {polars_type}")


def get_polars_type_from_python(
    python_type: Type, annotations: Optional[Dict[str, Any]] = None
) -> Any:
    """Convert a Python type annotation to a Polars type."""
    # Handle Optional/Union types
    origin = get_origin(python_type)
    if origin is Union:
        args = get_args(python_type)
        # If Union with None, get the non-None type
        non_none_args = [a for a in args if a is not type(None)]
        if len(non_none_args) == 1:
            return get_polars_type_from_python(non_none_args[0], annotations)
        elif len(non_none_args) > 1:
            # Multiple types in Union - default to String
            return pl.String

    # Handle List types
    if origin is list or origin is TypingList:
        args = get_args(python_type)
        if args:
            inner_type = args[0]
            inner_polars = get_polars_type_from_python(inner_type, annotations)
            return pl.List(inner_polars)
        return pl.List(pl.String)  # Default to List[String]

    # Handle Dict types - convert to Struct with key/value fields
    if origin is dict or origin is TypingDict:
        args = get_args(python_type)
        if len(args) >= 2:
            value_type = args[1]
            value_polars = get_polars_type_from_python(value_type, annotations)
            return pl.Struct([pl.Field("key", pl.String), pl.Field("value", value_polars)])
        return pl.Struct([pl.Field("key", pl.String), pl.Field("value", pl.String)])

    # Handle Tuple types (convert to List)
    if origin is tuple or origin is TypingTuple:
        args = get_args(python_type)
        if args:
            # Use the first type for simplicity
            inner_type = args[0]
            inner_polars = get_polars_type_from_python(inner_type, annotations)
            return pl.List(inner_polars)
        return pl.List(pl.String)

    # Handle datetime specially - Polars requires time unit
    if python_type is datetime:
        # Default to microseconds for datetime
        return pl.Datetime("us")

    # Handle Decimal specially - Polars requires precision and scale
    if python_type is Decimal:
        # Default to reasonable precision/scale (38, 10)
        return pl.Decimal(38, 10)

    # Check direct mapping
    if python_type in PYTHON_TO_POLARS:
        return PYTHON_TO_POLARS[python_type]

    # Check for special types
    if python_type is Any:
        return pl.String  # Default for Any

    # For dataclasses and TypedDicts, return Struct (handled specially in converters)
    # In Python 3.11+, all classes have __annotations__ (empty by default)
    # so we need to check if it's actually populated or if it's a dataclass
    if is_dataclass_type(python_type):
        return pl.Struct  # Will be converted properly in converters

    # Check if it's a TypedDict (has __annotations__ and is a dict subclass)
    if (
        hasattr(python_type, "__annotations__")
        and getattr(python_type, "__annotations__", None)
        and isinstance(python_type, type)
        and issubclass(python_type, dict)
    ):
        return pl.Struct  # Will be converted properly in converters

    raise UnsupportedTypeError(f"Unsupported Python type: {python_type}")
