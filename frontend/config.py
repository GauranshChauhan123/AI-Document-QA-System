import os

# When running in Docker the compose file injects BACKEND_URL=http://backend:8000.
# For local development it falls back to localhost.
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")