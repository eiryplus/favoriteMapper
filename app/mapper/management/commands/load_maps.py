from django.core.management.base import BaseCommand
from mapper.models import (
    Mapper,
    Map
)
from mapper import api


class Command(BaseCommand):
    help = '登録されているMapperの曲データを取得する'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for mapper in Mapper.objects.all():
            api.create_map_data(mapper.id)

