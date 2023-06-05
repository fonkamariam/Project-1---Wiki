from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("New_Page", views.cnp, name="cnp"),
    path("Random_Page", views.rp, name="rp"),
    path("WIKI/<str:x>", views.get, name='get')
]

