from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery

from app_content.models.article import Article


class ArticleQuerySetFactory:
    def __init__(self, base_qs=None):
        self.qs = base_qs or self._default_queryset()

    def _default_queryset(self):
        return (
            Article.objects.language()
            .filter(status="published", published_at__lte=timezone.now())
            .select_related("author")
            .prefetch_related("tags", "category")
        )

    def filter_by_tag(self, tag):
        self.qs = self.qs.filter(tags=tag)
        return self

    def filter_by_category(self, category):
        self.qs = self.qs.filter(category=category)
        return self

    def recent_articles(self, page_number, per_page=1):
        paginator = Paginator(
            self.qs.order_by("-published_at", "-created_at"), per_page
        )
        return paginator.get_page(page_number)

    def latest_articles(self, limit=5):
        return self.qs.order_by("-published_at")[:limit]

    def last_articles_by_authors(self):
        subquery = (
            self.qs.filter(author=OuterRef("author"))
            .order_by("-published_at")
            .values("id")[:1]
        )
        return self.qs.filter(id__in=Subquery(subquery))

    def featured_articles(self, limit=5):
        return self.qs.order_by("-published_at")[:limit]
