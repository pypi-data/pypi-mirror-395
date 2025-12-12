import context

from a2a_agentspeak.build_server import build_and_run

if __name__ == "__main__":

    host = "127.0.0.1"
    port = 9999

    name = "../../sample_agents/robots/robot"

    build_and_run(name, host, port)
    print("First agent running.")

    print("Going to run a second server on the same address (should report a failure).")
    if build_and_run(name, host, port):
        print("TEST KO")
    else:
        print("TEST OK")
