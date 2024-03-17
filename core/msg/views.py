from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import ValidationError
from .services.msg_service import MSGService
from .serializers import (
    QuerySerializer,
    InMessageSerializer,
    MessageSerializer,
    ChannelSerializer,
)


@extend_schema_view(
    post_message=extend_schema(
        summary="Post new message to channel by it's id",
        request=InMessageSerializer,
        responses={
            status.HTTP_201_CREATED: None,
        },
        auth=False,
    ),
    get_messages=extend_schema(
        summary="Get channel messages list",
        parameters=[QuerySerializer],
        responses={
            status.HTTP_200_OK: MessageSerializer(many=True),
            status.HTTP_404_NOT_FOUND: None,
        },
        auth=False,
    ),
    get_unread=extend_schema(
        summary="Get unread channels ids",
        responses={
            status.HTTP_200_OK: ChannelSerializer(many=True),
            status.HTTP_204_NO_CONTENT: None,
        },
        auth=False,
    ),
)
class MessageViewSet(ViewSet):
    msg_service = MSGService()

    # def list(self, request):
    #     query_ser = QuerySerializer(data=request.query_params)
    #
    #     if not query_ser.is_valid():
    #         raise ValidationError(query_ser.errors)
    #     applications = self.app_service.get_applications(**query_ser.data)
    #     return Response(ApplicationDetailsSerializer(applications, many=True).data)

    @action(detail=False, methods=["POST"])
    def post_message(self, request):
        in_msg = InMessageSerializer(data=request.data)
        if not in_msg.is_valid():
            raise ValidationError(in_msg.errors)
        self.msg_service.add_message(**in_msg.data)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"])
    def get_messages(self, request):
        query_ser = QuerySerializer(data=request.query_params)
        if not query_ser.is_valid():
            raise ValidationError(query_ser.errors)
        msgs = self.msg_service.get_channel_messages(query_ser.data.get("channel_id"))
        if msgs is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(
            status=status.HTTP_200_OK,
            data=MessageSerializer(msgs, many=True).data,
        )

    @action(detail=False, methods=["GET"])
    def get_unread(self, _):
        unread_channels_ids = self.msg_service.notify_admin_unread()
        if unread_channels_ids is None:
            return Response(status=status.HTTP_204_NO_CONTENT)

        unread_channels = [{"id": channel_id} for channel_id in unread_channels_ids]
        return Response(
            status=status.HTTP_200_OK,
            data=ChannelSerializer(unread_channels, many=True).data,
        )
