import context
from agentspeak import LinkedList, Literal

from a2a.utils import new_agent_text_message


from a2a.server.events import EventQueue



from a2a_acl.agent.acl_agent import ACLAgentExecutor
from a2a_acl.agent.server_utils import run_server
from a2a_acl.protocol.acl_message import ACLMessage

from a2a_agentspeak.content_codecs import cold_repository_codec
from a2a_agentspeak.content_codecs.common import (
    cold_repository_up_codec_id,
    cold_repository_down_codec_id, python_agentspeak_codec_id,
)

from a2a_acl.interface.interface import SkillDeclaration, DeclarativeForce, ACLAgentCard
from a2a_agentspeak.build_server import build_and_run
from a2a_acl.protocol.send_acl_message import (
    send_acl_message,
    spawn_send_acl_message, extract_text_from_message, extract_text_from_task,
)

from a2a_agentspeak.actions import check_action_for_hole
from a2a_acl.a2a_utils.card_holder import download_card
from cold_repository.codec import decode_cold_descr
from a2a_acl.utils.url import build_url
from a2a_agentspeak import actions


def do_explode():
    print("TEST OK")
    return 0


my_special_action = actions.Action(
    "function",
    ".special",
    (),
    do_explode,
)

skill1 = SkillDeclaration(DeclarativeForce.INPUT, "pong", 0, "Receive a pong reply.")
skill2 = SkillDeclaration(
    DeclarativeForce.INPUT, "selected", 2, "Receive a cold agent."
)
skills = [skill1, skill2]


class ClientAgentExecutor(ACLAgentExecutor):

    def __init__(self, host, port):
        super().__init__(host,port)
        self.codec_objects[cold_repository_down_codec_id]= cold_repository_codec.down_codec_object

    async def execute_tell(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ) -> None:
        res = str(m)
        print("Incoming message: " + res)
        await output_event_queue.enqueue_event(
            new_agent_text_message("MESSAGE RECEIVED")
        )

my_url = context.client_url

def decode_and_spawn(res):
        (filename, holes) = decode_cold_descr(res)
        print("Actions to fill: " + str(holes))
        assert len(holes) == 1  # only 1 action to fill

        if check_action_for_hole(holes[0], my_special_action):
            build_and_run(
                context.path_to_sample_agents + filename,
                context.host,
                context.free_port,
                [my_special_action],
            )

            spawn_send_acl_message(
                build_url(context.host, context.free_port),
                "achieve",
                "do_special",
                my_url,
                python_agentspeak_codec_id,
            )
        else:
            print("TEST KO : mismatch between hole and action.")


async def main() -> None:

    # 1) start an a2a server to receive asynchronous answers

    my_card = ACLAgentCard(
        "Client Agent", "A client agent", skills, [cold_repository_down_codec_id]
    )
    run_server(ClientAgentExecutor(my_card, my_url), context.host, context.client_port)

    # 2) query the other a2a agent

    try:
        repository_card = await download_card(context.repository_url)
    except Exception:
        print("Repository not available. Cannot continue.")
        exit(1)

    test_skill = Literal(
        "mandatory_skill", (Literal("action"), Literal("do_special"), 0)
    )
    lst = LinkedList(test_skill, [])
    request = str(Literal("cold_by_skills", (lst,)))

    print("Sending a request to the repository.")
    await send_acl_message(
        repository_card, "ask", request, my_url, cold_repository_up_codec_id,
        lambda message: decode_and_spawn(extract_text_from_message(message)),
        lambda message: decode_and_spawn(extract_text_from_task(message))
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
