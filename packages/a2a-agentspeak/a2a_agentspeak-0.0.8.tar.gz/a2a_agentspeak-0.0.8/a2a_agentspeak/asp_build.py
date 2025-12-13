from a2a.types import AgentCard


from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

from a2a_agentspeak.content_codecs.common import (
    python_agentspeak_codec_id,
    cold_repository_down_codec_id,
    hot_repository_down_codec_id,
    atom_codec_id,
)
from a2a_acl.interface import asi_parser
from a2a_acl.interface.card_conversion import a2a_card_from_bdi_card
from a2a_acl.interface.interface import (
    DeclarativeForce,
    SkillDeclaration,
    ACLAgentCard,
)
from a2a_agentspeak.embedded_agent import ASPAgentExecutor

import agentspeak

from a2a_agentspeak.check import check_achievement, check_input_belief, check_ask_belief
from a2a_acl.utils.result import Result
from a2a_acl.utils.url import build_url


class ASPAgentBuilder:
    skills: list[SkillDeclaration]

    def __init__(self, name, doc, implementation: str, additional_actions):
        self.skills = []
        self.name = name
        self.doc = doc
        self.implementation_file = implementation
        self.additional_actions = additional_actions
        self.codecs = [
            python_agentspeak_codec_id,
            cold_repository_down_codec_id,
            hot_repository_down_codec_id,
            atom_codec_id,
        ]

    def publish_ask(self, doc, functor, arity):
        self.skills.append(
            SkillDeclaration(
                doc=doc,
                functor=functor,
                arity=arity,
                declaration_kind=DeclarativeForce.BELIEF,
            )
        )

    def publish_listen(self, doc, functor, arity):
        self.skills.append(
            SkillDeclaration(
                doc=doc,
                functor=functor,
                arity=arity,
                declaration_kind=DeclarativeForce.INPUT,
            )
        )

    def publish_obey(self, doc, functor, arity):
        self.skills.append(
            SkillDeclaration(
                doc=doc,
                functor=functor,
                arity=arity,
                declaration_kind=DeclarativeForce.ACTION,
            )
        )

    def public_functors(self):
        return [s.functor for s in self.skills]

    def build_bdi_card(self):
        return ACLAgentCard(self.name, self.doc, self.skills, self.codecs)

    def build_a2a_card(self, url) -> AgentCard:
        return a2a_card_from_bdi_card(self.build_bdi_card(), url)

    def build_server(self, host:str, port:int) -> A2AStarletteApplication:
        url = build_url(host, port)
        self.executor = ASPAgentExecutor(
            self.implementation_file,
            url,
            additional_actions=self.additional_actions,
            card=self.build_bdi_card(),
        )

        request_handler = DefaultRequestHandler(
            agent_executor=self.executor,
            task_store=InMemoryTaskStore(),
        )
        app = A2AStarletteApplication(
            agent_card=self.build_a2a_card(url), http_handler=request_handler
        )
        return app

    def start_agent_behavior(self):
        self.executor.start_behavior()

    def check(self) -> Result:
        """Check that the public interface corresponds to actual triggers in implementation.
        More precisely:
         * achievements declared in the interface must have a trigger (we do not consider plans that would be added dynamically with askHow or tellHow).
         * belief literals which can be asked must occur in the implementation (we do not consider beliefs that are perceived during execution and which are not handled by the start implementation)
         * beliefs that are told to that agent must occur too in the start implementation.
        """
        LOGGER = agentspeak.get_logger(__name__)
        with open(self.implementation_file) as source:
            log = agentspeak.Log(LOGGER, 3)
            tokens = agentspeak.lexer.TokenStream(source, log)
            ast_agent: agentspeak.parser.ASTAgent = agentspeak.parser.parse(
                source.name, tokens, log
            )
            log.throw()

        # exists
        for s in self.skills:
            match s.declaration_kind:
                case DeclarativeForce.ACTION:
                    if not check_achievement(s.functor, ast_agent):
                        return Result(False, s.functor)
                case DeclarativeForce.BELIEF:
                    if not check_input_belief(s.functor, ast_agent):
                        return Result(False, s.functor)
                case DeclarativeForce.INPUT:
                    if not check_ask_belief(s.functor, ast_agent):
                        return Result(False, s.functor)
        return Result(True, None)


class InterfaceError(Exception):
    def __init__(self, token):
        self.token = token


def from_files_distinct(intf: str, impl: str, actions=()) -> ASPAgentBuilder:

    i: ACLAgentCard = asi_parser.read_file(intf)

    a: ASPAgentBuilder = ASPAgentBuilder(
        i.name, i.doc, impl, additional_actions=actions
    )

    for l in i.skills:
        match l.declaration_kind:
            case DeclarativeForce.BELIEF:
                a.publish_ask(doc=l.doc, functor=l.functor, arity=l.arity)
            case DeclarativeForce.INPUT:
                a.publish_listen(doc=l.doc, functor=l.functor, arity=l.arity)
            case DeclarativeForce.ACTION:
                a.publish_obey(doc=l.doc, functor=l.functor, arity=l.arity)
            case _:
                assert False

    r = a.check()
    if not r.success:
        raise InterfaceError(r.reason)
    else:
        return a


def from_files(name: str, actions=()) -> ASPAgentBuilder:
    return from_files_distinct(name + ".asi", name + ".asl", actions)
