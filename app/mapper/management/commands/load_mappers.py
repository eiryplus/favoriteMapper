import requests
import os
import time

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from mapper import consts
from mapper.models import Mapper, Map


class Command(BaseCommand):
    help = "登録されているMapperのデータを取得する"

    @staticmethod
    def _get_mapper(mapper_id: str) -> dict:
        try:
            url = consts.MAPPER_API_URL.format(mapper_id=mapper_id)
            response = requests.get(url=url, headers=consts.headers)
            return response.json()
        except:
            print(mapper_id)
            raise Exception()

    @staticmethod
    def _get_mapper_ids():
        file = os.path.join(settings.PROJECT_DIR, "tmp", "mappers.txt")
        with open(file, "r") as fp:
            result = [line.strip().split("/")[-1].split("#")[0] for line in fp]
        return result

    def handle(self, *args, **options):
        objects = []
        mapper_ids = set(self._get_mapper_ids())
        exists_ids = set(Mapper.objects.all().values_list("id", flat=True))
        new_mappers = list(mapper_ids - exists_ids)
        for mapper_id in new_mappers:
            j = self._get_mapper(mapper_id)
            if not j or "username" not in j:
                continue
            mapper = Mapper(id=mapper_id)
            mapper.username = j.get("username")
            mapper.save()
            time.sleep(1)
