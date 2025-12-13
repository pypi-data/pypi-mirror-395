import context

from a2a.types import (
    AgentCard,
)

from a2a_acl.protocol.send_acl_message import spawn_send_acl_message
from a2a_acl.a2a_utils.card_holder import download_card
from a2a_acl.utils.strings import neutralize_str
from a2a_acl.utils.url import build_url

from a2a_agentspeak.content_codecs.common import python_agentspeak_codec_id

host = "127.0.0.1"
port = context.port_client


async def main() -> None:

    sender_agent_url = build_url(host, context.port_sender)
    receiver_agent_url = build_url(host, context.port_receiver)
    my_url = build_url(host, context.port_client)

    # query the a2a agent

    # Fetch Public Agent Card and Initialize Client
    final_agent_card_to_use: AgentCard | None = None
    try:
        final_agent_card_to_use = await download_card(sender_agent_url)
        print(str(final_agent_card_to_use))

    except Exception:
        print("Client failed to fetch the public agent card. Cannot continue.")
        exit(-1)

    # First message (achieve)
    spawn_send_acl_message(
        final_agent_card_to_use,
        "achieve",
        "do_ping(" + neutralize_str(receiver_agent_url) + ")",
        my_url,
        python_agentspeak_codec_id,
    )

    # Second message (achieve)
    spawn_send_acl_message(
        final_agent_card_to_use,
        "achieve",
        "share_secret(" + neutralize_str(receiver_agent_url) + ")",
        my_url,
        python_agentspeak_codec_id,
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
