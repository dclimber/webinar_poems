from django.urls import path

from . import views

urlpatterns = [
    path("", views.search, name="search"),
    path("cls/", views.SearchView.as_view(),
         name="search_view"),
    path("tpl/", views.SearchTemplateView.as_view(),
         name="search_template"),
]
