from datetime import datetime
import json
import time

import requests

from mapper import consts
from mapper.models import Mapper, Map


def _fetch_maps(user_id: str, page: int = 0):
    url = consts.MAP_API_URL.format(mapper_id=user_id, page=page)
    response = requests.get(url=url, headers=consts.headers)
    return response.json()


def _fetch_all_map(mapper_id: str):
    next_page = 0
    while next_page is not None:
        data = _fetch_maps(mapper_id, next_page)
        yield data.get("docs")


def create_map_data(mapper_id: str):
    for maps in _fetch_all_map(mapper_id):
        time.sleep(0.7)
        for data in maps:
            s = data.get("uploaded").replace("Z", "+00:00")
            uploaded = datetime.fromisoformat(s)
            defaults = dict(
                mapper_id=mapper_id,
                uploaded=uploaded,
                name=data.get("name"),
                origin=json.dumps(data),
                duration=data.get("metadata").get("duration"),
            )
            map_, is_new = Map.objects.get_or_create(
                id=data.get("key"), defaults=defaults
            )
            if not is_new:
                # マップは登録日降順で取得できるため、取り込み済みのデータが
                # ある場合は処理を終了する
                return
            map_.save()
