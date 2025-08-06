from django.db.models import Prefetch

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from django.utils import timezone
from django.conf import settings

from app_content.models.tag import Tag
from app_content.models.article import Article
from app_content.models.category import Category
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
        base_qs = (
            Article.objects.language(lang)
            .filter(status="published", published_at__lte=timezone.now())
            .select_related("author")
            .distinct("id")  # Убираем дубли до префетча
        )

        # Префетч тегов и категорий с DISTINCT уже внутри
        qs = base_qs.prefetch_related(
            Prefetch(
                "tags",
                queryset=Tag.objects.language(lang).distinct("id").order_by("id"),
            ),
            Prefetch(
                "category",
                queryset=Category.objects.language(lang).distinct("id").order_by("id"),
            ),
        ).order_by("-published_at")

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
