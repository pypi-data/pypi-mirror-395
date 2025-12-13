from a2a_acl.interface import asi_parser
from a2a_acl.interface.interface import ACLAgentCard, SkillRequest


class ColdRepository:
    """A repository of agents that can be instantiated."""

    store: dict[str, tuple[ACLAgentCard, frozenset]]

    def __init__(self, path: str):
        self.store = {}
        self.path = path

    def add(self, file_name: str, holes=()):
        print(
            "Adding "
            + file_name
            + " to the repository of cold agents (from "
            + self.path
            + ")"
        )
        c = asi_parser.read_file(self.path + file_name + ".asi")
        self.store[file_name] = (c, holes)

    def get_agents_by_skills(
        self, skills: list[SkillRequest]
    ) -> list[tuple[str, frozenset]]:
        print(
            "Received the request to filter cold agents with following skills: "
            + str(skills)
        )
        return [
            (n, h)
            for (n, (c, h)) in self.store.items()
            if c.has_declared_skills(skills)
        ]

    def print_state(self):
        print("Registered cold agents:")
        for a, (c, _) in self.store.items():
            n = c.name if c else "-"
            if n.endswith("\n"):
                n = n.removesuffix("\n")
            print(str(a) + " (" + n + ", with " + str(len(c.skills)) + " skill(s))")
        print("(end)")

    def degrade(self, agent):
        raise NotImplementedError()
