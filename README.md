# Tree
Family Tree application

## Current project status
This repository now includes a working backend API scaffold for a family tree application using **FastAPI + SQLite**.

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
- `PATCH /people/{person_id}`
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

## Next steps
1. Build React frontend using a graph UI library (for example, React Flow).
2. Connect frontend CRUD interactions to the API.
3. Add branch collapse/expand and save state via `/tree-view-state`.
4. Add print-ready rendering and PDF export.
## Recommended approach
Given your experience, a **React frontend + Python backend** is an excellent fit for a family-tree app.

### Suggested architecture
- **Frontend (React + TypeScript)**
  - Graph rendering and interaction (zoom, pan, collapse/expand branches).
  - Person detail panels/forms for editing profile data.
- **Backend (Python FastAPI)**
  - REST API for people, relationships, notes, and media metadata.
  - Validation rules to keep family relationships consistent.
- **Database (PostgreSQL or SQLite for local-only)**
  - Persistent storage so reopening the app restores data.
- **Export service**
  - JSON export/import for backup.
  - PDF/PNG export for printing.

## Core feature plan
### 1) Data model first
Create explicit entities and relationships:
- `Person`: id, names, birth/death dates, bio, tags, photos
- `Relationship`: id, from_person_id, to_person_id, type (`parent`, `spouse`, `child`, `adopted`, etc.)
- `TreeViewState`: collapsed node ids, layout settings, zoom/pan defaults

Why first: good schema design prevents painful migrations later.

### 2) Build CRUD + persistence
Implement API endpoints:
- `POST/GET/PATCH /people`
- `POST/GET/DELETE /relationships`
- `GET/PUT /tree-view-state`
- `GET /export`, `POST /import`

This ensures all edits are saved and reloadable.

### 3) Add interactive tree UI
Use a graph library in React:
- **React Flow** (recommended for node-based editors)
- alternatives: Cytoscape.js, D3 (more custom, more work)

Required interactions:
- Add person node
- Connect people with typed relationships
- Collapse/expand descendants/ancestors
- Search/filter and focus on one branch

### 4) Person detail page/drawer
Clicking a person should open editable details:
- Core identity fields
- Timeline/events
- Notes and sources
- Media links/files

### 5) Export + print support
Start with:
- Export JSON (full fidelity backup)
- Print-friendly view (A4/Letter page modes)
- Optional PDF generation endpoint

## Tech choices for your stack
### Frontend
- React + TypeScript
- React Flow for graph editing
- Zustand/Redux for client state
- TanStack Query for API caching/sync

### Backend
- FastAPI + Pydantic + SQLAlchemy
- Alembic migrations
- PostgreSQL (production) or SQLite (single-user desktop/local)

### Optional packaging
- Web app first (fastest to ship)
- Later package as desktop with Tauri/Electron if needed offline

## Minimal MVP roadmap (practical)
1. Scaffold FastAPI + DB schema.
2. Build person/relationship CRUD.
3. Build React tree canvas with add/connect.
4. Implement collapse/expand + auto-save view state.
5. Add person detail editing.
6. Add JSON export/import.
7. Add print/PDF output.

## Key implementation notes
- Prevent invalid relationship loops where required (or clearly allow and represent them).
- Keep relationship types explicit; genealogy gets messy fast.
- Store layout and collapse state separately from genealogy facts.
- Add import/export early so users never feel trapped.

## Direct answer to your question
Yes—**React and Python are both very good choices** for this project.
- React is strong for interactive graph UIs.
- Python/FastAPI is fast for building clean APIs and persistence.

If you want the fastest path, start with a web app using React + FastAPI + PostgreSQL, then add desktop packaging only after core features are stable.
