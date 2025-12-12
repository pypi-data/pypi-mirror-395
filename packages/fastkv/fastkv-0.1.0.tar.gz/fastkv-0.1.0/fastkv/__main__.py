
"""
FastKV - High-performance filesystem-based key-value database
CLI Entry Point
"""

import sys
import os

# Add the parent directory to sys.path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastkv import main

if __name__ == "__main__":
    main()