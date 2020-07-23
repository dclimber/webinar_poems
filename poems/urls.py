from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("poet/<int:poet_pk>/", views.poet_view, name="poet"),
    path("poem/<int:poem_pk>/", views.poem_view, name="poem"),
]
