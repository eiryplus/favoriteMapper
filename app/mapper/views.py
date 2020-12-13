from django.views.generic import ListView

from mapper.models import Mapper, Map


class MapperList(ListView):
    model = Mapper
    ordering = "-latest_uploaded"
    template_name = "mapper/mapper_list.html"


class MapList(ListView):
    model = Map
    template_name = "mapper/map_list.html"

    def get_queryset(self):
        return Map.objects.all().select_related("mapper").order_by("-uploaded")
