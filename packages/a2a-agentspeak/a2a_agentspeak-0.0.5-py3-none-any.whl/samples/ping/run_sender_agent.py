import context

import threading

from a2a_agentspeak.build_server import build_and_run

host = "127.0.0.1"
port = context.port_sender

name = "sender"


if __name__ == "__main__":

    def start():
        build_and_run(name, host, port)

    threading.Thread(target=start).start()
