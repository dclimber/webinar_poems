from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("poet/<int:poet_pk>/", views.poet_view, name="poet"),
    path("poem/<int:poem_pk>/", views.poem_view, name="poem"),
    path("poem/add/", views.add_poem, name="add_poem"),
    path("poem/<int:poem_pk>/edit/", views.update_poem, name="update_poem"),
]
