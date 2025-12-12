"""
CLI entry point for Trackify activity tracker.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tracker.main import ActivityTracker


def main():
    """Start the Trackify activity tracker."""
    tracker = ActivityTracker(check_interval=1.0)
    tracker.run()


if __name__ == "__main__":
    main()
