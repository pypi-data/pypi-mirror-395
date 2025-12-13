from a2a.types import (
    AgentCard,
)
from a2a.utils import new_agent_text_message

from a2a.server.events import EventQueue
from a2a_acl.agent.acl_agent import ACLAgentExecutor
from a2a_acl.agent.server_utils import run_server
from a2a_acl.protocol.acl_message import ACLMessage
from a2a_acl.protocol.send_acl_message import send_acl_message
from a2a_acl.a2a_utils.card_holder import download_card
from a2a_agentspeak.content_codecs.common import python_codec_id, atom_codec_id
from a2a_acl.interface.interface import SkillDeclaration, DeclarativeForce, ACLAgentCard
from a2a_acl.utils.url import build_url

my_skill = SkillDeclaration(
    DeclarativeForce.INPUT, "pong", 0, "Receive a pong answer to a ping request."
)

my_card = ACLAgentCard("Client Agent", "A client agent", [my_skill], [atom_codec_id])

my_host = "127.0.0.1"
my_port = 9999
my_url = build_url(my_host, my_port)
other_agent_url = build_url(my_host, 9998)


class ClientAgentExecutor(ACLAgentExecutor):
    def __init__(self, my_url):
        super().__init__(my_card, my_url)
        self.pong_received = 0

    async def execute_tell(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ) -> None:
        print("BDI message received.")
        if m.content == "pong":
            print("pong received")
            self.pong_received += 1
        else:
            print("Other message received")
        if self.pong_received == 2:
            print("TEST OK")
        elif self.pong_received > 2:
            print("TEST KO)")
        await output_event_queue.enqueue_event(new_agent_text_message("Tell received"))


async def main() -> None:

    # 1) start an a2a server
    run_server(ClientAgentExecutor(my_url), my_host, my_port)

    # 2) query the other a2a agent

    # Fetch Public Agent Card and Initialize Client
    target_agent_card: AgentCard | None = None
    try:
        target_agent_card = await download_card(other_agent_url)
        print("Card downloaded.")

    except Exception:
        print("Client failed to fetch the public agent card. Cannot continue.")
        exit(-1)

    # First message (achieve)
    await send_acl_message(
        target_agent_card, "achieve", "ping", my_url, python_codec_id
    )
    print("First message sent.")

    # Second message (achieve)
    """await send_acl_message(
        target_agent_card, "achieve", "ping", my_url, python_codec_id
    )"""


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
