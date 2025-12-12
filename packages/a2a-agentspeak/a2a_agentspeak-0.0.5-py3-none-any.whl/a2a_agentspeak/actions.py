from dataclasses import dataclass
from typing import Callable


@dataclass
class Action:
    """Datatype for actions than can be added to AgentSpeak agents."""

    kind: str
    action_name: str
    arity: tuple
    implementation: Callable


def check_action_for_hole(hole, action):
    (hole_name, hole_arity) = hole
    return hole_name == action.action_name and hole_arity == len(action.arity)
