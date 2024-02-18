from django.urls import path

from . import views

urlpatterns = [
    path("populate", views.populate_database, name="populate"),
    path("display", views.display, name="display"),
]
