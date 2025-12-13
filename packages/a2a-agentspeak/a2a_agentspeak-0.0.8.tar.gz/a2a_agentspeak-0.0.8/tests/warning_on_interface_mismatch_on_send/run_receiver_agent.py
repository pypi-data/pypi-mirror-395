import context

import threading

from a2a_agentspeak import build_server


host = "127.0.0.1"
port = context.port_receiver

name = "receiver"


if __name__ == "__main__":

    def start():
        build_server.build_and_run(name, host, port)

    threading.Thread(target=start).start()
