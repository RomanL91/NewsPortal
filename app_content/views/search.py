from django.db.models import F, Value, CharField, Q
from django.db.models.functions import Greatest
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
    TrigramSimilarity,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from app_content.models.article import Article
from app_content.models.tag import Tag
from app_content.models.category import Category


def get_search_config(lang_code: str) -> str:
    """
    Безопасное преобразование языка в конфигурацию PostgreSQL.
    """
    return {
        "ru": "russian",
        "kk": "simple",
    }.get(lang_code.lower(), "simple")


class AutocompleteSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q")
        if not query or len(query.strip()) < 1:
            return Response(
                {"detail": "Missing or empty 'q' parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        lang = getattr(request, "LANGUAGE_CODE", settings.LANGUAGE_CODE)

        # === ARTICLES ===
        article_qs = (
            Article.objects.language(lang)
            .filter(status="published")
            .annotate(
                similarity=TrigramSimilarity("translations__title", query),
                type=Value("article", output_field=CharField()),
                title=F("translations__title"),
            )
            .filter(similarity__gt=0.05)  # сниженный порог
            .order_by("-similarity")
            .values("type", "id", "title", "similarity")[:5]
        )

        # === TAGS ===
        tag_qs = (
            Tag.objects.language(lang)
            .annotate(
                similarity=TrigramSimilarity("translations__name", query),
                type=Value("tag", output_field=CharField()),
                title=F("translations__name"),
            )
            .filter(similarity__gt=0.05)
            .order_by("-similarity")
            .values("type", "id", "title", "similarity")[:5]
        )

        # === CATEGORIES ===
        cat_qs = (
            Category.objects.language(lang)
            .annotate(
                similarity=TrigramSimilarity("translations__name", query),
                type=Value("category", output_field=CharField()),
                title=F("translations__name"),
            )
            .filter(similarity__gt=0.05)
            .order_by("-similarity")
            .values("type", "id", "title", "similarity")[:5]
        )

        # Объединяем и возвращаем
        results = {
            "articles": list(article_qs),
            "tags": list(tag_qs),
            "categories": list(cat_qs),
        }

        return Response(results)


class FullTextSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q")
        if not query or len(query.strip()) < 1:
            return Response(
                {"detail": "Missing or empty 'q' parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        lang = getattr(request, "LANGUAGE_CODE", settings.LANGUAGE_CODE)
        search_config = get_search_config(lang)
        search_query = SearchQuery(query, config=search_config)

        # === Поиск по статьям ===
        article_vector = (
            SearchVector("translations__title", weight="A", config=search_config)
            + SearchVector("translations__summary", weight="B", config=search_config)
            + SearchVector("translations__content", weight="C", config=search_config)
        )

        article_qs = (
            Article.objects.language(lang)
            .filter(status="published")
            .annotate(
                search=article_vector,
                rank=SearchRank(article_vector, search_query),
                similarity=TrigramSimilarity("translations__title", query),
                type=Value("article", output_field=CharField()),
                title=F("translations__title"),
                slug=F("translations__slug"),
                snippet=SearchHeadline(
                    "translations__content",
                    search_query,
                    config=search_config,
                    start_sel="<mark>",
                    stop_sel="</mark>",
                    max_words=35,
                    min_words=10,
                    short_word=3,
                    max_fragments=1,
                ),
            )
            .filter(Q(search=search_query) | Q(similarity__gt=0.2))
            .annotate(final_score=Greatest("rank", "similarity"))
            .values("type", "id", "title", "slug", "final_score", "snippet")[:10]
        )

        # === Поиск по тегам ===
        tag_vector = SearchVector(
            "translations__name", weight="A", config=search_config
        )
        tag_qs = (
            Tag.objects.language(lang)
            .annotate(
                search=tag_vector,
                rank=SearchRank(tag_vector, search_query),
                similarity=TrigramSimilarity("translations__name", query),
                type=Value("tag", output_field=CharField()),
                title=F("translations__name"),
                slug=F("translations__slug"),
                snippet=SearchHeadline(
                    "translations__name", search_query, config=search_config
                ),
            )
            .filter(Q(search=search_query) | Q(similarity__gt=0.2))
            .annotate(final_score=Greatest("rank", "similarity"))
            .values("type", "id", "title", "slug", "final_score", "snippet")[:10]
        )

        # === Поиск по категориям ===
        cat_vector = SearchVector(
            "translations__name", weight="A", config=search_config
        )
        cat_qs = (
            Category.objects.language(lang)
            .annotate(
                search=cat_vector,
                rank=SearchRank(cat_vector, search_query),
                similarity=TrigramSimilarity("translations__name", query),
                type=Value("category", output_field=CharField()),
                title=F("translations__name"),
                slug=F("translations__slug"),
                snippet=SearchHeadline(
                    "translations__name", search_query, config=search_config
                ),
            )
            .filter(Q(search=search_query) | Q(similarity__gt=0.2))
            .annotate(final_score=Greatest("rank", "similarity"))
            .values("type", "id", "title", "slug", "final_score", "snippet")[:10]
        )

        # Объединяем и сортируем
        combined = list(article_qs) + list(tag_qs) + list(cat_qs)
        results = sorted(combined, key=lambda x: x["final_score"], reverse=True)

        return Response(results)
