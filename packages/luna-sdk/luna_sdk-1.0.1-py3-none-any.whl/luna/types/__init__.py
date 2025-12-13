"""Type definitions for Luna SDK."""

from __future__ import annotations

from typing import TypeVar
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Pagination parameters for list requests."""

    limit: int | None = Field(default=20, ge=1, le=100)
    cursor: str | None = None


T = TypeVar("T")


class ListResponse(BaseModel):
    """Generic list response with pagination."""

    has_more: bool
    next_cursor: str | None = None


class User(BaseModel):
    """User resource."""

    id: str
    email: str
    name: str
    avatar_url: str | None = None
    created_at: str
    updated_at: str


class UserCreate(BaseModel):
    """Parameters for creating a user."""

    email: str
    name: str
    avatar_url: str | None = None


class UserUpdate(BaseModel):
    """Parameters for updating a user."""

    name: str | None = None
    avatar_url: str | None = None


class UserList(ListResponse):
    """Paginated list of users."""

    data: list[User]


class Project(BaseModel):
    """Project resource."""

    id: str
    name: str
    description: str | None = None
    owner_id: str
    created_at: str
    updated_at: str


class ProjectCreate(BaseModel):
    """Parameters for creating a project."""

    name: str
    description: str | None = None


class ProjectUpdate(BaseModel):
    """Parameters for updating a project."""

    name: str | None = None
    description: str | None = None


class ProjectList(ListResponse):
    """Paginated list of projects."""

    data: list[Project]


class ResidenceLocation(BaseModel):
    """Location of a residence."""

    latitude: float
    longitude: float
    suburb: str | None = None
    city: str | None = None


class Residence(BaseModel):
    """Residence resource."""

    id: str
    name: str
    slug: str
    address: str
    description: str | None = None

    # Filters & Attributes
    is_nsfas_accredited: bool
    min_price: float
    max_price: float
    currency_code: str
    gender_policy: str  # 'mixed' | 'male' | 'female'

    # Location & Relations
    location: ResidenceLocation
    campus_ids: list[str]

    # Social
    rating: float
    review_count: int

    images: list[str]
    amenities: list[str]


class ResidenceSearch(PaginationParams):
    """Search/Filter parameters for residences."""

    query: str | None = None
    nsfas: bool | None = None
    min_price: float | None = None
    max_price: float | None = None
    gender: str | None = None
    campus_id: str | None = None
    radius: float | None = None
    min_rating: float | None = None


class ResidenceList(ListResponse):
    """Paginated list of residences."""

    data: list[Residence]


class CampusLocation(BaseModel):
    """Location of a campus."""
    latitude: float
    longitude: float


class Campus(BaseModel):
    """Campus resource."""

    id: str
    name: str
    location: CampusLocation


class CampusList(ListResponse):
    """List of campuses."""

    data: list[Campus]


class Group(BaseModel):
    """Group resource."""

    id: str
    name: str
    description: str | None = None
    permissions: list[str]
    member_ids: list[str]


class GroupCreate(BaseModel):
    """Parameters for creating a group."""

    name: str
    description: str | None = None
    permissions: list[str] | None = None
    member_ids: list[str] | None = None


class GroupList(ListResponse):
    """Paginated list of groups."""

    data: list[Group]


class Bucket(BaseModel):
    """Storage Bucket."""

    id: str
    name: str
    public: bool
    created_at: str
    region: str | None = None


class BucketList(ListResponse):
    """List of buckets."""

    data: list[Bucket]


class FileObject(BaseModel):
    """File object."""

    id: str
    bucket_id: str
    key: str
    size: int
    content_type: str
    url: str


class CompletionRequest(BaseModel):
    """AI Completion Request."""
    model: str
    messages: list[dict[str, str]]
    temperature: float | None = None


class CompletionResponse(BaseModel):
    """AI Completion Response."""
    id: str
    choices: list[dict[str, Any]]


class Workflow(BaseModel):
    """Automation Workflow."""

    id: str
    name: str
    trigger_type: str
    is_active: bool


class WorkflowList(ListResponse):
    """List of workflows."""

    data: list[Workflow]


class WorkflowRun(BaseModel):
    """Workflow Run status."""

    id: str
    workflow_id: str
    status: str
    started_at: str
