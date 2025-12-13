import context

from a2a.server.events import EventQueue
from a2a_acl.agent.acl_agent import ACLAgentExecutor

from a2a_agentspeak.content_codecs import python_agentspeak_codec, hot_repository_codec
from a2a_agentspeak.content_codecs.common import (
    python_agentspeak_codec_id,
    hot_repository_down_codec_id,
    hot_repository_up_codec_id,
)
from a2a_acl.interface.card_conversion import a2a_card_from_bdi_card
from a2a_acl.interface.interface import (
    DeclarativeForce,
    SkillDeclaration,
    ACLAgentCard,
)
from a2a_acl.protocol.acl_message import ACLMessage
from a2a_acl.a2a_utils.send_message import sync_reply
from hot_repository.codec import (
    encode_url,
    decode_tell,
    decode_ask,
    build_skill_request,
)
from hot_repository.repository import HotRepository
from hot_repository.mistral_selector_prompt import LLMFailureException
from a2a_acl.utils.strings import clear


hot_repo_skills = [
    SkillDeclaration(DeclarativeForce.INPUT, "alive", 0, "Register as active"),
    SkillDeclaration(DeclarativeForce.INPUT, "alive", 1, "Register an agent as active"),
    SkillDeclaration(
        DeclarativeForce.BELIEF,
        "by_skills",
        1,
        "Request an agent by a list of skills.",
    ),
    SkillDeclaration(
        DeclarativeForce.BELIEF,
        "by_skills_and_spec",
        2,
        "Request an agent by a list of skills.",
    ),
    SkillDeclaration(
        DeclarativeForce.INPUT,
        "failure",
        1,
        "Report a failure from an agent.",
    ),
]
hot_repo_card = ACLAgentCard(
    "Hot BDI Agent Repository",
    "Hot BDI Agent Repository",
    hot_repo_skills,
    [python_agentspeak_codec_id, hot_repository_up_codec_id],
)


class RepositoryAgentExecutor(ACLAgentExecutor):
    hot_repo: HotRepository

    def __init__(self, my_url):
        super().__init__(hot_repo_card, my_url)
        self.hot_repo = HotRepository()
        self.codec_objects[hot_repository_up_codec_id] = hot_repository_codec.codec_object
        self.codec_objects["python_agentspeak_codec"] = (
            python_agentspeak_codec.codec_object
        )

    async def reply_with_url(self, res: str, output_event_queue, to):
        # sync answer
        await sync_reply(output_event_queue, res)
        # async answer
        self.send_message(
            to,
            "tell",
            encode_url(res),
            hot_repository_down_codec_id,
        )
        print("Answer sent (synchronous & asynchrounous).")

    async def reply_with_failure(self, k, output_event_queue):
        await sync_reply(output_event_queue, "No convenient agent found for " + str(k))

    async def execute_tell(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ) -> None:

        (f, t) = decode_tell(m.content)
        arity = len(t)
        if f == "alive" and arity == 1:
            u = t[0]
            assert isinstance(u, str)
            await self.hot_repo.register(clear(u))
        elif f == "alive" and arity == 0:
            await self.hot_repo.register(m.sender)
        elif f == "failure" and arity == 1:
            self.hot_repo.degrade(clear(t[0]))
        else:
            print(
                "Only 'alive' or 'failure' allowed here (with 0 or 1 parameter). Received: "
                + str(m.content)
            )

        print("I received this request from: " + m.sender)
        await sync_reply(output_event_queue, "OK.")
        self.print_state()
        print("")

    async def execute_ask(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ) -> None:

        (k, t) = decode_ask(m.content)
        match k:
            case "by_skills":
                elements = t[0]
                r = [build_skill_request(i, f, a) for (i, f, a) in elements]
                tmp = self.hot_repo.get_top_card_by_skills(r)
                if tmp:
                    await self.reply_with_url(tmp.url, output_event_queue, m.sender)
                else:
                    await self.reply_with_failure(k, output_event_queue)
            case "by_skills_and_spec":
                # example: by_skills_and_spec("a requirement manager", [s1|[s2|()]])
                descr = t[0]
                lst = t[1]
                assert isinstance(descr, str)
                assert isinstance(lst, list)
                elements = lst
                r = [build_skill_request(a, b, c) for (a, b, c) in elements]
                try:
                    tmp = self.hot_repo.select_by_llm(descr, r)
                except LLMFailureException:
                    print(
                        "Warning: failed to get a selection from LLM, fall back on top reputation selection."
                    )
                    tmp = self.hot_repo.get_top_card_by_skills(r)
                if tmp:
                    await self.reply_with_url(tmp.url, output_event_queue, m.sender)
                else:
                    await self.reply_with_failure(k, output_event_queue)

            case _:
                print("Request could not be decoded: " + str(k))
                await self.reply_with_failure(k, output_event_queue)

        print("I received this request from: " + m.sender)
        await sync_reply(output_event_queue, "OK.")
        self.print_state()
        print("")

    def print_state(self):
        self.hot_repo.print_state()
        print("")


def hot_repo_agent_card(url):
    return a2a_card_from_bdi_card(
        hot_repo_card,
        url,
    )
