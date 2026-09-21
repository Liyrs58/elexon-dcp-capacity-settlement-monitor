"""Start the local synthetic service-risk monitor."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from server import serve


if __name__ == "__main__":
    serve()
