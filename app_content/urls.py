from django.urls import path

from .views import home_view, articles_by_category, articles_by_tag, article_detail_view

urlpatterns = [
    path("", home_view, name="home"),
    path("<slug:slug>/", home_view, name="article_detail"),
    path("tag/<slug:slug>/", articles_by_tag, name="articles_by_tag"),
    path("category/<slug:slug>/", articles_by_category, name="articles_by_category"),
    path("article/<slug:slug>/", article_detail_view, name="article_detail"),
]
