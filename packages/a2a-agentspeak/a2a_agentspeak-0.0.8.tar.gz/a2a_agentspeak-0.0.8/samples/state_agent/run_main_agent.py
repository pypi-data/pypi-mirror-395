import threading

from a2a_agentspeak.build_server import build_and_run

if __name__ == "__main__":

    host = "127.0.0.1"
    port = 9999
    name = "state"

    def start():
        build_and_run(name, host, port)

    threading.Thread(target=start).start()
    print("-running a2a-server for " + name + " agent-")
