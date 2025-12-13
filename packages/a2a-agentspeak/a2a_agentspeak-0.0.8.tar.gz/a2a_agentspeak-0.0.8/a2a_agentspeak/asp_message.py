import io

import agentspeak

from agentspeak import LinkedList
from agentspeak.lexer import TokenStream
from agentspeak.parser import AstLiteral
from agentspeak.runtime import BuildTermVisitor

from a2a_acl.protocol.acl_message import ACLMessage


def lit_of_str(s: str) -> agentspeak.Literal:
    """Use the python-agentspeak parser."""
    # see agentspeak/parser.py
    log = agentspeak.Log(agentspeak.get_logger(__name__), 3)
    fake_source_file = io.StringIO(s + " .")
    fake_source_file.name = "inline"
    tokens = TokenStream(fake_source_file, log, 1)
    tok = next(tokens)
    (_, lit) = agentspeak.parser.parse_literal(tok, tokens, log)
    assert isinstance(lit, AstLiteral)
    return lit.accept(BuildTermVisitor({}))


# deprecated
def parse_asp_linked_list(s: str):
    # FIXME : use a grammar instead to allow nested lists
    if s == "()":
        return ()  # empty Linked list implemented by empty tuple
    else:
        assert s.startswith("[") and s.endswith("]")
        inside = s.removeprefix("[").removesuffix("]")
        if inside == "":
            return ()
        else:
            (head, tail) = inside.split("|", 1)
            return LinkedList(lit_of_str(head), parse_asp_linked_list(tail))


def strplan(p: str):
    return agentspeak.Literal("plain_text", (p,))


def add_source(lit: agentspeak.Literal, s: str) -> agentspeak.Literal:
    return lit.with_annotation(agentspeak.Literal("source", (agentspeak.Literal(s),)))


def add_task_id(lit: agentspeak.Literal, s: str | None) -> agentspeak.Literal:
    if s is None:
        return lit
    else:
        return lit.with_annotation(
            agentspeak.Literal("task_id", (agentspeak.Literal(s),))
        )


def goal_type(m: ACLMessage) -> agentspeak.GoalType:
    _i = m.illocution
    if _i == "tell" or _i == "untell":
        return agentspeak.GoalType.belief
    elif _i == "achieve" or _i == "unachieve":
        return agentspeak.GoalType.achievement
    elif _i == "tellHow" or _i == "untellHow":
        return agentspeak.GoalType.tellHow
    else:
        raise RuntimeError("Illocution not supported: " + _i)


def trigger(m: ACLMessage) -> agentspeak.Trigger:
    _i = m.illocution
    if _i == "tell" or _i == "achieve" or _i == "tellHow":
        return agentspeak.Trigger.addition
    elif _i == "untell" or _i == "unachieve" or _i == "untellHow":
        return agentspeak.Trigger.removal
    else:
        raise RuntimeError("Illocution not supported: " + _i)


def literal(m: ACLMessage) -> agentspeak.Literal:
    _i = m.illocution
    _c = m.content
    _s = m.sender
    if _i in ["tell", "untell", "achieve", "unachieve", "ask"]:
        lit = lit_of_str(_c).freeze({}, {})

    elif _i in ["tellHow", "untellHow"]:
        lit = strplan(_c).freeze({}, {})
    else:
        raise RuntimeError("Illocution not supported: " + _i)
    return add_task_id(add_source(lit, _s), m.task_id)
