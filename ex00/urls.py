from django.urls import path

from . import views

urlpatterns = [
    path("init", views.initialize_database, name="init"),
]
