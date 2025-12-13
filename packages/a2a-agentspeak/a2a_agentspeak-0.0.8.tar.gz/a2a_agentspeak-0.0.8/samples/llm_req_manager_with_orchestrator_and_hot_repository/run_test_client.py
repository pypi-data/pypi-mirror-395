import time

import context


from a2a.types import AgentCard
from a2a.utils import new_agent_text_message

from a2a.server.events import EventQueue


from a2a_acl.agent.acl_agent import ACLAgentExecutor
from a2a_acl.agent.server_utils import run_server
from a2a_acl.protocol.acl_message import ACLMessage
from a2a_acl.protocol.send_acl_message import send_acl_message
from a2a_acl.a2a_utils.card_holder import download_card

from a2a_agentspeak.content_codecs import python_agentspeak_codec
from a2a_agentspeak.content_codecs.common import hot_repository_up_codec_id, python_agentspeak_codec_id

from a2a_acl.interface.interface import ACLAgentCard, SkillDeclaration, DeclarativeForce

from a2a_acl.utils.strings import neutralize_str
from a2a_acl.utils.url import build_url

host = "127.0.0.1"
my_port = 9999
my_url = build_url(host, my_port)

my_card = ACLAgentCard(
    "Client Agent",
    "A client agent",
    [SkillDeclaration(DeclarativeForce("input"), "result", 1, "Receive a result.")],
    [python_agentspeak_codec_id],
)


class ReferenceAgentExecutor(ACLAgentExecutor):

    def __init__(self, my_url, orchestrator_agent: AgentCard):
        super().__init__(agentcard=my_card, my_url=my_url)
        self.orchestrator_agent: AgentCard = orchestrator_agent
        self.codec_objects["python_agentspeak_codec"] = (
            python_agentspeak_codec.codec_object
        )

    async def execute_tell(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ) -> None:
        await output_event_queue.enqueue_event(
            new_agent_text_message("MESSAGE RECEIVED")
        )
        print("The agent answered this: " + str(m.content))


async def main() -> None:
    try:
        orchestrator_agent_card = await download_card(context.orchestrator_agent_url)
    except Exception:
        print("Orchestrator not available. Cannot continue.")
        exit(1)

    # Start an a2a server.
    run_server(ReferenceAgentExecutor(my_url, orchestrator_agent_card), host, my_port)

    # Register agents to the repository
    try:
        repository_card = await download_card(context.repository_url)
    except Exception:
        print("Repository not available. Cannot continue.")
        exit(1)

    for u in context.solution_agent_urls:
        print("Registering " + u)
        await send_acl_message(
            repository_card,
            "tell",
            "alive(" + neutralize_str(u) + ")",
            my_url,
            hot_repository_up_codec_id,
        )

    # Send specification and build request to the orchestrator.
    info_spec = "spec(" + neutralize_str(context.spec1) + ")"
    await send_acl_message(
        orchestrator_agent_card, "tell", info_spec, my_url, python_agentspeak_codec_id
    )

    time.sleep(0.5)  # to avoid that the build message arrives before the spec message

    await send_acl_message(
        orchestrator_agent_card, "achieve", "build", my_url, python_agentspeak_codec_id
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
