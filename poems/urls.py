from django.urls import path

from . import views

fbv_patterns = [
    path("", views.index, name="index"),
    path("poet/<int:pk>/", views.poet_view, name="poet"),
    path("poet/add/", views.poet_create, name="add_poet"),
    path("poet/<int:pk>/edit/", views.poet_update, name="update_poet"),
    path("poet/<int:pk>/delete/", views.poet_delete, name="delete_poet"),

    path("poem/<int:pk>/", views.poem_view, name="poem"),
    path("poem/add/", views.poem_create, name="add_poem"),
    path("poem/<int:pk>/edit/", views.poem_update, name="update_poem"),
    path("poem/<int:pk>/delete/", views.poem_delete, name="delete_poem"),
]

cbv_patterns = [

]

urlpatterns = fbv_patterns
