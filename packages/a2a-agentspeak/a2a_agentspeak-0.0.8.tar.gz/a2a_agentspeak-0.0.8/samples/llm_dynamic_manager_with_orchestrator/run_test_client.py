

from a2a.types import (
    AgentCard,
)
from a2a.utils import new_agent_text_message


from a2a.server.events import EventQueue


from a2a_acl.agent.acl_agent import ACLAgentExecutor
from a2a_acl.agent.server_utils import run_server
from a2a_acl.protocol.acl_message import ACLMessage
from a2a_acl.interface.interface import (
    SkillRequest,
    DeclarativeForce,
    ACLAgentCard,
    SkillDeclaration,
)
from a2a_acl.interface.card_conversion import bdi_card_from_a2a_card
from a2a_acl.protocol.send_acl_message import send_acl_message
from a2a_acl.a2a_utils.card_holder import download_card

from a2a_agentspeak.content_codecs import python_agentspeak_codec
from a2a_agentspeak.content_codecs.common import python_agentspeak_codec_id
from hot_repository.repository import HotRepository

from mistral_selector_prompt import ask_llm_for_agent_selection
from samples.llm_dynamic_manager_with_orchestrator.context import (
    solution_agent_urls,
    spec1,
    orchestrator_agent_url,
)

from a2a_acl.utils.strings import neutralize_str
from a2a_acl.utils.url import build_url

host = "127.0.0.1"
my_port = 9999
my_url = build_url(host, my_port)


def has_skill(card: AgentCard, r: SkillRequest) -> bool:
    c = bdi_card_from_a2a_card(card)
    return c.has_declared_skill(r)


skill1 = SkillRequest(DeclarativeForce("input"), "spec", 1)
skill2 = SkillRequest(DeclarativeForce("action"), "build", 0)

my_skill = SkillDeclaration(DeclarativeForce("input"), "result", 1, "Receive a result.")
my_card = ACLAgentCard(
    "Client Agent", "A client agent", [my_skill], [python_agentspeak_codec_id]
)


def is_requirement_manager(card: AgentCard) -> bool:
    return has_skill(card, skill1) and has_skill(card, skill2)


class ClientAgentExecutor(ACLAgentExecutor):

    def __init__(self, my_url, orchestrator_agent: AgentCard):
        super().__init__(my_card, my_url)
        self.orchestrator_agent: AgentCard = orchestrator_agent
        self.current_selected_agent = None
        self.codec_objects["python_agentspeak_codec"] = (
            python_agentspeak_codec.codec_object
        )

    async def report_failure_to_orchestrator(self):
        await send_acl_message(
            self.orchestrator_agent,
            "tell",
            "failed(" + neutralize_str(self.current_selected_agent.url) + ")",
            my_url,
            python_agentspeak_codec_id,
        )

    async def execute_tell(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ) -> None:
        await output_event_queue.enqueue_event(
            new_agent_text_message("MESSAGE RECEIVED")
        )
        if m.content.startswith("failure"):  # fixme : not in interface
            print("The agent reported a failure.")
            await self.report_failure_to_orchestrator()
        else:
            print("The agent answered this: " + str(m))


async def main() -> None:
    repository = HotRepository()

    for u in solution_agent_urls:
        await repository.register(u)

    # filter agents that can manage requirements
    candidates: list[AgentCard] = repository.get_cards_by_skills([skill1, skill2])

    # Feed an orchestrator agent.
    orchestrator_agent_card = await download_card(orchestrator_agent_url)

    candidate_urls = [c.url for c in candidates]
    for u in candidate_urls:
        info = "register(" + neutralize_str(u) + ")"
        await send_acl_message(
            orchestrator_agent_card, "achieve", info, my_url, python_agentspeak_codec_id
        )

    # Start an a2a server.
    the_client_agent_executor = ClientAgentExecutor(my_url, orchestrator_agent_card)
    run_server(the_client_agent_executor, host, my_port)

    # Select the convenient agent
    if candidate_urls is []:
        raise Exception("No agent successfully contacted.")

    try:
        i = ask_llm_for_agent_selection(
            "Build a list of requirement from a specification.", candidates
        )
        if i < 0 or i >= len(candidates):
            raise Exception("Irregular answer from LLM.")
        selected_agent_card = candidates[i]
    except Exception:
        print("LLM selection failed, switching to default selection.")
        if candidates == []:
            raise Exception("No convenient agent found")
        else:
            selected_agent_card = candidates[0]

    print("Selected : " + selected_agent_card.name)
    the_client_agent_executor.current_selected_agent = selected_agent_card

    # Inform the orchestrator of the selection
    info = "selected(" + neutralize_str(selected_agent_card.url) + ")"
    await send_acl_message(
        orchestrator_agent_card, "tell", info, my_url, python_agentspeak_codec_id
    )

    info2 = "spec(" + neutralize_str(spec1) + ")"
    await send_acl_message(
        orchestrator_agent_card, "tell", info2, my_url, python_agentspeak_codec_id
    )

    await send_acl_message(
        orchestrator_agent_card, "achieve", "build", my_url, python_agentspeak_codec_id
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
