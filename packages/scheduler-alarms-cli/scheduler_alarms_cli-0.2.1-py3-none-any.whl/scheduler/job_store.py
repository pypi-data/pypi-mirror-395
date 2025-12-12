import json
from pathlib import Path

STORE_FILE = Path("jobs.json")

def load_jobs():
    if STORE_FILE.exists():
        return json.loads(STORE_FILE.read_text())
    return []

def save_jobs(jobs):
    STORE_FILE.write_text(json.dumps(jobs, indent=4))