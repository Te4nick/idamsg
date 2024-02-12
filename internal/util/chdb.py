from internal.entity.channel import Channel


class ChannelDB:
    def __init__(self):
        self.__db: dict[str: Channel] = {}

    def add_chanel(self, ch_id: str, ch: Channel) -> bool:
        if ch_id in self.__db:
            return False
        self.__db[ch_id] = ch
        return True

    def get_channel(self, ch_id: str) -> Channel | None:
        """
        Returns Channel object or None if not found
        :param ch_id: channel id
        :return: Channel object or NONE if not found
        """
        if ch_id in self.__db:
            return self.__db[ch_id]
        return None
