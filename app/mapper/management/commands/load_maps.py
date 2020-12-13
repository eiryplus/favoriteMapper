import time
from django.core.management.base import BaseCommand
from mapper.models import Mapper
from mapper import api


class Command(BaseCommand):
    help = "登録されているMapperの曲データを取得する"

    def handle(self, *args, **options):
        for mapper in Mapper.objects.all():
            print(mapper.username + " start ", end="")
            api.create_map_data(mapper.id)
            api.upload_latest_uploaded(mapper)
            for m in mapper.map_set.filter(downloaded=False):
                m.download()
                m.extract_zip()
                print(".", end="")
                time.sleep(1)
            print("finish.")
