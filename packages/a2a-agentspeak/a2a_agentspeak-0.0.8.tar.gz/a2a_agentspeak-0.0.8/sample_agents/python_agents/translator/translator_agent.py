import context

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.types import AgentCard

from a2a.server.events import EventQueue

import a2a_agentspeak.content_codecs.common

from a2a_acl.protocol.send_acl_message import send_acl_message

from a2a_acl.a2a_utils.send_message import sync_reply

from a2a_acl.interface.card_conversion import a2a_card_from_bdi_card
from a2a_acl.interface.interface import ACLAgentCard

from a2a_acl.utils.url import build_url

from sample_agents.python_agents.translator.translator_nl_to_bdi.translator import translate, LLMError

my_port = context.translator_agent_port
the_host = context.host
my_url = build_url(the_host, my_port)

acl_agent_port = context.acl_agent_port


class A2AtoACLAgentExecutor(AgentExecutor):

    def __init__(self, routing_to_card: AgentCard):
        self.routing_to_card = routing_to_card

    async def execute(self, ctx: RequestContext, event_queue: EventQueue) -> None:
        if ctx.configuration is None:
            sender = None
        elif ctx.configuration.push_notification_config is None:
            sender = None
        else:
            sender = ctx.configuration.push_notification_config.url
            # fixme : forward replies to sender.

        content = ctx.get_user_input()
        await sync_reply(event_queue, "Received.")

        try:
            (i, a) = translate(self.routing_to_card, content)
            await send_acl_message(
                self.routing_to_card,
                i,
                a,
                my_url,
                a2a_agentspeak.content_codecs.common.python_agentspeak_codec_id,
            )
        except LLMError:
            print("Failure while talking with the LLM.")

    async def cancel(self, ctx: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("Cancel not supported.")


def build_card(translator_url) -> AgentCard:
    return a2a_card_from_bdi_card(
        ACLAgentCard("translator", "A A2A -> ACL translator agent (with LLM)", [], []),
        translator_url,
    )
