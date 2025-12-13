import context

import threading

from a2a_agentspeak.build_server import build_and_run
from a2a_acl.utils.url import build_url

host = "127.0.0.1"
port = context.port_player
my_url = build_url(host, port)

name = "player_agent"


if __name__ == "__main__":

    def start():
        build_and_run(name, host, port, [])

    threading.Thread(target=start).start()

    input("Press ENTER to exit.")
