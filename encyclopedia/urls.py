from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("entrysearch", views.entrysearch, name="entrysearch"),
    path("entrynew", views.entrynew, name="entrynew"),
    path("wiki/<str:entry>/edit", views.entryedit, name="entryedit"),
    path("entryrandom", views.entryrandom, name="entryrandom")
]
