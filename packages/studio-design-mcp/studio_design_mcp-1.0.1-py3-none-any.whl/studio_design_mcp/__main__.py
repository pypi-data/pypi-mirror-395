import sys
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from server import serve

if __name__ == "__main__":
    serve()