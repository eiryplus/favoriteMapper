from django.core.management.base import BaseCommand
from mapper.models import Map


class Command(BaseCommand):
    help = "登録されているMapperの曲データを取得する"

    def handle(self, *args, **options):
        pass
        # for m in Map.objects.filter(downloaded=True):
        #     m.extract_zip()
