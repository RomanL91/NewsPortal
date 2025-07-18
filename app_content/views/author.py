from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings
from django.contrib.auth import get_user_model

from app_content.serializers.author import AuthorSerializer, AuthorDetailSerializer
from app_content.services.author_content_factory import AuthorContentFactory

from app_content.views.docs import DOC_Author_View_Set


User = get_user_model()


class AuthorViewSet(viewsets.ViewSet):

    def _get_lang(self, request):
        return getattr(
            request, "LANGUAGE_CODE", getattr(settings, "LANGUAGE_CODE", "ru")
        )

    def list(self, request):
        lang = self._get_lang(request)

        queryset = (
            User.objects.filter(articles__status="published")
            .distinct()
            .prefetch_related("articles")
        )

        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = AuthorSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        lang = self._get_lang(request)

        try:
            author = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        factory = AuthorContentFactory(author, lang)

        # Применяем пагинацию к статьям автора
        paginator = LimitOffsetPagination()
        paginated_articles = paginator.paginate_queryset(
            factory.get_articles(), request
        )

        # Передаём пагинированные статьи через context
        serializer = AuthorDetailSerializer(
            author,
            context={
                "request": request,
                "articles_page": paginated_articles,
                "tags_qs": factory.get_tags(),
            },
        )
        return Response(serializer.data)


AuthorViewSet.__doc__ = DOC_Author_View_Set
