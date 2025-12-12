import os
import sys

from a2a_acl.utils.url import build_url

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

host = "127.0.0.1"
free_port = 9990

orchestrator_agent_url = build_url(host, 9980)

spec1 = "A function to compare two words."

repository_url = build_url(host, 9970)

path_to_sample_agents = "../../sample_agents/"
