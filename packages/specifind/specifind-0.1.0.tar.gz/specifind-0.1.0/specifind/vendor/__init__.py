import sys

from pathlib import Path

vendor_dir = str(Path(__file__).parent)
if vendor_dir not in sys.path:
    sys.path.insert(0, vendor_dir)
