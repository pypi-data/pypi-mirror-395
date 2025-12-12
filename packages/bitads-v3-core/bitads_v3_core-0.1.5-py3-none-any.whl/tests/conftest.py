"""
Pytest configuration for bitads_v3_core tests.

This ensures the package is importable during testing.
"""
import sys
from pathlib import Path

# Add the project root to the path so we can import bitads_v3_core
# The package is located at bitads_v3_core/bitads_v3_core/
# This is needed when running tests before the package is installed
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

