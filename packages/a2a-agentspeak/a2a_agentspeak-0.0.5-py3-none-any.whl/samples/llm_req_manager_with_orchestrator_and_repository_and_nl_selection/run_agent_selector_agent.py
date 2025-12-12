import context

from a2a_agentspeak import build_server

if __name__ == "__main__":

    host = "127.0.0.1"
    port = 9980

    name = "agent_selector"
    build_server.build_and_run(name, host, port)
