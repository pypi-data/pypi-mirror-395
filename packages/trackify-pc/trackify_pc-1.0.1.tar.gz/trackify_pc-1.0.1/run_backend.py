"""
Helper script to run the backend server from the project root.
This ensures proper module resolution for package imports.
"""
import uvicorn


def main():
    """Main entry point for the backend server."""
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
