"""Reports which commit is running. scripts/deploy.py writes app/version.json at deploy time (git-ignored)."""
import json
from pathlib import Path

_FILE = Path(__file__).parent / "version.json"


def get_version() -> dict:
    """Return deployed commit info, or a 'dev' marker when running locally."""
    try:
        return json.loads(_FILE.read_text())
    except (OSError, ValueError):
        return {"sha": "dev", "deployed_at": None, "run_url": None}

# In app/main.py add:
#   from app.version import get_version
#   @app.get("/version")
#   def version():
#       return get_version()
