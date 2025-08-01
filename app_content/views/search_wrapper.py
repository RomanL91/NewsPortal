from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from app_content.views.search import FullTextSearchView, AutocompleteSearchView

from app_content.views.docs import (
    DOC_Search_EntryPoint,
    DOC_Search_FullText,
    DOC_Search_Autocomplete,
)


def set_docstring(doc):
    def decorator(func):
        func.__doc__ = doc
        return func

    return decorator


class SearchViewSet(ViewSet):
    def list(self, request):
        return Response(
            {
                "detail": "Search endpoint. Use /search/fulltext/ or /search/autocomplete/.",
            }
        )

    @action(detail=False, methods=["get"])
    @set_docstring(DOC_Search_FullText)
    def fulltext(self, request: Request):
        return FullTextSearchView().get(request)

    @action(detail=False, methods=["get"])
    @set_docstring(DOC_Search_Autocomplete)
    def autocomplete(self, request: Request):
        return AutocompleteSearchView().get(request)


SearchViewSet.__doc__ = DOC_Search_EntryPoint
