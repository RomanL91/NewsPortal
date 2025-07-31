from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings

from app_content.models.tag import Tag
from app_content.serializers.tag import TagSerializer

from app_content.views.docs import DOC_Tag_View_Set


class TagViewSet(viewsets.ViewSet):
    def _get_lang(self, request):
        return getattr(
            request, "LANGUAGE_CODE", getattr(settings, "LANGUAGE_CODE", "ru")
        )

    def list(self, request):
        lang = self._get_lang(request)
        queryset = Tag.objects.language(lang).all().distinct("id")

        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = TagSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        lang = self._get_lang(request)
        try:
            tag = Tag.objects.language(lang).get(pk=pk)
        except Tag.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TagSerializer(tag, context={"request": request})
        return Response(serializer.data)


TagViewSet.__doc__ = DOC_Tag_View_Set
