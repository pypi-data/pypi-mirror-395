from . import server  # This ensures server module is fully loaded and initialized
from .server import serve
import sys
import io

def main():
  if sys.platform == "win32":
      sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
      sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
  serve()

if __name__ == "__main__":
    main()
