from rest_framework import serializers
from .models import Source, Headline

class HeadlineSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source='source.source_name', read_only=True)

    class Meta:
        model = Headline
        fields = ['source', 'title', 'link']

class SourceSerializer(serializers.ModelSerializer):
    news = HeadlineSerializer(many=True, read_only=True)

    class Meta:
        model = Source
        fields = ['source_name', 'source_link', 'source_category', 'updated_datetime', 'news']