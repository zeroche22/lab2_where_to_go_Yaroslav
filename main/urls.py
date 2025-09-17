from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("places/", views.place_list, name="place_list"),
    path("places/add/", views.add_place, name="add_place"),
    path("places/<int:idx>/", views.place_detail, name="place_detail"),
    path("random/", views.random_place, name="random_place"),
]
