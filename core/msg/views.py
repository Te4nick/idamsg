from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.viewsets import ViewSet
from .services import MSGService, ImageService, OperationsService
from .serializers import (
    GetChannelMessagesQuerySerializer,
    InMessageSerializer,
    MessageSerializer,
    ChannelSerializer,
    OperationSerializer,
    GetOperationQuerySerializer,
)
from uuid import UUID


@extend_schema_view(
    post_message=extend_schema(
        summary="Post new message to channel by it's id",
        request=InMessageSerializer,
        responses={
            status.HTTP_201_CREATED: InMessageSerializer,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ReturnDict,
        },
        auth=False,
    ),
    get_messages=extend_schema(
        summary="Get channel messages list",
        parameters=[GetChannelMessagesQuerySerializer],
        responses={
            status.HTTP_200_OK: MessageSerializer(many=True),
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ReturnDict,
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
    generate_image=extend_schema(
        summary="Generate image and get operation details",
        responses={
            status.HTTP_200_OK: OperationSerializer,
        },
        auth=False,
    ),
    get_image_status=extend_schema(
        summary="Get image generation status",
        parameters=[GetOperationQuerySerializer],
        responses={
            status.HTTP_200_OK: OperationSerializer,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ReturnDict,
        },
        auth=False,
    ),
)
class MessageViewSet(ViewSet):
    msg_service = MSGService()
    image_service = ImageService()
    ops_service = OperationsService()

    @action(detail=False, methods=["POST"])
    def post_message(self, request):
        in_msg = InMessageSerializer(data=request.data)
        if not in_msg.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=in_msg.errors,
            )

        self.msg_service.add_message(**in_msg.data)
        self.image_service.put_string(in_msg.data.get("content"))
        return Response(
            status=status.HTTP_201_CREATED,
            data=InMessageSerializer(in_msg.data).data,
        )

    @action(detail=False, methods=["GET"])
    def get_messages(self, request):
        query_ser = GetChannelMessagesQuerySerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=query_ser.errors,
            )

        msgs = self.msg_service.get_channel_messages(query_ser.data.get("channel_id"))
        if msgs is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )

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

    @action(detail=False, methods=["GET"])
    def generate_image(self, _):
        op_id = self.ops_service.execute_operation(self.image_service.generate_image)
        op = self.ops_service.get_operation(op_id)
        return Response(
            status=status.HTTP_200_OK,
            data=OperationSerializer(op).data,
        )

    @action(detail=False, methods=["GET"])
    def get_image_status(self, request):
        query_ser = GetOperationQuerySerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=query_ser.errors,
            )

        op = self.ops_service.get_operation(UUID(query_ser.data.get("id")))
        if op is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            status=status.HTTP_200_OK,
            data=OperationSerializer(
                {
                    "id": op.id,
                    "done": op.done,
                    "result": {
                        "path": op.result[1:],
                    },
                }
            ).data,
        )
