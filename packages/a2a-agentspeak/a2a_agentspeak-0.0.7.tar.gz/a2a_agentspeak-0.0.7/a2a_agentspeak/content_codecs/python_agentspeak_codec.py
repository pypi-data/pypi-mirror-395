from a2a_agentspeak import asp_message
from a2a_agentspeak.content_codecs.common import Codec, python_agentspeak_codec_id


class PythonAgentspeakCodec(Codec):

    def __init__(self):
        super().__init__(python_agentspeak_codec_id)

    def extract_entry_point(self, s: str):
        return self.decode(s).functor

    def decode(self, s: str):
        return asp_message.lit_of_str(s)


codec_object = PythonAgentspeakCodec()
