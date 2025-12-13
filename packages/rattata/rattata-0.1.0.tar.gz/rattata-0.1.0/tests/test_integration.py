"""Integration tests with actual Polars DataFrames."""

import polars as pl
from dataclasses import dataclass
from typing import List
from rattata import to_dataclass, from_dataclass, from_typeddict


class TestDataFrameIntegration:
    """Integration tests with Polars DataFrames."""

    def test_dataclass_to_dataframe(self):
        """Test converting dataclass to schema and using with DataFrame."""

        @dataclass
        class Person:
            name: str
            age: int
            score: float

        schema = from_dataclass(Person)
        assert isinstance(schema, pl.Schema)

        # Create DataFrame with the schema
        df = pl.DataFrame(
            {"name": ["Alice", "Bob"], "age": [30, 25], "score": [95.5, 87.0]},
            schema=schema,
        )

        assert df.schema == schema
        assert df["name"].dtype == pl.String
        assert df["age"].dtype == pl.Int64
        assert df["score"].dtype == pl.Float64

    def test_dataframe_schema_to_dataclass(self):
        """Test converting DataFrame schema to dataclass."""
        df = pl.DataFrame(
            {
                "name": ["Alice", "Bob"],
                "age": [30, 25],
                "score": [95.5, 87.0],
            }
        )

        Person = to_dataclass(dict(df.schema), class_name="Person")
        person = Person(name="Charlie", age=28, score=92.0)
        assert person.name == "Charlie"

    def test_round_trip_with_dataframe(self):
        """Test round-trip conversion through DataFrame."""

        @dataclass
        class Product:
            name: str
            price: float
            in_stock: bool

        # Convert to schema
        schema = from_dataclass(Product)

        # Create DataFrame
        df = pl.DataFrame(
            {
                "name": ["Widget", "Gadget"],
                "price": [10.99, 25.50],
                "in_stock": [True, False],
            },
            schema=schema,
        )

        # Convert schema back to dataclass
        Product2 = to_dataclass(dict(df.schema), class_name="Product2")
        product = Product2(name="Test", price=15.0, in_stock=True)
        assert product.name == "Test"

    def test_dataframe_with_list_column(self):
        """Test DataFrame with list column."""

        @dataclass
        class Item:
            name: str
            tags: List[str]

        schema = from_dataclass(Item)

        df = pl.DataFrame(
            {
                "name": ["Item1", "Item2"],
                "tags": [["tag1", "tag2"], ["tag3"]],
            },
            schema=schema,
        )

        assert df.schema["tags"] == pl.List(pl.String)
        assert df["tags"].dtype == pl.List(pl.String)

    def test_dataframe_with_nested_struct(self):
        """Test DataFrame with nested struct column."""

        @dataclass
        class Address:
            street: str
            city: str

        @dataclass
        class Person:
            name: str
            address: Address

        schema = from_dataclass(Person)

        # Create DataFrame with struct data
        df = pl.DataFrame(
            {
                "name": ["Alice"],
                "address": [{"street": "123 Main", "city": "Springfield"}],
            },
            schema=schema,
        )

        assert isinstance(df.schema["address"], pl.Struct)
        assert df["address"].dtype == pl.Struct

    def test_typeddict_to_dataframe(self):
        """Test converting TypedDict to schema and using with DataFrame."""
        from typing import TypedDict

        class BookDict(TypedDict):
            title: str
            author: str
            pages: int

        schema = from_typeddict(BookDict)

        df = pl.DataFrame(
            {
                "title": ["Book1", "Book2"],
                "author": ["Author1", "Author2"],
                "pages": [100, 200],
            },
            schema=schema,
        )

        assert df.schema == schema
        assert df["title"].dtype == pl.String
