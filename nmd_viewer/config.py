import os

from dotenv import load_dotenv

load_dotenv()

DNS = "https://nmd.ddns.net"
INSTAGRAM_URL = "https://www.instagram.com/alexxnmd/"
GITHUB_URL = "https://github.com/alexNMD"

PROJECTS_PATH = "/app/nmd_project"
DOCUMENTS_PATH = "/app/documents"
CV_FILENAME = os.getenv("CV_FILENAME")
