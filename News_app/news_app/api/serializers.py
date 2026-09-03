from rest_framework import serializers
from accounts.models import Article, ReaderProfile


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class subscribeArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReaderProfile
        fields = '__all__'