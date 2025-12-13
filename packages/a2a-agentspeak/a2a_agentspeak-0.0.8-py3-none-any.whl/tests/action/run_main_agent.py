import context

import threading


from a2a_agentspeak.build_server import build_and_run
from a2a_agentspeak.actions import Action


if __name__ == "__main__":

    host = "127.0.0.1"
    port = 9999

    name = "receiver"

    def square(x):
        return x * x

    def start():
        build_and_run(
            name,
            host,
            port,
            specific_actions=[Action("function", ".square", (int,), square)],
        )

    threading.Thread(target=start).start()
