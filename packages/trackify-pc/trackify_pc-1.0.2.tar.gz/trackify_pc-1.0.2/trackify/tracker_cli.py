"""
CLI entry point for Trackify activity tracker.
"""
from trackify.tracker.main import ActivityTracker


def main():
    """Start the Trackify activity tracker."""
    tracker = ActivityTracker(check_interval=1.0)
    tracker.run()


if __name__ == "__main__":
    main()
