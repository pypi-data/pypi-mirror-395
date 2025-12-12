"""Pydantic adapter - convert Pydantic models to Schema IR."""

from ..core import Field, Schema
from ..types import from_pydantic_field


def from_pydantic(model):
    """Convert Pydantic model to Schema IR."""
    from pydantic import BaseModel

    if not issubclass(model, BaseModel):
        raise TypeError(f"Expected Pydantic model, got {type(model)}")

    fields = [
        _build_field(name, field_info)
        for name, field_info in model.model_fields.items()
    ]

    return Schema(fields=fields, name=model.__name__)


def _build_field(name, field_info) -> Field:
    """Build Field with round-trip annotation support."""
    type_expr, annotation = from_pydantic_field(field_info)

    return Field(
        name=name,
        type=type_expr,
        optional=not field_info.is_required(),
        description=field_info.description,
        annotation=annotation,
    )
