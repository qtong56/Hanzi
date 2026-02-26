import sys
from pathlib import Path

# Add backend/ to sys.path so `from app.services.segmentation import ...` works
sys.path.insert(0, str(Path(__file__).parent.parent))
