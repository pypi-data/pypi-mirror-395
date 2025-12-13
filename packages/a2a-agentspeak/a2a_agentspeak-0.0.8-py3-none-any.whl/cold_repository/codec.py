from a2a_acl.utils.strings import neutralize_str, clear


def encode_name(s: str) -> str:
    return "selected(" + neutralize_str(s) + ")"


def encode_cold_descr(name: str, holes) -> str:
    return "cold_agent(" + name + "," + str(holes) + ")"


# FIXME : use a grammar parser


def decode_hole_list(s: str) -> list:
    # fixme : temporary hypothesis : zero or one hole
    if s == "":
        return []
    else:
        s2 = s.removesuffix(",")
        s3 = s2.removeprefix("(").removesuffix(")")
        (a, b) = s3.split(",")
        return [(clear(a), int(b))]


def decode_cold_descr(s: str) -> tuple:
    """Example: cold_agent(robots/open_robot,(('.special', 0),))"""
    assert s.startswith("cold_agent(")
    s2 = s.removeprefix("cold_agent(").removesuffix(")")
    (n, h) = s2.split(",", 1)
    l = decode_hole_list(h.removeprefix("(").removesuffix(")"))
    return (n, l)
