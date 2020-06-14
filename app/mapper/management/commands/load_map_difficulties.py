import time
from django.core.management.base import BaseCommand
from mapper.models import Map
from mapper import api


class Command(BaseCommand):
    help = "登録されているMapperの曲データを取得する"

    def handle(self, *args, **options):
        for m in Map.objects.filter(downloaded=True):
            m.extract_zip()
