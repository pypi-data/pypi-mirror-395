task_manager/
├── __init__.py
├── models.py        # dataclasses for User, Task, Project
├── storage.py       # in-memory persistence (could be swapped with DB later)
├── services.py      # business logic for creating, updating, filtering tasks
├── cli.py           # simple text-based interface
├── main.py          # entrypoint
