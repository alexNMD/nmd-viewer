import os

from dotenv import load_dotenv

load_dotenv()

DNS = os.getenv("NMDNS")
INSTAGRAM_URL = os.getenv("INSTAGRAM_PROFILE")
GITHUB_URL = os.getenv("GITHUB_PROFILE")

PROJECTS_PATH = os.getenv("PROJECTS_PATH", default="/app/nmd_project")
DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH", default="/app/documents")
CV_FILENAME = os.getenv("CV_FILENAME")
