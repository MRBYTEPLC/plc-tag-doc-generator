"""
main.py
---------
Entry point for the PLC Tag Documentation Generator.

To run in Thonny IDE:
  1. Open this file (main.py) in Thonny.
  2. Press F5 (or the "Run" button).
  3. Click "Load Sample File" to try it immediately, or "Open L5X
     File..." to load your own Studio 5000 L5X export.

Requires Python 3.8+. Tkinter and xml.etree.ElementTree are part of
the standard library. openpyxl and python-docx are optional, needed
only for Excel and Word export respectively.
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.gui.app import run

if __name__ == "__main__":
    run()
