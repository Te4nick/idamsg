# from abc import ABC, abstractmethod
# from internal.entity.channel import Channel
#
#
# class RepositoryABC(ABC):
#     @abstractmethod
#     def add_chanel(self, ch_id: str, ch: ChannelDC) -> bool:
#         pass
#
#     @abstractmethod
#     def get_channel(self, ch_id: str) -> ChannelDC | None:
#         pass
#
#     @abstractmethod
#     def remove_channel(self, ch_id: str) -> bool:
#         pass
#
#     @abstractmethod
#     def get_all_channels(self) -> list[ChannelDC]:
#         pass
#
#     @abstractmethod
#     def add_message(self, ch_id: str, msg: str) -> bool:
#         pass
