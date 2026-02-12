from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


RelationshipLiteral = Literal["parent", "child", "spouse", "adopted", "sibling"]


class PersonBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=120)
    last_name: str | None = Field(default=None, max_length=120)
    birth_date: date | None = None
    death_date: date | None = None
    bio: str | None = None


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=120)
    last_name: str | None = Field(default=None, max_length=120)
    birth_date: date | None = None
    death_date: date | None = None
    bio: str | None = None


class Person(PersonBase):
    id: int

    model_config = {"from_attributes": True}


class RelationshipBase(BaseModel):
    from_person_id: int
    to_person_id: int
    relationship_type: RelationshipLiteral


class RelationshipCreate(RelationshipBase):
    pass


class Relationship(RelationshipBase):
    id: int

    model_config = {"from_attributes": True}


class TreeViewStatePayload(BaseModel):
    collapsed_node_ids: list[int] = Field(default_factory=list)
    viewport: dict = Field(default_factory=dict)


class ExportData(BaseModel):
    people: list[Person]
    relationships: list[Relationship]
    tree_view_state: TreeViewStatePayload
