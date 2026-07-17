from __future__ import annotations

from rest_framework import serializers


class PublicIdentitySerializer(serializers.Serializer[dict[str, str]]):
    owner = serializers.CharField()
    api_version = serializers.CharField()
