from a2a_agentspeak import build_server
from a2a_acl.protocol.send_acl_message import spawn_send_acl_message
from a2a_acl.utils.url import build_url

from a2a_agentspeak.content_codecs.common import python_agentspeak_codec_id

if __name__ == "__main__":

    host = "127.0.0.1"
    port = 9999
    name = "../../sample_agents/robots/robot"
    url = build_url(host, port)

    build_server.build_and_run(name, host, port, [])

    spawn_send_acl_message(url, "achieve", "do_jump", "", python_agentspeak_codec_id)
