import httpx

from a2a.client import A2ACardResolver
from a2a.types import AgentCard
from a2a.utils import new_agent_text_message

from a2a.server.events import EventQueue

from a2a_acl.agent.acl_agent import ACLAgentExecutor
from a2a_acl.agent.server_utils import run_server
from a2a_acl.protocol.acl_message import ACLMessage
from a2a_acl.protocol.send_acl_message import send_acl_message

from a2a_acl.interface.interface import SkillDeclaration, DeclarativeForce, ACLAgentCard
from a2a_agentspeak.content_codecs.common import atom_codec_id
from a2a_acl.utils.url import build_url

my_skill = SkillDeclaration(
    DeclarativeForce.INPUT, "pong", 0, "Receive a pong answer to a ping request."
)
my_card = ACLAgentCard("Client Agent", "A client agent", [my_skill], [atom_codec_id])


class ClientAgentExecutor(ACLAgentExecutor):
    def __init__(self, url):
        super().__init__(my_card, url)
        self.pong_received = 0

    async def execute_tell(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ) -> None:
        if m.content == "pong":
            self.pong_received += 1
        if self.pong_received == 2:
            print("TEST OK")
        elif self.pong_received > 2:
            print("TEST KO)")
        await output_event_queue.enqueue_event(new_agent_text_message("Tell received"))


other_agent_url = "http://127.0.0.1:9999"
my_host = "127.0.0.1"
my_port = 9998
my_url = build_url(my_host, my_port)


async def main() -> None:

    # 1) start an a2a server
    run_server(ClientAgentExecutor(my_url), my_host, my_port)

    # 2) query the other a2a agent

    async with httpx.AsyncClient() as httpx_client:
        # Initialize A2ACardResolver
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=other_agent_url,
        )

        # Fetch Public Agent Card and Initialize Client
        final_agent_card_to_use: AgentCard | None = None
        try:
            _public_card = (
                await resolver.get_agent_card()
            )  # Fetches from default public path
            final_agent_card_to_use = _public_card

        except Exception as e:
            print("Client failed to fetch the public agent card. Cannot continue.")
            exit(-1)

    # First message (achieve)
    await send_acl_message(
        final_agent_card_to_use, "achieve", "ping", my_url, atom_codec_id
    )
    # Second message (achieve)
    await send_acl_message(
        final_agent_card_to_use, "achieve", "ping", my_url, atom_codec_id
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
