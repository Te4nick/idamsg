from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.Serializer):
    author = serializers.CharField(required=True, max_length=50)
    content = serializers.CharField(required=True, max_length=200)

    def create(self, validated_data):
        return Message(
            author=validated_data["author"],
            content=validated_data["content"],
        )


class InMessageSerializer(MessageSerializer):
    channel_id = serializers.CharField(required=True, max_length=50)


class ChannelSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, max_length=50)


class QuerySerializer(serializers.Serializer):
    channel_id = serializers.CharField(required=True, max_length=50)
    limit = serializers.IntegerField(min_value=1, default=10, max_value=50)
    offset = serializers.IntegerField(min_value=0, default=0)
