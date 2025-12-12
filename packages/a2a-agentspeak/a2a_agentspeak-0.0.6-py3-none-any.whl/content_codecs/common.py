from abc import ABC, abstractmethod


class BadFormat(Exception):
    pass


class UnknownCodec(Exception):
    pass


class NotPublic(Exception):
    pass


class Codec(ABC):

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def extract_entry_point(self, s: str):
        pass

    @abstractmethod
    def decode(self, s: str):
        pass


python_agentspeak_codec_id = "python_agentspeak_codec"
python_codec_id = "python_codec"
cold_repository_up_codec_id = "cold_repository_up_codec"
cold_repository_down_codec_id = "cold_repository_down_codec"
hot_repository_down_codec_id = "hot_repository_down_codec"
hot_repository_up_codec_id = "hot_repository_up_codec"
atom_codec_id = "atom_codec"
