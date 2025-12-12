from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class Component(BaseModel):
    """A processed visual component."""

    id: UUID
    type: str
    label: str
    description: Optional[str] = None
    content: Optional[str] = None
    render_svg: Optional[str] = None
    grounding: Optional[dict] = None


class ComponentDeleteResponse(BaseModel):
    """Response from deleting a component."""

    message: str
    component_id: UUID
