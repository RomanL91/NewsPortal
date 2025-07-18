from django.conf import settings
from django.utils.translation import get_language
from app_content.models.article import Article
from app_content.models.tag import Tag


class AuthorContentFactory:
    def __init__(self, author, lang=None):
        self.author = author
        self.lang = lang or get_language()
        self._articles = None

    def get_articles(self):
        if self._articles is None:
            self._articles = (
                Article.objects.language(self.lang)
                .filter(status="published", author=self.author)
                .order_by("-published_at")
                .prefetch_related("tags", "category")
            )
        return self._articles

    def get_tags(self):
        return (
            Tag.objects.language(self.lang)
            .filter(articles__in=self.get_articles())
            .distinct()
        )
