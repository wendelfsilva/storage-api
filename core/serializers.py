from django.contrib.auth.models import User
from rest_framework import serializers

from core import models, validators


# Serializers define the API representation.


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'url',
            'username',
            'email'
        ]


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Document
        fields = [
            'id',
            'url',
            'path',
            'revision',
            'file',
            'file_name',
            'uploaded_at',
            'user',
        ]
        validators = [validators.PathAndFileExtensionValidator()]


class DocumentDownloadSerializer(serializers.Serializer):
    revision = serializers.IntegerField(required=False, default=None)
