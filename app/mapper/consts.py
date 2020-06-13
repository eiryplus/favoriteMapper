import os
from django.conf import settings

MAPPER_API_URL = "https://beatsaver.com/api/users/find/{mapper_id}"
MAP_API_URL = "https://beatsaver.com/api/maps/uploader/{mapper_id}/{page}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
}
DATA_DIR = os.path.join(settings.PROJECT_DIR, "data")
DOWNLOAD_DIR = os.path.join(DATA_DIR, "zip")
EXTRACT_DIR = os.path.join(DATA_DIR, "extract")
BASE_URL = "https://beatsaver.com"
