from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("poet/<int:poet_pk>/", views.poet_view, name="poet"),
]
