from rest_framework import serializers
from app_content.models.article import Article
from app_content.models.tag import Tag
from app_content.models.category import Category
from users.models import User  # замените на вашу модель

from app_content.serializers.translation_utils import (
    TranslationAwareSerializerMixin,
    create_translated_getter,
)


class TagSerializer(TranslationAwareSerializerMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    get_name = create_translated_getter("name")
    get_slug = create_translated_getter("slug")

    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class CategorySerializer(TranslationAwareSerializerMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    get_name = create_translated_getter("name")
    get_slug = create_translated_getter("slug")

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "photo",
        ]


class ArticleListSerializer(
    TranslationAwareSerializerMixin, serializers.ModelSerializer
):
    title = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    author = AuthorSerializer()

    get_title = create_translated_getter("title")
    get_slug = create_translated_getter("slug")

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "summary",
            "slug",
            "cover_thumbnail",
            "author",
            "published_at",
            "views_count",
        ]


class ArticleDetailSerializer(
    TranslationAwareSerializerMixin, serializers.ModelSerializer
):
    title = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    author = AuthorSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer(many=True)

    get_title = create_translated_getter("title")
    get_slug = create_translated_getter("slug")
    get_summary = create_translated_getter("summary")
    get_content = create_translated_getter("content")

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "content",
            "cover_image",
            "cover_thumbnail",
            "published_at",
            "author",
            "tags",
            "category",
            "views_count",
        ]
