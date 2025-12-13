"""Comprehensive edge case tests."""

import pytest
import polars as pl
from dataclasses import dataclass
from typing import List, Optional, Union
from rattata import (
    to_dataclass,
    from_dataclass,
    from_typeddict,
    SchemaError,
    ConversionError,
    UnsupportedTypeError,
)


class TestFieldNameEdgeCases:
    """Tests for edge cases with field names."""

    def test_unicode_field_names(self):
        """Test field names with Unicode characters."""
        schema = {
            "name_ñ": pl.String,
            "âge": pl.Int32,
            "café": pl.String,
        }
        Person = to_dataclass(schema, class_name="Person")
        person = Person(name_ñ="Test", âge=30, café="coffee")
        assert person.name_ñ == "Test"

    def test_very_long_field_name(self):
        """Test with very long field names."""
        long_name = "a" * 1000
        schema = {long_name: pl.String}
        Person = to_dataclass(schema, class_name="Person")
        person = Person(**{long_name: "test"})
        assert getattr(person, long_name) == "test"

    def test_field_name_with_underscores(self):
        """Test field names with multiple underscores."""
        schema = {
            "field__name": pl.String,
            "_private": pl.Int32,
            "normal_field": pl.String,
        }
        Person = to_dataclass(schema, class_name="Person")
        person = Person(field__name="test", _private=1, normal_field="normal")
        assert person.field__name == "test"

    def test_empty_field_name_raises_error(self):
        """Test that empty field names raise error."""
        # This should be caught by validation
        with pytest.raises(SchemaError, match="empty field name"):
            to_dataclass({"": pl.String}, class_name="Invalid")


class TestTypeEdgeCases:
    """Tests for edge cases with types."""

    def test_optional_nested_structures(self):
        """Test Optional nested structures."""
        from typing import Optional

        @dataclass
        class Address:
            street: str

        @dataclass
        class Person:
            name: str
            address: Optional[Address] = None

        schema = from_dataclass(Person)
        assert isinstance(schema["address"], pl.Struct)

    def test_union_with_multiple_types(self):
        """Test Union types with multiple non-None types."""

        @dataclass
        class Value:
            data: Union[str, int, float]

        schema = from_dataclass(Value)
        # Union with multiple types defaults to String
        assert schema["data"] == pl.String

    def test_list_of_optional(self):
        """Test List[Optional[T]]."""
        from typing import Optional

        @dataclass
        class Items:
            values: List[Optional[str]]

        schema = from_dataclass(Items)
        assert isinstance(schema["values"], pl.List)
        assert schema["values"].inner == pl.String

    def test_nested_lists(self):
        """Test deeply nested lists."""
        schema = {
            "matrix": pl.List(pl.List(pl.List(pl.Float64))),
        }
        Matrix = to_dataclass(schema, class_name="Matrix")
        matrix = Matrix(matrix=[[[1.0, 2.0]]])
        assert matrix.matrix == [[[1.0, 2.0]]]

    def test_list_containing_struct(self):
        """Test List containing Struct."""
        schema = {
            "users": pl.List(
                pl.Struct(
                    [
                        pl.Field("name", pl.String),
                        pl.Field("age", pl.Int32),
                    ]
                )
            ),
        }
        Users = to_dataclass(schema, class_name="Users")
        # This is complex, so just verify it can be created
        assert Users is not None

    def test_struct_containing_list(self):
        """Test Struct containing List."""
        schema = {
            "user": pl.Struct(
                [
                    pl.Field("name", pl.String),
                    pl.Field("tags", pl.List(pl.String)),
                ]
            ),
        }
        User = to_dataclass(schema, class_name="User")
        user = User(user=User.UserStruct(name="Alice", tags=["tag1", "tag2"]))
        assert user.user.name == "Alice"
        assert user.user.tags == ["tag1", "tag2"]


class TestComplexNestedScenarios:
    """Tests for complex nested scenarios."""

    def test_very_wide_schema(self):
        """Test schema with many fields."""
        schema = {f"field_{i}": pl.String for i in range(50)}
        Wide = to_dataclass(schema, class_name="Wide")
        assert Wide is not None

    def test_mixed_nesting_patterns(self):
        """Test mixed nesting patterns."""
        schema = {
            "users": pl.List(
                pl.Struct(
                    [
                        pl.Field("name", pl.String),
                        pl.Field("scores", pl.List(pl.Float64)),
                        pl.Field(
                            "address",
                            pl.Struct(
                                [
                                    pl.Field("street", pl.String),
                                    pl.Field("tags", pl.List(pl.String)),
                                ]
                            ),
                        ),
                    ]
                )
            ),
        }
        Complex = to_dataclass(schema, class_name="Complex")
        assert Complex is not None


class TestErrorHandlingEdgeCases:
    """Tests for error handling in edge cases."""

    def test_any_type_handling(self):
        """Test dataclass with Any type (proxy for missing type hints)."""
        from typing import Any

        @dataclass
        class Person:
            name: str
            age: Any  # Any type should default to String

        # Any converts to String (default)
        schema = from_dataclass(Person)
        assert schema["name"] == pl.String
        assert schema["age"] == pl.String  # Any defaults to String

    def test_invalid_nested_type(self):
        """Test invalid nested type."""
        schema = {
            "field": "not a valid type",
        }
        with pytest.raises((ConversionError, UnsupportedTypeError)):
            to_dataclass(schema, class_name="Invalid")

    def test_none_in_schema_raises_error(self):
        """Test that None values in schema raise error."""
        schema = {
            "name": pl.String,
            "age": None,  # Invalid
        }
        with pytest.raises(SchemaError):
            to_dataclass(schema, class_name="Invalid")


class TestDefaultValues:
    """Tests for default values in dataclasses."""

    def test_dataclass_with_defaults(self):
        """Test dataclass with default values."""

        @dataclass
        class Product:
            name: str
            price: float = 0.0
            in_stock: bool = True

        schema = from_dataclass(Product)
        assert schema["name"] == pl.String
        assert schema["price"] == pl.Float64
        assert schema["in_stock"] == pl.Boolean

    def test_optional_with_default_none(self):
        """Test Optional field with default None."""

        @dataclass
        class Item:
            name: str
            description: Optional[str] = None

        schema = from_dataclass(Item)
        assert schema["name"] == pl.String
        assert schema["description"] == pl.String


class TestTypedDictEdgeCases:
    """Tests for TypedDict edge cases."""

    def test_total_false_typeddict(self):
        """Test TypedDict with total=False."""
        from typing import TypedDict

        class PartialDict(TypedDict, total=False):
            name: str
            age: int

        schema = from_typeddict(PartialDict)
        assert schema["name"] == pl.String
        assert schema["age"] == pl.Int64

    def test_inherited_typeddict(self):
        """Test TypedDict inheritance."""
        from typing import TypedDict

        class BaseDict(TypedDict):
            name: str

        class ExtendedDict(BaseDict):
            age: int

        schema = from_typeddict(ExtendedDict)
        assert "name" in schema
        assert "age" in schema


class TestDateAndTimeTypes:
    """Tests for date and time types."""

    def test_date_type(self):
        """Test Date type conversion."""
        from datetime import date

        @dataclass
        class Event:
            event_date: date

        schema = from_dataclass(Event)
        assert schema["event_date"] == pl.Date

    def test_datetime_type(self):
        """Test Datetime type conversion."""
        from datetime import datetime

        @dataclass
        class Event:
            timestamp: datetime

        schema = from_dataclass(Event)
        assert schema["timestamp"] == pl.Datetime

    def test_polars_date_to_python(self):
        """Test Polars Date to Python."""
        schema = {"date": pl.Date}
        Event = to_dataclass(schema, class_name="Event")
        # Verify it can be instantiated
        assert Event is not None

    def test_polars_datetime_to_python(self):
        """Test Polars Datetime to Python."""
        # Datetime requires time unit parameter
        schema = {"timestamp": pl.Datetime("us")}
        Event = to_dataclass(schema, class_name="Event")
        # Verify it can be instantiated
        assert Event is not None


class TestDecimalType:
    """Tests for Decimal type."""

    def test_decimal_type(self):
        """Test Decimal type conversion."""
        from decimal import Decimal

        @dataclass
        class Money:
            amount: Decimal

        schema = from_dataclass(Money)
        # Decimal is converted to pl.Decimal with default precision/scale
        assert isinstance(schema["amount"], pl.Decimal)

    def test_polars_decimal_to_python(self):
        """Test Polars Decimal to Python."""
        schema = {"amount": pl.Decimal}
        Money = to_dataclass(schema, class_name="Money")
        assert Money is not None


class TestBinaryType:
    """Tests for Binary type."""

    def test_binary_type(self):
        """Test Binary type conversion."""

        @dataclass
        class Data:
            content: bytes

        schema = from_dataclass(Data)
        assert schema["content"] == pl.Binary

    def test_polars_binary_to_python(self):
        """Test Polars Binary to Python."""
        schema = {"data": pl.Binary}
        Data = to_dataclass(schema, class_name="Data")
        assert Data is not None
