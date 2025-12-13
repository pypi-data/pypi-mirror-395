import asyncio
import threading
import time

import uvicorn

from a2a_agentspeak import actions
from a2a_agentspeak.asp_build import from_files, ASPAgentBuilder
from a2a_acl.utils.url import build_url


def build_and_run(asp_filename: str, host:str, port:int, specific_actions=()):
    a: ASPAgentBuilder = from_files(
        asp_filename,
        actions=tuple(specific_actions)
        + (spawn_action,),  # forward reference / mutual recursion
    )

    # build and run the a2a server
    server = a.build_server(host, port)
    u_server = uvicorn.Server(uvicorn.Config(server.build(), host=host, port=port))

    def start():
        loop = asyncio.new_event_loop()  # loop = asyncio.get_event_loop()
        loop.run_until_complete(u_server.serve())
        loop.close()
        print("Shutdown.")

    threading.Thread(target=start).start()
    print("Running a2a-server for " + asp_filename + " agent.")
    time.sleep(0.5)
    if not u_server.started:
        return False
    else:
        print("Starting agent behavior.")
        # running the internal behavior after opening the server
        a.start_agent_behavior()
        return True


def do_spawn(fic: str, port=9990) -> str:
    host = "127.0.0.1"
    """A spawn that tries several ports until one available port is found (between 9990 and 9999)."""
    current_port = port
    success = False
    while current_port < 10000 and not success:
        success = build_and_run(fic, host, current_port)
        used_port = current_port
        current_port += 1
    if success:
        return build_url(host, used_port)
    else:
        raise Exception("Failed to spawn agent (no port available)")


spawn_action = actions.Action(
    "function",
    ".spawn",
    (str,),
    do_spawn,
)
