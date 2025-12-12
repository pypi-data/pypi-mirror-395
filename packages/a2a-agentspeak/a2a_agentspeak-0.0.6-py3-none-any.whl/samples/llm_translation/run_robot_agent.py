import context

from a2a_agentspeak import build_server

if __name__ == "__main__":

    port = context.acl_agent_port
    host = context.host
    name = "../../sample_agents/robots/robot"

    build_server.build_and_run(name, host, port)
