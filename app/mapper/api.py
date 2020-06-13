from datetime import datetime
import json
import time

import requests

from mapper import consts
from mapper.models import (
    Mapper,
    Map
)


def _fetch_maps(user_id: str, page: int = 0):
    url = consts.MAP_API_URL.format(mapper_id=user_id, page=page)
    response = requests.get(url=url, headers=consts.headers)
    return response.json()


def _fetch_all_map(mapper_id: str):
    result = []
    next_page = 0
    while next_page is not None:
        data = _fetch_maps(mapper_id, next_page)
        result += data.get("docs")
        next_page = data.get("nextPage")
        time.sleep(0.5)
    return result


def create_map_data(mapper_id: str):
    maps = _fetch_all_map(mapper_id)
    for data in maps:
        s = data.get("uploaded").replace('Z', '+00:00')
        uploaded = datetime.fromisoformat(s)
        defaults = dict(
            mapper_id=mapper_id,
            uploaded=uploaded,
            name=data.get("name"),
            origin=json.dumps(data),
            duration=data.get("metadata").get("duration")
        )
        map_, _ = Map.objects.get_or_create(id=data.get("key"), defaults=defaults)
        map_.save()
