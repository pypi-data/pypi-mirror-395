import context

from a2a_agentspeak import build_server, actions


def do_explode():
    print("TEST OK")
    return 0


my_special_action = actions.Action(
    "function",
    ".special",
    (),
    do_explode,
)

if __name__ == "__main__":

    host = "127.0.0.1"
    port = 9999
    name = "../../sample_agents/robots/open_robot"

    build_server.build_and_run(name, host, port, [my_special_action])
