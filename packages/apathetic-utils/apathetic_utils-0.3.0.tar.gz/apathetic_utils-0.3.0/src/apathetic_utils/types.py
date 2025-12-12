# src/apathetic_utils/types.py
"""Type utilities."""

from __future__ import annotations

from types import UnionType
from typing import (
    Any,
    Literal,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

from typing_extensions import NotRequired


ApatheticUtils_T = TypeVar("ApatheticUtils_T")


class ApatheticUtils_Internal_Types:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides type utility functionality.

    This class contains utilities for type checking and manipulation.
    When mixed into apathetic_utils, it provides type utility methods.
    """

    @staticmethod
    def cast_hint(
        typ: type[ApatheticUtils_T],  # noqa: ARG004
        value: Any,
    ) -> ApatheticUtils_T:
        """Explicit cast that documents intent but is purely for type hinting.

        A drop-in replacement for `typing.cast`, meant for places where:
          - You want to silence mypy's redundant-cast warnings.
          - You want to signal "this narrowing is intentional."
          - You need IDEs (like Pylance) to retain strong inference on a value.

        Does not handle Union, Optional, or nested generics: stick to cast(),
          because unions almost always represent a meaningful type narrowing.

        This function performs *no runtime checks*.
        """
        return cast("ApatheticUtils_T", value)

    @staticmethod
    def schema_from_typeddict(td: type[Any]) -> dict[str, Any]:
        """Extract field names and their annotated types from a TypedDict."""
        return get_type_hints(td, include_extras=True)

    @staticmethod
    def literal_to_set(literal_type: Any) -> set[Any]:
        """Extract values from a Literal type as a set.

        Example:
            StitchMode = Literal["raw", "package"]
            valid_modes = literal_to_set(StitchMode)  # Returns set with literal values

        Args:
            literal_type: A Literal type (e.g., Literal["a", "b"])

        Returns:
            A set containing all values from the Literal type.
            Returns set[Any] to allow flexible operations without requiring
            casts. The actual values are constrained by the Literal type at
            runtime validation.

        Type Safety Tradeoffs:
            This function returns set[Any] after considering three approaches:

            1. set[Any] (current): Allows flexible operations (e.g., sorted(),
               membership checks) without requiring casts. Less type-safe but
               more ergonomic for common use cases.

            2. set[str | int | float | bool | None]: More type-safe, but requires
               casts for operations like sorted() that expect specific types,
               creating noise and potential for errors.

            3. TypeVar (like cast_hint): Would provide perfect type inference,
               but Python's type system cannot extract the union of literal
               values from a Literal type at the type level.

            The current approach prioritizes ergonomics while still providing
            runtime validation that the input is a Literal type.

        Raises:
            TypeError: If the input is not a Literal type
        """
        origin = get_origin(literal_type)
        if origin is not Literal:
            msg = f"Expected Literal type, got {literal_type}"
            raise TypeError(msg)
        return set(get_args(literal_type))

    @staticmethod
    def _isinstance_generics(  # noqa: PLR0911
        value: Any,
        origin: Any,
        args: tuple[Any, ...],
    ) -> bool:
        # Outer container check
        if not isinstance(value, origin):
            return False

        # Recursively check elements for known homogeneous containers
        if not args:
            return True

        # list[str]
        if origin is list and isinstance(value, list):
            subtype = args[0]
            items = ApatheticUtils_Internal_Types.cast_hint(list[Any], value)
            return all(
                ApatheticUtils_Internal_Types.safe_isinstance(v, subtype) for v in items
            )

        # dict[str, int]
        if origin is dict and isinstance(value, dict):
            key_t, val_t = args if len(args) == 2 else (Any, Any)  # noqa: PLR2004
            dct = ApatheticUtils_Internal_Types.cast_hint(dict[Any, Any], value)
            return all(
                ApatheticUtils_Internal_Types.safe_isinstance(k, key_t)
                and ApatheticUtils_Internal_Types.safe_isinstance(v, val_t)
                for k, v in dct.items()
            )

        # Tuple[str, int] etc.
        if origin is tuple and isinstance(value, tuple):
            subtypes = args
            tup = ApatheticUtils_Internal_Types.cast_hint(tuple[Any, ...], value)
            # Check for Ellipsis first (tuple[str, ...])
            if len(subtypes) == 2 and subtypes[1] is Ellipsis:  # noqa: PLR2004
                return all(
                    ApatheticUtils_Internal_Types.safe_isinstance(v, subtypes[0])
                    for v in tup
                )
            # Fixed-length tuples (tuple[str, int])
            if len(subtypes) == len(tup):
                return all(
                    ApatheticUtils_Internal_Types.safe_isinstance(v, t)
                    for v, t in zip(tup, subtypes, strict=False)
                )
            return False

        return True  # e.g., other typing origins like set[], Iterable[]

    @staticmethod
    def safe_isinstance(value: Any, expected_type: Any) -> bool:  # noqa: PLR0911
        """Like isinstance(), but safe for TypedDicts and typing generics.

        Handles:
          - typing.Union, Optional, Any
          - typing.NotRequired
          - TypedDict subclasses
          - list[...] with inner types
          - Defensive fallback for exotic typing constructs
        """
        # --- Always allow Any ---
        if expected_type is Any:
            return True

        origin = get_origin(expected_type)
        args = get_args(expected_type)

        # --- Handle NotRequired (extract inner type) ---
        if origin is NotRequired:
            # NotRequired[str] → validate as str
            if args:
                return ApatheticUtils_Internal_Types.safe_isinstance(value, args[0])
            return True

        # --- Handle Literals explicitly ---
        if origin is Literal:
            # Literal["x", "y"] → True if value equals any of the allowed literals
            return value in args

        # --- Handle Unions (includes Optional) ---
        if origin in {Union, UnionType}:
            # e.g. Union[str, int]
            return any(
                ApatheticUtils_Internal_Types.safe_isinstance(value, t) for t in args
            )

        # --- Handle special case: TypedDicts ---
        try:
            if (
                isinstance(expected_type, type)
                and hasattr(expected_type, "__annotations__")
                and hasattr(expected_type, "__total__")
            ):
                # Treat TypedDict-like as dict
                return isinstance(value, dict)
        except TypeError:
            # Not a class — skip
            pass

        # --- Handle generics like list[str], dict[str, int] ---
        if origin:
            return ApatheticUtils_Internal_Types._isinstance_generics(
                value, origin, args
            )

        # --- Fallback for simple types ---
        try:
            return isinstance(value, expected_type)
        except TypeError:
            # Non-type or strange typing construct
            return False
