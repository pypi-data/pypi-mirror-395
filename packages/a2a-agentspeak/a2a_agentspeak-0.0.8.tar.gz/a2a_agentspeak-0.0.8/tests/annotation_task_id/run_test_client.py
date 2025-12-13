import time

from a2a.types import AgentCard
from a2a.utils import new_agent_text_message

from a2a.server.events import EventQueue

from a2a_acl.agent.acl_agent import ACLAgentExecutor
from a2a_acl.agent.server_utils import run_server
from a2a_acl.protocol.acl_message import ACLMessage
from a2a_acl.protocol.send_acl_message import send_acl_message
from a2a_acl.a2a_utils.card_holder import download_card

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
        print(str(m))
        if m.content == "pong":
            self.pong_received += 1
            print("New counter value: " + str(self.pong_received))
        await output_event_queue.enqueue_event(new_agent_text_message("Tell received"))

    def check(self) -> int:
        return self.pong_received


other_agent_url = "http://127.0.0.1:9999"
my_host = "127.0.0.1"
my_port = 9998
my_url = build_url(my_host, my_port)


async def main() -> None:

    # 1) start an a2a server
    a = ClientAgentExecutor(my_url)
    run_server(a, my_host, my_port)

    # 2) query the other a2a agent

    # Fetch Public Agent Card and Initialize Client
    final_agent_card_to_use: AgentCard | None = None
    try:
        final_agent_card_to_use = await download_card(other_agent_url)

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

    time.sleep(1)
    c = a.check()
    if c == 1:
        print("Test OK")
    else:
        print("Test KO : " + str(c))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
