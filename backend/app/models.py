from sqlalchemy import JSON, Column, Date, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
import enum

from .db import Base


class RelationshipType(str, enum.Enum):
    parent = "parent"
    child = "child"
    spouse = "spouse"
    adopted = "adopted"
    sibling = "sibling"


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=True)
    birth_date = Column(Date, nullable=True)
    death_date = Column(Date, nullable=True)
    bio = Column(Text, nullable=True)

    outgoing_relationships = relationship(
        "Relationship",
        foreign_keys="Relationship.from_person_id",
        cascade="all, delete-orphan",
    )
    incoming_relationships = relationship(
        "Relationship",
        foreign_keys="Relationship.to_person_id",
        cascade="all, delete-orphan",
    )


class Relationship(Base):
    __tablename__ = "relationships"
    __table_args__ = (
        UniqueConstraint(
            "from_person_id",
            "to_person_id",
            "relationship_type",
            name="uq_relationship_triplet",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    from_person_id = Column(Integer, ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    to_person_id = Column(Integer, ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(Enum(RelationshipType), nullable=False)


class TreeViewState(Base):
    __tablename__ = "tree_view_state"

    id = Column(Integer, primary_key=True, default=1)
    collapsed_node_ids = Column(JSON, nullable=False, default=list)
    viewport = Column(JSON, nullable=False, default=dict)
