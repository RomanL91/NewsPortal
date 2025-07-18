from rest_framework import serializers

from app_content.models.tag import Tag
from app_content.models.article import Article
from app_content.models.category import Category

from app_content.services.category_content_factory import CategoryContentFactory

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


class CategorySerializer(TranslationAwareSerializerMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    get_name = create_translated_getter("name")
    get_slug = create_translated_getter("slug")

    class Meta:
        model = Category
        fields = ["id", "parent", "name", "slug"]


class CategoryDetailSerializer(CategorySerializer):
    articles = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ["articles", "tags"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        self._limit = int(request.query_params.get("limit", 20)) if request else 20
        self._offset = int(request.query_params.get("offset", 0)) if request else 0
        self._factory = None

    @property
    def factory(self) -> CategoryContentFactory:
        if self._factory is None:
            self._factory = CategoryContentFactory(self.instance, self.get_lang())
        return self._factory

    def get_articles(self, obj):
        articles = self.factory.get_articles()[
            self._offset : self._offset + self._limit
        ]
        return ArticleShortSerializer(articles, many=True, context=self.context).data

    def get_tags(self, obj):
        tags = self.factory.get_tags()
        serialized = TagSerializer(tags, many=True, context=self.context).data
        return list({tag["id"]: tag for tag in serialized}.values())
