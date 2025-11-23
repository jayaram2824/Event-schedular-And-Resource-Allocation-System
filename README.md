# Event Scheduling & Resource Allocation System

Minimal Flask app to schedule events and allocate shared resources (rooms, instructors, equipment) with conflict detection.

Setup
1. Create and activate a Python virtual environment (PowerShell):

```powershell
python -m venv venv; .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the app:

```powershell
python app.py
```

The app will start at `http://127.0.0.1:5000/`.

Design notes
- SQLite database stored in `instance/events.db`.
- Models: `Event`, `Resource`, `EventResourceAllocation`.
- Conflict detection: when allocating a resource to an event the server checks for any existing allocations for the same resource whose event time overlaps. Overlap logic used: `start < existing_end and end > existing_start`.

Views
- Add/Edit/View Events: `/events`, `/events/new`, `/events/edit/<id>`
- Add/Edit/View Resources: `/resources`, `/resources/new`, `/resources/edit/<id>`
- Allocate resources to events: `/allocate`
- Conflict detection is done during allocation; a dedicated `/conflicts` view was removed.

Next steps / ideas
- Add delete operations and confirmation
- Add user authentication and permissions
- Add calendar view (FullCalendar)
- Make allocation edit/remove support and advanced conflict resolution suggestions
