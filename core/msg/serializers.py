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


class GetChannelMessagesQuerySerializer(serializers.Serializer):
    channel_id = serializers.CharField(required=True, max_length=50)
    limit = serializers.IntegerField(min_value=1, default=10, max_value=50)
    offset = serializers.IntegerField(min_value=0, default=0)


class OperationSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, min_length=36, max_length=36)
    done = serializers.BooleanField()
    result = serializers.DictField()


class GetOperationQuerySerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
