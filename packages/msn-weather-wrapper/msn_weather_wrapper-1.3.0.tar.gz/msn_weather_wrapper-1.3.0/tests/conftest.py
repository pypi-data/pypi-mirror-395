"""Pytest configuration and fixtures for all tests."""

import os

# Set environment variables before any imports that might use them
# This ensures the Flask app can initialize properly in test mode
os.environ["FLASK_ENV"] = "development"
os.environ["FLASK_DEBUG"] = "1"
os.environ["TESTING"] = "1"

# Optional: Set other test-specific environment variables
os.environ.setdefault("CORS_ORIGINS", "http://localhost:5173")
os.environ.setdefault("RATE_LIMIT_PER_IP", "100")
os.environ.setdefault("RATE_LIMIT_GLOBAL", "1000")
