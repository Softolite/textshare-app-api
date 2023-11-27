"""
Serializers for content APIs
"""
from rest_framework import serializers

from core.models import Content


class ContentSerializer(serializers.ModelSerializer):
    """Serializer for contents."""

    class Meta:
        model = Content
        fields = ['id', 'title', 'link', 'pin',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContentDetailSerializer(ContentSerializer):
    """Serializer for content detail view."""

    class Meta(ContentSerializer.Meta):
        fields = ContentSerializer.Meta.fields + ['description']
