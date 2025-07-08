from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from app_content.models.tag import Tag
from app_content.models.article import Article
from app_content.models.category import Category


def home_view(request, slug=None):
    categories = Category.objects.prefetch_related("articles").all()
    tags = Tag.objects.all()

    if slug:
        tag = get_object_or_404(Tag, translations__slug=slug)
        all_articles = (
            tag.articles.language()
            .filter(status="published")
            .order_by("-published_at", "-created_at")
        )
    else:
        tag = None
        all_articles = (
            Article.objects.language()
            .filter(status="published")
            .order_by("-published_at", "-created_at")
        )

    paginator = Paginator(all_articles, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "app_content/home.html",
        {
            "categories": categories,
            "tags": tags,
            "recent_articles": page_obj,
            "current_tag": tag,
        },
    )


def articles_by_category(request, slug):
    category = get_object_or_404(Category, translations__slug=slug)
    articles = (
        Article.objects.filter(category=category)
        .order_by("-published_at", "-created_at")
        .distinct()
    )

    return render(
        request,
        "app_content/articles_by_category.html",
        {
            "category": category,
            "articles": articles,
        },
    )


def articles_by_tag(request, slug):
    tag = get_object_or_404(Tag, translations__slug=slug)
    articles = (
        Article.objects.filter(tags=tag)
        .order_by("-published_at", "-created_at")
        .distinct()
    )

    return render(
        request,
        "app_content/articles_by_tag.html",
        {
            "current_tag": tag,
            "articles": articles,
        },
    )


def article_detail_view(request, slug):
    article = get_object_or_404(Article, translations__slug=slug)

    # Список просмотренных статей в сессии
    viewed = request.session.get("viewed_articles", [])

    if article.id not in viewed:
        article.views_count = (article.views_count or 0) + 1
        article.save(update_fields=["views_count"])
        viewed.append(article.id)
        request.session["viewed_articles"] = viewed  # обновляем сессию

    return render(
        request,
        "app_content/article_detail.html",
        {
            "article": article,
        },
    )
