from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.displayContent, name="title"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("random/", views.randomPage, name="random"),
    path("edit/<str:title>", views.edit, name="edit")
]
