"""
CLI entry point for Trackify backend server.
"""
import uvicorn


def main():
    """Start the Trackify backend API server."""
    uvicorn.run(
        "trackify.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
