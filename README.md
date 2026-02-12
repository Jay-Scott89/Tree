# Tree
Family Tree application

## Current project status
This repository includes a working backend API scaffold for a family tree application using **FastAPI + SQLite**.

## Quick start
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs are available at:
- `http://127.0.0.1:8000/docs`

## Implemented endpoints
- `GET /health`
- `POST /people`
- `GET /people`
- `GET /people/{person_id}`
- `PATCH /people/{person_id}`
- `DELETE /people/{person_id}`
- `POST /relationships`
- `GET /relationships`
- `DELETE /relationships/{relationship_id}`
- `GET /tree-view-state`
- `PUT /tree-view-state`
- `GET /export`
- `POST /import`

## Data model
### Person
- First name, last name
- Birth and death dates
- Bio/details field

### Relationship
- `from_person_id`
- `to_person_id`
- `relationship_type` (`parent`, `child`, `spouse`, `adopted`, `sibling`)

### Tree view state
- Collapsed node ids
- Viewport object (for zoom/pan/layout state)

## Notes
- Persistence defaults to local SQLite (`tree.db`).
- You can override DB connection with `DATABASE_URL`.

## Next steps
1. Build React frontend using a graph UI library (for example, React Flow).
2. Connect frontend CRUD interactions to the API.
3. Add branch collapse/expand and save state via `/tree-view-state`.
4. Add print-ready rendering and PDF export.
