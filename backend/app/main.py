from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import Person, Relationship, TreeViewState
from .schemas import (
    ExportData,
    PersonCreate,
    Person as PersonSchema,
    PersonUpdate,
    Relationship as RelationshipSchema,
    RelationshipCreate,
    TreeViewStatePayload,
)

app = FastAPI(title="Tree API", version="0.1.0")
Base.metadata.create_all(bind=engine)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/people", response_model=PersonSchema, status_code=status.HTTP_201_CREATED)
def create_person(payload: PersonCreate, db: Session = Depends(get_db)):
    person = Person(**payload.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@app.get("/people", response_model=list[PersonSchema])
def list_people(db: Session = Depends(get_db)):
    return db.query(Person).order_by(Person.id.asc()).all()


@app.patch("/people/{person_id}", response_model=PersonSchema)
def update_person(person_id: int, payload: PersonUpdate, db: Session = Depends(get_db)):
    person = db.get(Person, person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(person, key, value)

    db.commit()
    db.refresh(person)
    return person


@app.post("/relationships", response_model=RelationshipSchema, status_code=status.HTTP_201_CREATED)
def create_relationship(payload: RelationshipCreate, db: Session = Depends(get_db)):
    if payload.from_person_id == payload.to_person_id:
        raise HTTPException(status_code=400, detail="Self relationships are not allowed")

    from_person = db.get(Person, payload.from_person_id)
    to_person = db.get(Person, payload.to_person_id)
    if not from_person or not to_person:
        raise HTTPException(status_code=404, detail="Referenced person not found")

    relationship = Relationship(**payload.model_dump())
    db.add(relationship)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Relationship already exists")

    db.refresh(relationship)
    return relationship


@app.get("/relationships", response_model=list[RelationshipSchema])
def list_relationships(db: Session = Depends(get_db)):
    return db.query(Relationship).order_by(Relationship.id.asc()).all()


@app.delete("/relationships/{relationship_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_relationship(relationship_id: int, db: Session = Depends(get_db)):
    relationship = db.get(Relationship, relationship_id)
    if not relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")

    db.delete(relationship)
    db.commit()


@app.get("/tree-view-state", response_model=TreeViewStatePayload)
def get_tree_view_state(db: Session = Depends(get_db)):
    state = db.get(TreeViewState, 1)
    if not state:
        return TreeViewStatePayload()
    return TreeViewStatePayload(collapsed_node_ids=state.collapsed_node_ids, viewport=state.viewport)


@app.put("/tree-view-state", response_model=TreeViewStatePayload)
def put_tree_view_state(payload: TreeViewStatePayload, db: Session = Depends(get_db)):
    state = db.get(TreeViewState, 1)
    if not state:
        state = TreeViewState(id=1)
        db.add(state)

    state.collapsed_node_ids = payload.collapsed_node_ids
    state.viewport = payload.viewport
    db.commit()

    return payload


@app.get("/export", response_model=ExportData)
def export_data(db: Session = Depends(get_db)):
    people = db.query(Person).order_by(Person.id.asc()).all()
    relationships = db.query(Relationship).order_by(Relationship.id.asc()).all()
    state = db.get(TreeViewState, 1)
    payload = TreeViewStatePayload()
    if state:
        payload = TreeViewStatePayload(
            collapsed_node_ids=state.collapsed_node_ids,
            viewport=state.viewport,
        )

    return ExportData(people=people, relationships=relationships, tree_view_state=payload)


@app.post("/import", response_model=ExportData)
def import_data(payload: ExportData, db: Session = Depends(get_db)):
    db.query(Relationship).delete()
    db.query(Person).delete()
    db.query(TreeViewState).delete()
    db.commit()

    for person in payload.people:
        db.add(Person(**person.model_dump()))
    db.commit()

    for relationship in payload.relationships:
        db.add(Relationship(**relationship.model_dump()))

    db.add(
        TreeViewState(
            id=1,
            collapsed_node_ids=payload.tree_view_state.collapsed_node_ids,
            viewport=payload.tree_view_state.viewport,
        )
    )
    db.commit()

    return payload
