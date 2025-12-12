from a2a_agentspeak.content_codecs import python_agentspeak_codec
from a2a_agentspeak.content_codecs.common import (
    cold_repository_up_codec_id,
    cold_repository_down_codec_id,
    Codec,
)
from cold_repository.codec import decode_cold_descr


class ColdRepositoryUpCodec(Codec):
    """Messages sent to a cold repository.
    Example : cold_by_skill(...)"""

    def __init__(self):
        super().__init__(cold_repository_up_codec_id)

    def extract_entry_point(self, s: str):
        if s.startswith("cold_by_skills("):
            return "cold_by_skills"
        else:
            print("Unrecognized entry point: " + s)
            raise NotImplementedError()

    def decode(self, s: str):
        if s.startswith("cold_by_skills("):
            return python_agentspeak_codec.codec_object.decode(
                s
            )  # fixme : remove dependency on python-agentspeak
        else:
            print("Unable to decode: " + s)
            raise NotImplementedError()


up_codec_object = ColdRepositoryUpCodec()


class ColdRepositoryDownCodec(Codec):
    """Messages sent by cold repository.
    Example: selected(cold(agent(...))"""

    def __init__(self):
        super().__init__(cold_repository_down_codec_id)

    def extract_entry_point(self, s: str):
        if s.startswith("selected("):
            return "selected"
        else:
            print("Unrecognized entry point: " + s)
            raise NotImplementedError()

    def decode(self, s: str):
        if s.startswith("selected(cold_agent("):
            s2 = s.removeprefix("selected(").removesuffix(")")
            return decode_cold_descr(s2)
        else:
            print("Unable to decode: " + s)
            raise NotImplementedError()


down_codec_object = ColdRepositoryDownCodec()
