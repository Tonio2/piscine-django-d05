from django.urls import path

from . import views

urlpatterns = [
    path("init", views.initialize_database, name="init"),
    path("populate", views.populate_database, name="populate"),
    path("display", views.display, name="display"),
]
