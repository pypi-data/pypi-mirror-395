import context

from a2a_agentspeak import build_server

if __name__ == "__main__":

    host = "127.0.0.1"
    port = 9993

    name = "../../sample_agents/requirement_generators/bad_requirement_manager"

    build_server.build_and_run(name, host, port)
