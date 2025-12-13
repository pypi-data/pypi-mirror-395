from a2a_acl.interface.interface import SkillRequest, DeclarativeForce
from a2a_acl.utils.strings import neutralize_str, clear


def encode_url(url: str) -> str:
    return "selected(" + neutralize_str(url) + ")"


# FIXME : use a grammar parser


def decode_tell(s: str):
    (f, a) = s.split("(", 1)
    a2 = a.removesuffix(")")
    t = a2.split(",")
    return (f, t)


def decode_mandatory_skill(s: str):
    """Example : mandatory_skill(input, spec, 1)"""
    assert s.startswith("mandatory_skill(")
    s2 = s.removeprefix("mandatory_skill(").removesuffix(")")
    (a, b, c) = s2.split(",")
    return (a, b.removeprefix(" "), c.removeprefix(" "))


def decode_list(s: str):
    """example : [mandatory_skill(input, spec, 1)|[mandatory_skill(action, build, 0)|[]]]"""
    l = s.split("|")
    l2 = [e.removeprefix("[") for e in l]
    l3 = l2[0:-1]

    return [decode_mandatory_skill(m) for m in l3]


def decode_ask(s: str):
    (f, a) = s.split("(", 1)
    a2 = a.removesuffix(")")
    if f == "by_skills" or f == "cold_by_skills":
        l = decode_list(a2)
        return (f, (l,))
    elif f == "by_skills_and_spec":
        (d, a3) = a2.split(",", 1)  # NL description must have no comma.
        l = decode_list(a3.removeprefix(" "))
        return (f, (clear(d), l))
    else:
        raise NotImplementedError


def build_skill_request(i: str, f: str, a: str) -> SkillRequest:
    return SkillRequest(DeclarativeForce(i), f, int(a))
