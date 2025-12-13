import agentspeak
import agentspeak.runtime
import agentspeak.ext_stdlib

from a2a.server.events import EventQueue
from a2a_acl import protocol
from agentspeak import Literal

import a2a_acl.protocol.acl_message


from a2a_agentspeak import a2a_stdlib
from a2a_agentspeak.asp_message import literal, trigger, goal_type

from a2a_acl.agent.acl_agent import ACLAgentExecutor
from a2a_acl.protocol.acl_message import Illocution, ACLMessage

from a2a_agentspeak.check import check_illoc
from a2a_acl.protocol.send_acl_message import (
    spawn_send_acl_message,
    extract_text_from_message,
    extract_text_from_task,
)
from a2a_agentspeak.send_message import (
    spawn_check_recipient_intf,
)
from a2a_agentspeak.content_codecs import python_agentspeak_codec, cold_repository_codec, hot_repository_codec

from a2a_agentspeak.content_codecs.common import (
    python_agentspeak_codec_id,
    UnknownCodec,
    cold_repository_down_codec_id,
    hot_repository_down_codec_id,
    atom_codec_id,
    python_codec_id,
)
from a2a_acl.interface.interface import ACLAgentCard
from a2a_agentspeak.actions import Action

from a2a_acl.a2a_utils.send_message import sync_reply



def fast_do_send(
    to_url: str,
    illoc: Illocution,
    content: agentspeak.Literal | str,
    my_url: str,
    codec: str,
    message_handler,
    task_handler,
):
    spawn_check_recipient_intf(to_url, illoc, content)

    spawn_send_acl_message(
        dest=to_url,
        illocution=str(illoc),
        content=str(content),
        sender=my_url,
        codec=codec,
        message_processor=message_handler,
        task_processor=task_handler,
    )


class EmbeddedASPAgent:

    def __init__(
        self,
        asl_file: str,
        url: str,
        lib: agentspeak.Actions,
        additional_actions: set[Action],
    ):
        self.my_url = url

        self.env = agentspeak.runtime.Environment()

        # add custom actions (must occur before loading the asl file)
        self.bdi_actions = lib
        self.add_custom_actions()
        for t in additional_actions:
            self.add_action(t)

        with open(asl_file) as source:
            self.asp_agent = self.env.build_agent(source, self.bdi_actions)

    def start(self):
        self.env.run_agent(self.asp_agent)

    # this method is called by __init__
    def add_custom_actions(self):
        actions = self.bdi_actions

        @actions.add_procedure(".send", (None, agentspeak.Literal, None))
        def _fast_send_to_url(
            u: agentspeak.Literal, illoc: agentspeak.Literal, term: agentspeak.Literal
        ):
            assert check_illoc(illoc)

            # Use the simplest codec among atom and agentspeak
            codec = atom_codec_id if len(term.args) == 0 else python_agentspeak_codec_id

            fast_do_send(
                str(u),
                protocol.acl_message.Illocution(str(illoc)),
                term,
                self.my_url,  # Remark : here self is a ACLAgent and not an agentspeak.agent. For this reason it is difficult to get that function out of the class.
                codec,
                lambda message: self.process_signal(
                    extract_text_from_message(message), None
                ),
                lambda task: self.process_signal(extract_text_from_task(task), None),
            )

        @actions.add_procedure(
            ".send_cb", (None, agentspeak.Literal, None, agentspeak.Literal)
        )
        def _fast_send_to_url_cb(
            u: agentspeak.Literal,
            illoc: agentspeak.Literal,
            term: agentspeak.Literal,
            cb: agentspeak.Literal,
        ):
            assert check_illoc(illoc)

            # Use the simplest codec among atom and agentspeak
            codec = atom_codec_id if len(term.args) == 0 else python_agentspeak_codec_id

            fast_do_send(
                str(u),
                a2a_acl.protocol.acl_message.Illocution(str(illoc)),
                term,
                self.my_url,
                # Remark : here self is a ACLAgent and not an agentspeak.agent. For this reason it is difficult to get that function out of the class.
                codec,
                lambda message: self.process_signal(
                    extract_text_from_message(message), cb.functor
                ),
                lambda task: self.process_signal(
                    extract_text_from_task(task), cb.functor
                ),
            )

        @actions.add_procedure(".send_int", (None, agentspeak.Literal, int))
        def _fast_send_int_to_url(
            u: agentspeak.Literal, illoc: agentspeak.Literal, term: int
        ):
            assert check_illoc(illoc)

            codec = python_codec_id

            fast_do_send(
                str(u),
                protocol.acl_message.Illocution(str(illoc)),
                str(term),
                self.my_url,
                # Remark : here self is a ACLAgent and not an agentspeak.agent. For this reason it is difficult to get that function out of the class.
                codec,
                lambda message: self.process_signal(
                    extract_text_from_message(message), None
                ),
                lambda task: self.process_signal(extract_text_from_task(task), None),
            )

        @actions.add_procedure(
            ".send_int_cb", (None, agentspeak.Literal, int, agentspeak.Literal)
        )
        def _fast_send_int_to_url_cb(
            u: agentspeak.Literal,
            illoc: agentspeak.Literal,
            term: int,
            cb: agentspeak.Literal,
        ):
            assert check_illoc(illoc)

            codec = python_codec_id

            fast_do_send(
                str(u),
                protocol.acl_message.Illocution(str(illoc)),
                str(term),
                self.my_url,
                # Remark : here self is a ACLAgent and not an agentspeak.agent. For this reason it is difficult to get that function out of the class.
                codec,
                lambda message: self.process_signal(
                    extract_text_from_message(message), cb.functor
                ),
                lambda task: self.process_signal(
                    extract_text_from_task(task), cb.functor
                ),
            )

    def add_action(self, action: Action):
        if action.kind == "function":
            self.bdi_actions.add_function(
                action.action_name, action.arity, action.implementation
            )
        else:
            print("This kind of tool is not supported yet: " + action.kind)

    def process_tell_message(self, msg: ACLMessage):
        """Process tell requests following the AgentSpeak defined behavior."""
        assert msg.illocution == Illocution.TELL
        self.asp_agent.call(
            trigger(msg),
            agentspeak.GoalType.belief,
            literal(msg),
            agentspeak.runtime.Intention(),
        )
        self.env.run()

    def process_achieve_message(self, msg: ACLMessage):
        """Process achieve requests following the AgentSpeak defined behavior."""
        assert msg.illocution == Illocution.ACHIEVE
        self.asp_agent.call(
            trigger(msg),
            agentspeak.GoalType.achievement,
            literal(msg),
            agentspeak.runtime.Intention(),
        )
        self.env.run()

    def process_signal(self, txt: str, callback_functor: str | None):
        if callback_functor is None:
            print("(Received synchronous reply : " + txt + ")")
        else:
            try:
                lit = Literal(callback_functor, (txt,))
                self.asp_agent.call(
                    agentspeak.Trigger.addition,
                    agentspeak.GoalType.achievement,
                    lit,
                    agentspeak.runtime.Intention(),
                    delayed=True,
                )
                self.env.run()
            except agentspeak.AslError as e:
                print("Warning: " + callback_functor + " not handled (" + str(e) + ")")

    def process_cold_repo_tell_message(self, msg: ACLMessage):
        assert msg.illocution == "tell" and msg.content.startswith(
            "selected(cold_agent("
        )
        (name, holes) = cold_repository_codec.down_codec_object.decode(msg.content)
        if not holes == []:
            raise NotImplementedError()
        a = Literal("cold_agent", (name, ()))
        self.asp_agent.call(
            trigger(msg),
            goal_type(msg),
            Literal("selected", (a,)),
            agentspeak.runtime.Intention(),
        )
        self.env.run()

    def process_hot_repo_message(self, msg: ACLMessage):
        self.process_tell_message(msg)

    def extract_from_beliefs(self, a: str):
        r = self.asp_agent.beliefs[(a, 1)]  # fixme : arity
        assert isinstance(r, set)
        if r == set():
            return None
        else:
            tmp = next(iter(r))
            assert isinstance(tmp, agentspeak.Literal)
            assert tmp.functor == a
            assert isinstance(tmp.args, tuple)
            return tmp.args[0]

    def get_belief(self, s: str) -> str | None:
        r = self.extract_from_beliefs(s)
        if r is not None:
            return str(r)
        else:
            return None

    async def preprocess_tell_message(
        self, m: ACLMessage, output_event_queue: EventQueue
    ):

        print("(Received a message: " + str(m) + ")")

        if not (m.codec == python_agentspeak_codec_id or m.codec == atom_codec_id):
            print("Warning: unknown codec " + m.codec)

        if m.illocution == "tell":
            await sync_reply(output_event_queue, "Tell received.")
            self.process_tell_message(m)
        else:
            print("Cannot manage illocution " + m.illocution)

    async def preprocess_achieve_message(
        self, m: ACLMessage, output_event_queue: EventQueue
    ):

        print("(Received a message: " + str(m) + ")")

        if not (m.codec == python_agentspeak_codec_id or m.codec == atom_codec_id):
            print("Warning: unknown codec " + m.codec)

        if m.illocution == "achieve":
            await sync_reply(output_event_queue, "Achieve received")
            self.process_achieve_message(m)

        else:
            print("Cannot manage illocution " + m.illocution)

    async def preprocess_ask_message(
        self, m: ACLMessage, output_event_queue: EventQueue
    ):
        """Reply synchronously with the required information."""
        print("(Received a message: " + str(m) + ")")

        if not (m.codec == python_agentspeak_codec_id or m.codec == atom_codec_id):
            print("Warning: unknown codec " + m.codec)

        if (
            m.illocution == "ask"
        ):  # fixme : also check that the requested belief is public.
            """in A2A, each received message has an event queue to post responses.
            This is not the case in AgentSpeak.
            Here we add an illocution for requests that need an answer : ask"""
            result = self.get_belief(m.content)
            if result is not None:
                await sync_reply(output_event_queue, result)
            else:
                pass  # do not reply
        else:
            print("Cannot manage illocution " + m.illocution)

    async def preprocess_cold_repo_tell_message(
        self, m: ACLMessage, output_event_queue: EventQueue
    ):

        print("(Received a cold repository message: " + str(m) + ")")

        if not (m.codec == cold_repository_down_codec_id):
            print("Warning: unknown codec " + m.codec)

        if m.illocution == "tell":
            await sync_reply(output_event_queue, "Tell received.")
            self.process_cold_repo_tell_message(m)
        else:
            print("Cannot manage illocution " + m.illocution)

    async def preprocess_hot_repo_tell_message(
        self, m: ACLMessage, output_event_queue: EventQueue
    ):

        print("(Received a hot repository message: " + str(m) + ")")

        if not (m.codec == hot_repository_down_codec_id):
            print("Warning: unknown codec " + m.codec)

        if m.illocution == "tell":
            await sync_reply(output_event_queue, "Tell received.")
            self.process_hot_repo_message(m)
        else:
            print("Cannot manage illocution " + m.illocution)


class ASPAgentExecutor(ACLAgentExecutor):

    def __init__(
        self,
        asl_file: str,
        url: str,
        additional_actions,
        card: ACLAgentCard,
    ):
        super().__init__(card, url)
        self.acl_agent = EmbeddedASPAgent(
            asl_file,
            url,
            lib=agentspeak.Actions(a2a_stdlib.actions),
            additional_actions=additional_actions,
        )
        self.codec_objects["python_agentspeak_codec"] = (
            python_agentspeak_codec.codec_object
        )
        self.codec_objects["cold_repository_down_codec"] = (
            cold_repository_codec.down_codec_object
        )

        self.codec_objects["hot_repository_down_codec"] = (
            hot_repository_codec.codec_object
        )

    def start_behavior(self):
        self.acl_agent.start()

    def is_public(self, lit: str) -> bool:
        return lit in self.public_entry_points

    async def execute_tell(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ) -> None:
        # FIXME
        if m.codec == python_agentspeak_codec_id or m.codec == atom_codec_id:
            await self.acl_agent.preprocess_tell_message(m, output_event_queue)
        elif m.codec == cold_repository_down_codec_id:
            await self.acl_agent.preprocess_cold_repo_tell_message(
                m, output_event_queue
            )
        elif m.codec == hot_repository_down_codec_id:
            await self.acl_agent.preprocess_hot_repo_tell_message(m, output_event_queue)
        else:
            raise UnknownCodec

    async def execute_achieve(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ) -> None:
        # achieve messages are always in the python_agentspeak_codec (possible misuse however because other codecs are accepted)
        await self.acl_agent.preprocess_achieve_message(m, output_event_queue)

    async def execute_ask(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ) -> None:
        # ask messages are always in the python_agentspeak_codec (possible misuse however because other codecs are accepted)
        await self.acl_agent.preprocess_ask_message(m, output_event_queue)
