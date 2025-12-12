"""Record-related models."""

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Record(BaseModel):
    """Generic record model."""

    id: str
    tenant_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_deleted: bool = False

    class Config:
        extra = "allow"  # Allow extra fields


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model."""

    data: list[T]
    total: int
    skip: int = 0
    limit: int = 100


class ObjectDefinition(BaseModel):
    """Object/table definition."""

    api_name: str
    label: str
    plural_label: Optional[str] = None
    description: Optional[str] = None
    is_custom: bool = False
    field_count: Optional[int] = None


class FieldDefinition(BaseModel):
    """Field definition."""

    api_name: str
    label: str
    field_type: str
    is_required: bool = False
    is_unique: bool = False
    max_length: Optional[int] = None
    default_value: Optional[Any] = None
    help_text: Optional[str] = None
    picklist_values: Optional[list[dict[str, Any]]] = None


class ObjectSchema(BaseModel):
    """Complete object schema with fields."""

    object: ObjectDefinition
    fields: list[FieldDefinition]
