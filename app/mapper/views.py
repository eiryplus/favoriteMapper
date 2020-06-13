from django.views.generic import ListView

from mapper.models import Mapper, Map


class MapperList(ListView):
    model = Mapper


class MapList(ListView):
    model = Map

    def get_queryset(self):
        return Map.objects.all().select_related("mapper").order_by("-uploaded")
