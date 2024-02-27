import os

from annotated_types import Ge, Le
from fastapi import APIRouter, status, HTTPException, Response
from icecream import ic
from typing import Annotated

from src.api.schemas.messages import Message, MessageIn, MessageAllOut
from src.api.schemas.channels import Channel, ChannelAllUnreadOut
from src.api.schemas.image import Image
from src.msg_service import MSGService

router = APIRouter(tags=["Messages"])


msg_service = MSGService()


@router.post("/messages", response_model=Message, status_code=status.HTTP_202_ACCEPTED)
def create_message(msg: MessageIn):
    msg_service.add_message(msg.channel, msg.author, msg.content)
    return Message(
        author=msg.author,
        content=msg.content,
    )


@router.get(
    "/messages/{channel_id}",
    responses={
        status.HTTP_200_OK: {"model": MessageAllOut},
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
)
def get_messages(
    channel_id: str, offset: Annotated[int, Ge(0)], limit: Annotated[int, Ge(1), Le(50)]
):
    msgs = msg_service.get_channel_messages(channel_id)

    if msgs is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    out = MessageAllOut(messages=[])
    for i in range(offset, offset + limit):
        try:
            out.messages.append(Message(author=msgs[i][0], content=msgs[i][1]))
        except IndexError as e:
            ic(e)
            break

    return out


@router.get(
    "/messages/unread",
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_200_OK: {"model": ChannelAllUnreadOut},
    },
)
def get_unread():
    if msg_service.notify_admin_unread():
        res = ChannelAllUnreadOut(count=0, channels=[])

        for channel_id, unread in msg_service.unread.items():
            if unread:
                res.count += 1
                res.channels.append(Channel(id=channel_id))
        return res

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/messages/image/generate",
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_200_OK: {"model": Image},
    },
)
def generate_image():
    ic(os.getcwd())
    if image_path := msg_service.generate_most_common_words():
        return Image(path="/static/png/" + image_path)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
