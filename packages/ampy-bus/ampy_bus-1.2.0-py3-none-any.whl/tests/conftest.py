"""
Pytest configuration for ampy-bus tests.

This file ensures that the ampybus package can be imported during testing,
even if it's not installed in the environment.
"""
import sys
from pathlib import Path

# Add the parent directory to sys.path so we can import ampybus
# This allows tests to run without requiring 'pip install -e .'
project_root = Path(__file__).parent.parent.parent
python_dir = project_root / "python"
if str(python_dir) not in sys.path:
    sys.path.insert(0, str(python_dir))

