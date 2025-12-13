
import context

from a2a.types import (
    AgentCard,
)

from a2a.utils import new_agent_text_message

from a2a.server.events import EventQueue

from a2a_acl.agent.acl_agent import ACLAgentExecutor

from a2a_acl.protocol.acl_message import ACLMessage
from a2a_acl.protocol.send_acl_message import send_acl_message
from a2a_acl.a2a_utils.card_holder import download_card
from a2a_agentspeak.content_codecs.common import python_agentspeak_codec_id

from a2a_acl.interface.interface import ACLAgentCard

from a2a_acl.utils.url import build_url

host = "127.0.0.1"
port = context.port_client

my_card = ACLAgentCard(
    "Client Agent", "A client agent", [], [python_agentspeak_codec_id]
)

class ClientAgentExecutor(ACLAgentExecutor):

    def __init__(self):
        super().__init__(my_card)

    async def execute_bdi(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ) -> None:
        print("Incoming message: " + str(m))
        await output_event_queue.enqueue_event(
            new_agent_text_message("MESSAGE RECEIVED")
        )


async def main() -> None:

    target_agent_url = build_url(host, context.port_sender)
    my_url = build_url(host, context.port_client)

    # Fetch Public Agent Card and Initialize Client
    target_agent_card: AgentCard | None = None

    try:
        target_agent_card = await download_card(target_agent_url)

    except Exception:
        print("Client failed to fetch the public agent card. Cannot continue.")
        exit(-1)

    await send_acl_message(target_agent_card, "achieve", "do_ping", my_url, "atom")
    print("Message sent.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
