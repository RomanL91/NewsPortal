from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from django.utils import timezone
from django.conf import settings

from app_content.models.article import Article
from app_content.serializers.article import (
    ArticleListSerializer,
    ArticleDetailSerializer,
)

from app_content.views.docs import DOC_Article_View_Set


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):

    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        lang = getattr(
            self.request, "LANGUAGE_CODE", getattr(settings, "LANGUAGE_CODE", "ru")
        )
        qs = (
            Article.objects.language(lang)
            .filter(status="published", published_at__lte=timezone.now())
            .select_related("author")
            .prefetch_related("tags", "category")
            .order_by("-published_at")
        )

        category = self.request.query_params.get("category")
        tag = self.request.query_params.get("tag")
        author = self.request.query_params.get("author")

        if category:
            qs = qs.filter(category__id=category)
        if tag:
            qs = qs.filter(tags__id=tag)
        if author:
            qs = qs.filter(author__id=author)

        return qs.distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ArticleDetailSerializer
        return ArticleListSerializer


ArticleViewSet.__doc__ = DOC_Article_View_Set
