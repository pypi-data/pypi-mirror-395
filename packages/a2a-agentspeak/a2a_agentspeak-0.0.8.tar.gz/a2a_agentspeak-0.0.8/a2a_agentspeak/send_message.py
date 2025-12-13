import asyncio
from threading import Thread

import agentspeak
import httpx
from a2a.client import A2ACardResolver, A2AClientJSONError, A2AClientHTTPError
from a2a.types import AgentCard

from a2a_acl.interface.card_conversion import bdi_card_from_a2a_card
from a2a_acl.interface.interface import SkillRequest

from a2a_acl.interface.skill_conversion import decl_of_illoc
from a2a_acl.protocol.acl_message import Illocution


def has_declared_skill(
    illoc: Illocution, content: agentspeak.Literal, card: AgentCard
) -> bool:
    """To be used before sending a message."""
    r = SkillRequest(decl_of_illoc(illoc), content.functor, len(content.args))
    c = bdi_card_from_a2a_card(card)
    return c.has_declared_skill(r)


async def check_recipient_intf(
    to_url: str, illoc: Illocution, content: agentspeak.Literal
):
    async with httpx.AsyncClient() as httpx_client:

        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=to_url,
        )

        try:
            _public_card = await resolver.get_agent_card()
            if not has_declared_skill(illoc, content, _public_card):
                print(
                    "WARNING: the recipient of the message does not publish that skill: "
                    + illoc
                    + " "
                    + str(content.functor)
                    + "/"
                    + str(len(content.args))
                    + "."
                )
        except A2AClientJSONError as e:
            print("---FAIL---: ASL agent failed to send (JSON). " + str(e))
        except A2AClientHTTPError as e:
            print("---FAIL---: ASL agent failed to send (HTTP). " + str(e))
        except Exception as e:
            print("---FAIL---: ASL agent failed to send (other). " + str(e))


class CheckRecipientThread(Thread):
    def __init__(self, to_url: str, illoc: Illocution, content: agentspeak.Literal):
        super().__init__()
        self.to_url = to_url
        self.illoc = illoc
        self.content = content

        def run(self):
            loop = asyncio.new_event_loop()  # loop = asyncio.get_event_loop()
            loop.run_until_complete(
                check_recipient_intf(self.to_url, self.illocution, self.content)
            )
            loop.close()


def spawn_check_recipient_intf(
    to_url: str, illoc: Illocution, content: agentspeak.Literal
) -> None:
    t = CheckRecipientThread(to_url, illoc, content)
    t.start()
