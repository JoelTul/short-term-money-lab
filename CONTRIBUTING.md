# Contributing

## Development

Keep each commit focused on one change.
Run the Python tests when changing Python behavior:

    .\.venv\Scripts\python.exe -m pytest -q

Document changes to calculation assumptions.
Do not commit credentials, virtual environments, or temporary downloads.
Published results should include sample dates and data sources.

## Working across computers

Commit and push before switching computers.
On the other computer, check git status first.
When the working tree is clean, run git pull --ff-only.
Each computer needs its own virtual environment.
