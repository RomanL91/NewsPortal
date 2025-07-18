from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings

from app_content.models.category import Category
from app_content.serializers.category import (
    CategorySerializer,
    CategoryDetailSerializer,
)

from app_content.views.docs import DOC_Category_View_Set


class CategoryViewSet(viewsets.ViewSet):

    def _get_lang(self, request):
        return getattr(
            request, "LANGUAGE_CODE", getattr(settings, "LANGUAGE_CODE", "ru")
        )

    def list(self, request):
        lang = self._get_lang(request)
        queryset = Category.objects.language(lang).all()

        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = CategorySerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        lang = self._get_lang(request)

        try:
            category = Category.objects.language(lang).get(pk=pk)
        except Category.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryDetailSerializer(category, context={"request": request})
        return Response(serializer.data)


CategoryViewSet.__doc__ = DOC_Category_View_Set
