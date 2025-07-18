from django.utils.translation import get_language

from app_content.models.tag import Tag
from app_content.models.article import Article


class CategoryContentFactory:
    def __init__(self, category, lang=None):
        self.category = category
        self.lang = lang or get_language()
        self._articles = None

    def get_articles(self):
        if self._articles is None:
            self._articles = (
                Article.objects.language(self.lang)
                .filter(status="published", category=self.category)
                .order_by("-published_at")
                .select_related("author")
                .prefetch_related("tags")
            )
        return self._articles

    def get_tags(self):
        return (
            Tag.objects.language(self.lang)
            .filter(articles__in=self.get_articles())
            .distinct()
        )
