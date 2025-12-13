"""Core conversion functions between Polars schemas and Python data structures."""

from __future__ import annotations

import polars as pl
from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Dict, Type, Optional, Union, Tuple, get_type_hints, get_origin, get_args
from collections import namedtuple
from collections.abc import Iterable

try:
    from typing import TypedDict, NamedTuple  # noqa: F401
except ImportError:
    from typing_extensions import TypedDict  # noqa: F401
    from typing_extensions import NamedTuple  # type: ignore[assignment]  # noqa: F401

from .errors import SchemaError, ConversionError, UnsupportedTypeError
from .type_mappings import (
    get_python_type_from_polars,
    get_polars_type_from_python,
)

# get_type_hints is imported at top level, no need for conditional


def _normalize_polars_schema(
    schema: Union[pl.Schema, Dict[str, Any], Iterable[Tuple[str, Any]]],
) -> Dict[str, Any]:
    """
    Normalize a Polars schema from any supported format to a dict.

    Supports:
    - pl.Schema: Polars Schema object
    - dict[str, pl.DataType]: Dictionary mapping field names to types
    - Iterable[tuple[str, pl.DataType]]: Iterable of (field_name, type) tuples

    Args:
        schema: Polars schema in any supported format

    Returns:
        Normalized dictionary mapping field names to Polars types

    Raises:
        SchemaError: If the schema format is invalid
    """
    # Handle pl.Schema
    if isinstance(schema, pl.Schema):
        return dict(schema)

    # Handle dict
    if isinstance(schema, dict):
        return schema

    # Handle Iterable[tuple[str, Any]]
    # Note: Check for string explicitly since strings are iterable
    if isinstance(schema, str):
        raise SchemaError(
            f"Schema must be pl.Schema, dict, or iterable of tuples, got {type(schema)}"
        )

    if isinstance(schema, (list, tuple)) or hasattr(schema, "__iter__"):
        try:
            # Try to convert to dict from iterable of tuples
            result = {}
            for item in schema:
                if not isinstance(item, (tuple, list)) or len(item) != 2:
                    raise SchemaError(f"Schema items must be (field_name, type) tuples, got {item}")
                field_name, field_type = item
                if not isinstance(field_name, str):
                    raise SchemaError(f"Field name must be a string, got {type(field_name)}")
                if field_name in result:
                    raise SchemaError(f"Duplicate field name '{field_name}' in schema")
                result[field_name] = field_type
            if not result:
                raise SchemaError("Schema cannot be empty")
            return result
        except SchemaError:
            raise
        except (TypeError, ValueError) as e:
            raise SchemaError(f"Invalid schema format: {e}") from e

    raise SchemaError(f"Schema must be pl.Schema, dict, or iterable of tuples, got {type(schema)}")


def _validate_schema(schema: Dict[str, Any], schema_type: str = "Polars") -> None:
    """Validate schema structure."""
    if not isinstance(schema, dict):
        raise SchemaError(f"{schema_type} schema must be a dictionary")

    if not schema:
        raise SchemaError(f"{schema_type} schema cannot be empty")

    field_names = list(schema.keys())

    # Check for duplicate field names
    if len(field_names) != len(set(field_names)):
        raise SchemaError(f"{schema_type} schema contains duplicate field names")

    # Check for empty field names
    for name in field_names:
        if not isinstance(name, str):
            raise SchemaError(f"{schema_type} field names must be strings, got {type(name)}")
        if name == "":
            raise SchemaError(f"{schema_type} schema contains empty field name")
        if schema[name] is None:
            raise SchemaError(f"{schema_type} field '{name}' has None type")


def _validate_name(name: str, name_type: str = "name") -> None:
    """Validate that a name is a valid Python identifier."""
    if not isinstance(name, str):
        raise SchemaError(f"{name_type} must be a string, got {type(name)}")
    if not name:
        raise SchemaError(f"{name_type} cannot be empty")
    if not name.isidentifier():
        raise SchemaError(f"{name_type} '{name}' is not a valid Python identifier")
    # Check for Python keywords
    import keyword

    if keyword.iskeyword(name):
        raise SchemaError(f"{name_type} '{name}' is a Python keyword and cannot be used")


def to_dataclass(
    polars_schema: Union[pl.Schema, Dict[str, Any], Iterable[Tuple[str, Any]]],
    class_name: str = "DataClass",
) -> Type:
    """
    Convert a Polars schema to a dataclass.

    Args:
        polars_schema: Polars schema in any supported format:
            - pl.Schema: Polars Schema object
            - dict[str, pl.DataType]: Dictionary mapping field names to types
            - Iterable[tuple[str, pl.DataType]]: Iterable of (field_name, type) tuples
        class_name: Name for the generated dataclass

    Returns:
        A dataclass type

    Raises:
        SchemaError: If the schema structure is invalid or class_name is invalid
        UnsupportedTypeError: If a type cannot be converted
    """
    # Normalize schema to dict format
    polars_schema = _normalize_polars_schema(polars_schema)

    _validate_schema(polars_schema, "Polars")
    _validate_name(class_name, "class_name")

    # Build annotations dict for the dataclass
    annotations: Dict[str, Any] = {}
    namespace: Dict[str, Any] = {}

    struct_counter: Dict[str, int] = {}  # Track nested struct counts by level
    for field_name, polars_type in polars_schema.items():
        try:
            python_type = _convert_polars_type_to_python_annotation(
                polars_type, namespace, class_name, struct_counter, 0
            )
            annotations[field_name] = python_type
        except (UnsupportedTypeError, ConversionError) as e:
            raise ConversionError(
                f"Could not convert field '{field_name}' (Polars type: {polars_type}): {e}"
            ) from e

    # Create the dataclass using a proper approach
    # We need to create the class with annotations and then apply dataclass decorator
    namespace["__annotations__"] = annotations
    # Use a more appropriate module - try to get caller's module, fallback to __main__
    try:
        import inspect

        frame = inspect.currentframe()
        if frame and frame.f_back:
            caller_module = frame.f_back.f_globals.get("__name__", "__main__")
            namespace["__module__"] = caller_module
        else:
            namespace["__module__"] = "__main__"
    except Exception:
        namespace["__module__"] = "__main__"

    # Create a class with the annotations
    cls = type(class_name, (), namespace)

    # Apply dataclass decorator
    return dataclass(cls)


def _convert_polars_type_to_python_annotation(
    polars_type: Any,
    namespace: Dict[str, Any],
    parent_name: str,
    struct_counter: Dict[str, int],
    depth: int = 0,
) -> Any:
    """Convert a Polars type to a Python type annotation, handling nested structures."""
    # Handle List types
    if isinstance(polars_type, pl.List):
        inner_type = polars_type.inner
        inner_annotation: Any = _convert_polars_type_to_python_annotation(
            inner_type, namespace, parent_name, struct_counter, depth
        )
        from typing import List

        return List[inner_annotation]  # type: ignore[valid-type]

    # Handle Struct types - create nested dataclass/TypedDict
    if isinstance(polars_type, pl.Struct):
        # Track nested struct counts to avoid naming conflicts
        counter_key = f"{parent_name}_{depth}"
        struct_counter[counter_key] = struct_counter.get(counter_key, 0) + 1
        counter = struct_counter[counter_key]
        nested_name = f"{parent_name}Struct{counter}" if counter > 1 else f"{parent_name}Struct"

        # Convert struct fields to annotations
        struct_annotations = {}
        for field in polars_type.fields:
            field_name = field.name
            field_type = field.dtype
            struct_annotations[field_name] = _convert_polars_type_to_python_annotation(
                field_type, namespace, nested_name, struct_counter, depth + 1
            )

        # For dataclass conversion, we'll create a nested dataclass
        nested_namespace: Dict[str, Any] = {  # noqa: F823
            "__annotations__": struct_annotations,
            "__module__": namespace.get("__module__", "__main__"),
        }
        nested_class = type(nested_name, (), nested_namespace)
        nested_dataclass: Any = dataclass(nested_class)
        # Store in namespace so it's available when the parent class is created
        namespace[nested_name] = nested_dataclass
        return nested_dataclass

    # Handle primitive types
    try:
        python_type = get_python_type_from_polars(polars_type)
    except UnsupportedTypeError as e:
        raise ConversionError(f"Could not convert Polars type {polars_type}: {e}") from e

    # Make all fields Optional for nullability

    return Optional[python_type]


def to_typeddict(
    polars_schema: Union[pl.Schema, Dict[str, Any], Iterable[Tuple[str, Any]]],
    dict_name: str = "TypedDict",
) -> Type:
    """
    Convert a Polars schema to a TypedDict.

    Args:
        polars_schema: Polars schema in any supported format:
            - pl.Schema: Polars Schema object
            - dict[str, pl.DataType]: Dictionary mapping field names to types
            - Iterable[tuple[str, pl.DataType]]: Iterable of (field_name, type) tuples
        dict_name: Name for the generated TypedDict

    Returns:
        A TypedDict type

    Raises:
        SchemaError: If the schema structure is invalid or dict_name is invalid
        UnsupportedTypeError: If a type cannot be converted
    """
    # Normalize schema to dict format
    polars_schema = _normalize_polars_schema(polars_schema)

    _validate_schema(polars_schema, "Polars")
    _validate_name(dict_name, "dict_name")

    # Build annotations dict for the TypedDict
    annotations: Dict[str, Any] = {}
    namespace: Dict[str, Any] = {}

    struct_counter: Dict[str, int] = {}  # Track nested struct counts by level
    for field_name, polars_type in polars_schema.items():
        try:
            python_type = _convert_polars_type_to_typeddict_annotation(
                polars_type, namespace, dict_name, struct_counter, 0
            )
            annotations[field_name] = python_type
        except (UnsupportedTypeError, ConversionError) as e:
            raise ConversionError(
                f"Could not convert field '{field_name}' (Polars type: {polars_type}): {e}"
            ) from e

    # Create TypedDict using functional syntax
    try:
        # Try typing.TypedDict first (Python 3.8+)
        from typing import TypedDict as TypedDictClass

        return TypedDictClass(dict_name, annotations, total=True)  # type: ignore[operator, misc, no-any-return]
    except (ImportError, TypeError):
        # Fall back to typing_extensions
        from typing_extensions import TypedDict as TypedDictClass

        return TypedDictClass(dict_name, annotations, total=True)  # type: ignore[operator, misc, no-any-return]


def _convert_polars_type_to_typeddict_annotation(
    polars_type: Any,
    namespace: Dict[str, Any],
    parent_name: str,
    struct_counter: Dict[str, int],
    depth: int = 0,
) -> Any:
    """Convert a Polars type to a TypedDict annotation, handling nested structures."""
    # Handle List types
    if isinstance(polars_type, pl.List):
        inner_type = polars_type.inner
        inner_annotation: Any = _convert_polars_type_to_typeddict_annotation(
            inner_type, namespace, parent_name, struct_counter, depth
        )
        from typing import List

        return List[inner_annotation]  # type: ignore[valid-type]

    # Handle Struct types - create nested TypedDict
    if isinstance(polars_type, pl.Struct):
        counter_key = f"{parent_name}_{depth}"
        struct_counter[counter_key] = struct_counter.get(counter_key, 0) + 1
        counter = struct_counter[counter_key]
        nested_name = f"{parent_name}Dict{counter}" if counter > 1 else f"{parent_name}Dict"

        # Convert struct fields to annotations
        struct_annotations = {}
        for field in polars_type.fields:
            field_name = field.name
            field_type = field.dtype
            struct_annotations[field_name] = _convert_polars_type_to_typeddict_annotation(
                field_type, namespace, nested_name, struct_counter, depth + 1
            )

        # Create nested TypedDict
        try:
            from typing import TypedDict as TypedDictClass
        except ImportError:
            from typing_extensions import TypedDict as TypedDictClass

        nested_typeddict = TypedDictClass(nested_name, struct_annotations, total=True)  # type: ignore[operator, misc]
        namespace[nested_name] = nested_typeddict
        return nested_typeddict

    # Handle primitive types
    try:
        python_type = get_python_type_from_polars(polars_type)
    except UnsupportedTypeError as e:
        raise ConversionError(f"Could not convert Polars type {polars_type}: {e}") from e

    # Make all fields Optional for nullability

    return Optional[python_type]


def to_namedtuple(
    polars_schema: Union[pl.Schema, Dict[str, Any], Iterable[Tuple[str, Any]]],
    tuple_name: str = "NamedTuple",
) -> Type:
    """
    Convert a Polars schema to a NamedTuple.

    Args:
        polars_schema: Polars schema in any supported format:
            - pl.Schema: Polars Schema object
            - dict[str, pl.DataType]: Dictionary mapping field names to types
            - Iterable[tuple[str, pl.DataType]]: Iterable of (field_name, type) tuples
        tuple_name: Name for the generated NamedTuple

    Returns:
        A NamedTuple type (typing.NamedTuple preferred, collections.namedtuple as fallback)

    Raises:
        SchemaError: If the schema structure is invalid or tuple_name is invalid
        UnsupportedTypeError: If a type cannot be converted
    """
    # Normalize schema to dict format
    polars_schema = _normalize_polars_schema(polars_schema)

    _validate_schema(polars_schema, "Polars")
    _validate_name(tuple_name, "tuple_name")

    # Build annotations dict for the NamedTuple
    annotations: Dict[str, Any] = {}

    for field_name, polars_type in polars_schema.items():
        # NamedTuples don't support nested structures well, so we'll convert to basic types
        try:
            python_type = _convert_polars_type_to_namedtuple_annotation(polars_type)
            annotations[field_name] = python_type
        except (UnsupportedTypeError, ConversionError) as e:
            raise ConversionError(
                f"Could not convert field '{field_name}' (Polars type: {polars_type}): {e}"
            ) from e

    # Create NamedTuple using typing.NamedTuple
    try:
        from typing import NamedTuple as NamedTupleClass

        # NamedTuple expects a list of (name, type) tuples
        field_definitions = [(name, annotation) for name, annotation in annotations.items()]
        return NamedTupleClass(tuple_name, field_definitions)  # type: ignore[return-value]
    except (ImportError, TypeError):
        # Fall back to collections.namedtuple (loses type information)
        field_names = list(annotations.keys())
        return namedtuple(tuple_name, field_names)


def _convert_polars_type_to_namedtuple_annotation(polars_type: Any) -> Any:
    """Convert a Polars type to a NamedTuple annotation (simplified - no nested structures)."""
    # Handle List types
    if isinstance(polars_type, pl.List):
        from typing import List

        return List[Any]

    # Handle Struct types - convert to dict
    if isinstance(polars_type, pl.Struct):
        from typing import Dict

        return Dict[str, Any]

    # Handle primitive types
    try:
        return get_python_type_from_polars(polars_type)
    except UnsupportedTypeError as e:
        raise ConversionError(
            f"Could not convert Polars type {polars_type} for NamedTuple: {e}"
        ) from e


def from_dataclass(dataclass_cls: Type) -> pl.Schema:
    """
    Convert a dataclass to a Polars schema.

    Args:
        dataclass_cls: A dataclass type

    Returns:
        Polars Schema object mapping field names to Polars types
    """
    if not is_dataclass(dataclass_cls):
        raise SchemaError(f"{dataclass_cls} is not a dataclass")

    # Get type hints
    try:
        hints = get_type_hints(dataclass_cls)
    except Exception as e:
        raise ConversionError(f"Could not get type hints from dataclass: {e}")

    # Convert each field
    polars_schema = {}
    for field in fields(dataclass_cls):
        field_name = field.name
        field_type = hints.get(field_name, field.type if hasattr(field, "type") else Any)

        try:
            polars_type = _convert_python_type_to_polars(field_type, hints)
            polars_schema[field_name] = polars_type
        except (ConversionError, UnsupportedTypeError):
            raise
        except Exception as e:
            raise ConversionError(
                f"Could not convert field '{field_name}' (type: {field_type}): {e}"
            ) from e

    return pl.Schema(polars_schema)


def from_typeddict(typeddict_cls: Type) -> pl.Schema:
    """
    Convert a TypedDict to a Polars schema.

    Args:
        typeddict_cls: A TypedDict type

    Returns:
        Polars Schema object mapping field names to Polars types
    """
    # Check if it's a TypedDict
    if not (hasattr(typeddict_cls, "__annotations__") or hasattr(typeddict_cls, "__total__")):
        # Try to detect TypedDict by checking if it's a dict subclass with annotations
        if not (isinstance(typeddict_cls, type) and issubclass(typeddict_cls, dict)):
            raise SchemaError(f"{typeddict_cls} is not a TypedDict")

    # Get annotations
    annotations = getattr(typeddict_cls, "__annotations__", {})
    if not annotations:
        # Try to get from __dict__
        annotations = getattr(typeddict_cls, "__dict__", {}).get("__annotations__", {})

    if not annotations:
        raise SchemaError(f"Could not find annotations in TypedDict {typeddict_cls}")

    # Convert each field
    polars_schema = {}
    for field_name, field_type in annotations.items():
        try:
            polars_type = _convert_python_type_to_polars(field_type, annotations)
            polars_schema[field_name] = polars_type
        except (ConversionError, UnsupportedTypeError):
            raise
        except Exception as e:
            raise ConversionError(
                f"Could not convert field '{field_name}' (type: {field_type}): {e}"
            ) from e

    return pl.Schema(polars_schema)


def from_namedtuple(namedtuple_cls: Type) -> pl.Schema:
    """
    Convert a NamedTuple to a Polars schema.

    Args:
        namedtuple_cls: A NamedTuple type (typing.NamedTuple or collections.namedtuple)

    Returns:
        Polars Schema object mapping field names to Polars types
    """
    # Get annotations if available (typing.NamedTuple)
    # In Python 3.11+, collections.namedtuple also has __annotations__ but it's empty
    # so we need to check if it's actually populated
    if hasattr(namedtuple_cls, "__annotations__") and namedtuple_cls.__annotations__:
        annotations = namedtuple_cls.__annotations__
    elif hasattr(namedtuple_cls, "_fields"):
        # collections.namedtuple - no type information
        annotations = {field: Any for field in namedtuple_cls._fields}
    else:
        raise SchemaError(f"{namedtuple_cls} is not a NamedTuple")

    # Convert each field
    polars_schema = {}
    for field_name, field_type in annotations.items():
        try:
            polars_type = _convert_python_type_to_polars(field_type, annotations)
            polars_schema[field_name] = polars_type
        except (ConversionError, UnsupportedTypeError):
            raise
        except Exception as e:
            raise ConversionError(
                f"Could not convert field '{field_name}' (type: {field_type}): {e}"
            ) from e

    return pl.Schema(polars_schema)


def _convert_python_type_to_polars(
    python_type: Any, all_annotations: Optional[Dict[str, Any]] = None
) -> Any:
    """Convert a Python type annotation to a Polars type, handling nested structures."""
    if all_annotations is None:
        all_annotations = {}

    # Handle Optional/Union with None
    origin = get_origin(python_type)
    if origin is Union:
        args = get_args(python_type)
        non_none_args = [a for a in args if a is not type(None)]
        if non_none_args:
            # Use the first non-None type
            return _convert_python_type_to_polars(non_none_args[0], all_annotations)

    # Handle List types
    if origin is list:
        args = get_args(python_type)
        if args:
            inner_type = args[0]
            inner_polars = _convert_python_type_to_polars(inner_type, all_annotations)
            return pl.List(inner_polars)
        return pl.List(pl.String)

    # Handle Dict types - convert to Struct with key/value fields
    if origin is dict:
        args = get_args(python_type)
        if len(args) >= 2:
            value_type = args[1]
            value_polars = _convert_python_type_to_polars(value_type, all_annotations)
            return pl.Struct([pl.Field("key", pl.String), pl.Field("value", value_polars)])
        return pl.Struct([pl.Field("key", pl.String), pl.Field("value", pl.String)])

    # Handle nested dataclasses - convert to Struct
    if is_dataclass(python_type):
        nested_schema = from_dataclass(python_type)  # type: ignore[arg-type]
        # Convert to pl.Field list
        struct_fields = [pl.Field(name, dtype) for name, dtype in nested_schema.items()]
        return pl.Struct(struct_fields)

    # Handle nested TypedDict - convert to Struct
    if isinstance(python_type, type) and issubclass(python_type, dict):
        if hasattr(python_type, "__annotations__"):
            nested_schema = from_typeddict(python_type)
            struct_fields = [pl.Field(name, dtype) for name, dtype in nested_schema.items()]
            return pl.Struct(struct_fields)

    # Handle primitive types
    try:
        return get_polars_type_from_python(python_type, all_annotations)
    except (ValueError, UnsupportedTypeError) as e:
        # Raise UnsupportedTypeError with context instead of silent fallback
        raise UnsupportedTypeError(
            f"Unsupported Python type: {python_type}. Original error: {e}"
        ) from e
