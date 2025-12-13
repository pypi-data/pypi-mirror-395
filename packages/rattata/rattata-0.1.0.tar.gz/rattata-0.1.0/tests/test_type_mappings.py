"""Tests for type mapping functions."""

import pytest
import polars as pl
from typing import List, Dict, Optional, Union
from datetime import date, datetime
from decimal import Decimal

from rattata.type_mappings import (
    get_python_type_from_polars,
    get_polars_type_from_python,
    POLARS_TO_PYTHON,
    PYTHON_TO_POLARS,
)
from rattata import UnsupportedTypeError


class TestGetPythonTypeFromPolars:
    """Tests for get_python_type_from_polars function."""

    @pytest.mark.parametrize(
        "polars_type,python_type",
        [
            (pl.Int8, int),
            (pl.Int16, int),
            (pl.Int32, int),
            (pl.Int64, int),
            (pl.UInt8, int),
            (pl.UInt16, int),
            (pl.UInt32, int),
            (pl.UInt64, int),
            (pl.Float32, float),
            (pl.Float64, float),
            (pl.Boolean, bool),
            (pl.String, str),
            (pl.Utf8, str),
            (pl.Date, date),
            (pl.Datetime("us"), datetime),  # Datetime requires time unit
            (pl.Decimal(38, 10), Decimal),  # Decimal requires precision/scale
            (pl.Binary, bytes),
            (pl.Null, type(None)),
            (pl.Categorical, str),
        ],
    )
    def test_primitive_types(self, polars_type, python_type):
        """Test conversion of primitive Polars types."""
        result = get_python_type_from_polars(polars_type)
        assert result == python_type  # noqa: E721

    def test_list_type(self):
        """Test conversion of List type."""
        list_type = pl.List(pl.String)
        result = get_python_type_from_polars(list_type)
        assert hasattr(result, "__origin__")
        origin = getattr(result, "__origin__", None)
        # Check it's a List type (might be typing.List or list)
        assert origin in (list, List)

    def test_unsupported_type_raises_error(self):
        """Test that unsupported types raise UnsupportedTypeError."""

        # Create a mock unsupported type
        class UnsupportedType:
            pass

        with pytest.raises(UnsupportedTypeError):
            get_python_type_from_polars(UnsupportedType)


class TestGetPolarsTypeFromPython:
    """Tests for get_polars_type_from_python function."""

    @pytest.mark.parametrize(
        "python_type,polars_type",
        [
            (int, pl.Int64),
            (float, pl.Float64),
            (bool, pl.Boolean),
            (str, pl.String),
            (date, pl.Date),
            (datetime, pl.Datetime),
            (Decimal, pl.Decimal),
            (bytes, pl.Binary),
            (type(None), pl.Null),
        ],
    )
    def test_primitive_types(self, python_type, polars_type):
        """Test conversion of primitive Python types."""
        result = get_polars_type_from_python(python_type)
        assert result == polars_type

    def test_optional_type(self):
        """Test conversion of Optional type."""
        optional_str = Optional[str]
        result = get_polars_type_from_python(optional_str)
        assert result == pl.String

    def test_list_type(self):
        """Test conversion of List type."""
        list_type = List[str]
        result = get_polars_type_from_python(list_type)
        assert isinstance(result, pl.List)
        assert result.inner == pl.String

    def test_dict_type(self):
        """Test conversion of Dict type."""
        dict_type = Dict[str, int]
        result = get_polars_type_from_python(dict_type)
        # Dict converts to Struct
        assert isinstance(result, pl.Struct)

    def test_union_type(self):
        """Test conversion of Union type."""
        union_type = Union[str, int]
        result = get_polars_type_from_python(union_type)
        # Union with multiple non-None types defaults to String
        assert result == pl.String

    def test_unsupported_type_raises_error(self):
        """Test that unsupported types raise UnsupportedTypeError."""

        class UnsupportedType:
            pass

        with pytest.raises(UnsupportedTypeError):
            get_polars_type_from_python(UnsupportedType)


class TestTypeMappings:
    """Tests for type mapping dictionaries."""

    def test_polars_to_python_mappings(self):
        """Test POLARS_TO_PYTHON mappings."""
        assert POLARS_TO_PYTHON[pl.Int8] == int  # noqa: E721
        assert POLARS_TO_PYTHON[pl.String] == str  # noqa: E721
        assert POLARS_TO_PYTHON[pl.Boolean] == bool  # noqa: E721

    def test_python_to_polars_mappings(self):
        """Test PYTHON_TO_POLARS mappings."""
        assert PYTHON_TO_POLARS[int] == pl.Int64
        assert PYTHON_TO_POLARS[str] == pl.String
        assert PYTHON_TO_POLARS[bool] == pl.Boolean
