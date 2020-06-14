import time
from django.core.management.base import BaseCommand
from mapper.models import Map


class Command(BaseCommand):
    help = "Mapファイルを取得する"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for m in Map.objects.filter(downloaded=False):
            m.download()
            time.sleep(1)
