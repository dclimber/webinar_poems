from django.urls import path

from . import views
from . import views_cbv as cbv

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
    path("", cbv.Index.as_view(), name="index"),
    path("poet/<int:pk>/", cbv.PoetView.as_view(), name="poet"),
    path("poet/add/", cbv.PoetCreate.as_view(), name="add_poet"),
    path("poet/<int:pk>/edit/", cbv.PoetUpdate.as_view(),
         name="update_poet"),
    path("poet/<int:pk>/delete/", cbv.PoetDelete.as_view(),
         name="delete_poet"),

    path("poem/<int:pk>/", cbv.PoemView.as_view(), name="poem"),
    path("poem/add/", cbv.PoemCreate.as_view(), name="add_poem"),
    path("poem/<int:pk>/edit/", cbv.PoemUpdate.as_view(),
         name="update_poem"),
    path("poem/<int:pk>/delete/", cbv.PoemDelete.as_view(),
         name="delete_poem"),
]

urlpatterns = cbv_patterns
