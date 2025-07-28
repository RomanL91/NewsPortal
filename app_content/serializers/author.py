from rest_framework import serializers
from django.conf import settings

from app_content.models.article import Article
from app_content.models.tag import Tag
from app_content.services.author_content_factory import AuthorContentFactory
from app_content.serializers.translation_utils import (
    TranslationAwareSerializerMixin,
    create_translated_getter,
)

from django.contrib.auth import get_user_model

User = get_user_model()


class TagSerializer(TranslationAwareSerializerMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    get_name = create_translated_getter("name")
    get_slug = create_translated_getter("slug")

    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class ArticleShortSerializer(
    TranslationAwareSerializerMixin, serializers.ModelSerializer
):
    title = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    get_title = create_translated_getter("title")
    get_slug = create_translated_getter("slug")

    class Meta:
        model = Article
        fields = ["id", "title", "slug", "cover_thumbnail", "published_at"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "photo",
        ]


class AuthorDetailSerializer(AuthorSerializer):
    articles = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta(AuthorSerializer.Meta):
        fields = AuthorSerializer.Meta.fields + ["articles", "tags"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        self._limit = int(request.query_params.get("limit", 10)) if request else 10
        self._offset = int(request.query_params.get("offset", 0)) if request else 0
        self._factory = None

    @property
    def factory(self):
        if self._factory is None:
            self._factory = AuthorContentFactory(self.instance, self.get_lang())
        return self._factory

    def get_lang(self):
        request = self.context.get("request")
        return getattr(request, "LANGUAGE_CODE", "ru")

    def get_articles(self, obj):
        page = self.factory.get_articles()[self._offset : self._offset + self._limit]
        return ArticleShortSerializer(page, many=True, context=self.context).data

    def get_tags(self, obj):
        tag_qs = self.factory.get_tags()
        serialized = TagSerializer(tag_qs, many=True, context=self.context).data
        return list({tag["id"]: tag for tag in serialized}.values())
