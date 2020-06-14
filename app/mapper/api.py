from datetime import datetime
import json
import time
import os

import requests

from mapper import consts
from mapper.models import Map, DIFFICULTY_DICT


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
        time.sleep(0.9)
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


def _get_difficulty_data(m: Map):
    map_sets = m.info_dat.get("_difficultyBeatmapSets", [])
    map_sets = list(filter(
        lambda s: s.get("_beatmapCharacteristicName") == "Standard",
        map_sets
    ))
    if not map_sets:
        return []
    difficulties = map_sets[0].get("_difficultyBeatmaps")
    result = list()
    for d in difficulties:
        file_path = os.path.join(m.extract_path, d.get("_beatmapFilename"))
        if not d.get("_difficulty") not in DIFFICULTY_DICT:
            raise ValueError("想定している難易度ではありません")
        with open(file_path, "r", encoding="utf-8") as fp:
            tmp = dict(
                level=DIFFICULTY_DICT.get(d.get("_difficulty")),
                file_name=json.load(fp),
                speed=d.get("_noteJumpMovementSpeed"),
            )
        result.append(tmp)
    return result


def create_difficulty(m: Map):
    m.duration = m.music_file_duration
    m.save()
    difficulty_data = _get_difficulty_data(m)
    for d in difficulty_data:
        # TODO: Difficulty データを生成する
        print(d)
