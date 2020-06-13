from django.urls import path
from mapper import views

urlpatterns = [
    path("", views.MapperList.as_view(), name="mapper_list"),
    path("map", views.MapList.as_view(), name="map_list"),
]
