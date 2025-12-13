import context



from a2a_acl.protocol.send_acl_message import spawn_send_acl_message
from a2a_acl.a2a_utils.card_holder import download_card
from a2a_agentspeak.content_codecs.common import python_agentspeak_codec_id

from a2a_acl.interface.interface import ACLAgentCard
from a2a_acl.utils.strings import neutralize_str
from a2a_acl.utils.url import build_url

host = "127.0.0.1"
port = context.port_client

my_card = ACLAgentCard("Client Agent", "A client agent", [], [])


async def main() -> None:

    sender_agent_url = build_url(host, context.port_sender)
    receiver_agent_url = build_url(host, context.port_receiver)
    my_url = build_url(host, context.port_client)

    try:
        agent_card_to_use = await download_card(sender_agent_url)
        spawn_send_acl_message(
            agent_card_to_use,
            "achieve",
            "do_ping(" + neutralize_str(receiver_agent_url) + ")",
            my_url,
            python_agentspeak_codec_id,
        )
    except Exception as e:
        print("Client failed to fetch the public agent card. Cannot continue.")
        exit(-1)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
