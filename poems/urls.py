from django.urls import path

from . import views

fbv_patterns = [
    path("", views.index, name="index"),
    path("poet/<int:poet_pk>/", views.poet_view, name="poet"),
    path("poet/add/", views.add_poet, name="add_poet"),
    path("poet/<int:poet_pk>/edit/", views.update_poet, name="update_poet"),
    path("poet/<int:poet_pk>/delete/", views.delete_poet, name="delete_poet"),

    path("poem/<int:poem_pk>/", views.poem_view, name="poem"),
    path("poem/add/", views.add_poem, name="add_poem"),
    path("poem/<int:poem_pk>/edit/", views.update_poem, name="update_poem"),
    path("poem/<int:poem_pk>/delete/", views.delete_poem, name="delete_poem"),
]

cbv_patterns = [

]

urlpatterns = fbv_patterns
