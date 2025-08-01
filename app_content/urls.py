from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_content.views.category import CategoryViewSet
from app_content.views.author import AuthorViewSet
from app_content.views.article import ArticleViewSet
from app_content.views.tag import TagViewSet

from app_content.views.search_wrapper import SearchViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("authors", AuthorViewSet, basename="authors")
router.register("articles", ArticleViewSet, basename="article")
router.register("tags", TagViewSet, basename="tags")
router.register("search", SearchViewSet, basename="search")

urlpatterns = [
    path("", include(router.urls)),
]
