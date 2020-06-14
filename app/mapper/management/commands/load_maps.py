from django.core.management.base import BaseCommand
from mapper.models import Mapper
from mapper import api


class Command(BaseCommand):
    help = "登録されているMapperの曲データを取得する"

    def handle(self, *args, **options):
        for mapper in Mapper.objects.all():
            api.create_map_data(mapper.id)
