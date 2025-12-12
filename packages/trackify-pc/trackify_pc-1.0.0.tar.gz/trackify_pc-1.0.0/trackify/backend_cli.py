"""
CLI entry point for Trackify backend server.
"""
import uvicorn
import sys
import os


def main():
    """Start the Trackify backend API server."""
    # Add parent directory to path for imports
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
