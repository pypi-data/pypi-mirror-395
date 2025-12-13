from a2a.server.events import EventQueue


from a2a_acl.agent.acl_agent import ACLAgentExecutor

from a2a_agentspeak.content_codecs import python_agentspeak_codec, cold_repository_codec
from a2a_agentspeak.content_codecs.common import (
    cold_repository_up_codec_id,
    python_agentspeak_codec_id,
)
from a2a_acl.interface.card_conversion import a2a_card_from_bdi_card
from a2a_acl.interface.interface import (
    DeclarativeForce,
    SkillDeclaration,
    ACLAgentCard,
)
from a2a_acl.protocol.acl_message import ACLMessage

from a2a_acl.a2a_utils.send_message import sync_reply

from cold_repository.repository import ColdRepository
from cold_repository.codec import encode_cold_descr
from hot_repository.codec import decode_tell, decode_ask, build_skill_request

from a2a_acl.utils.strings import clear

import a2a_agentspeak.content_codecs.common

cold_repo_skills = [
    SkillDeclaration(DeclarativeForce.INPUT, "alive", 0, "Register as active"),
    SkillDeclaration(DeclarativeForce.INPUT, "alive", 1, "Register an agent as active"),
    SkillDeclaration(
        DeclarativeForce.BELIEF,
        "cold_by_skills",
        1,
        "Request a cold agent by a list of skills.",
    ),
    SkillDeclaration(
        DeclarativeForce.INPUT,
        "failure",
        1,
        "Report a failure from an agent.",
    ),
]

my_card = ACLAgentCard(
    "Cold ACL Agent Repository",
    "Cold ACL Agent Repository",
    cold_repo_skills,
    [cold_repository_up_codec_id, python_agentspeak_codec_id],
)


class RepositoryAgentExecutor(ACLAgentExecutor):
    cold_repo_for_asl_files: ColdRepository
    cold_repo_for_py_files: ColdRepository

    def __init__(self, my_url):
        super().__init__(my_card, my_url)
        print("Starting a fresh cold repository.")
        self.cold_repo_for_asl_files = ColdRepository("../sample_agents/")
        self.cold_repo_for_py_files = ColdRepository("../sample_agents/python_agents/")
        self.codec_objects[cold_repository_up_codec_id] = cold_repository_codec.up_codec_object
        self.codec_objects[python_agentspeak_codec_id] = python_agentspeak_codec.codec_object

    @staticmethod
    def register_cold(repo: ColdRepository, filename: str, holes=()):
        repo.add(filename, holes)

    def register_cold_asl(self, filename: str, holes=()):
        self.register_cold(self.cold_repo_for_asl_files, filename, holes)

    def register_cold_py(self, filename: str, holes=()):
        self.register_cold(self.cold_repo_for_py_files, filename, holes)

    async def reply_with_descr(self, res: str, holes, output_event_queue, to):
        s = encode_cold_descr(res, holes)

        # sync answer
        await sync_reply(output_event_queue, s)
        # async answer
        self.send_message(
            to,
            "tell",
            "selected(" + s + ")",
            a2a_agentspeak.content_codecs.common.cold_repository_down_codec_id,
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
        if f == "failure" and len(t) == 1:
            self.cold_repo_for_asl_files.degrade(clear(t[0]))
        else:
            print(
                "Only 'failure' allowed here (with 1 parameter). Received: "
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
            case "cold_by_skills":
                elements = t[0]
                r = [build_skill_request(i, f, a) for (i, f, a) in elements]
                tmp = self.cold_repo_for_asl_files.get_agents_by_skills(r)
                (res, holes) = tmp[0] if not tmp == [] else (None, None)
                if res:
                    await self.reply_with_descr(
                        res, holes, output_event_queue, m.sender
                    )
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
        self.cold_repo_for_asl_files.print_state()
        print("")


def cold_repo_agent_card(url):
    return a2a_card_from_bdi_card(
        my_card,
        url,
    )
