import os
import sys

from a2a_acl.utils.url import build_url

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

host = "127.0.0.1"
repository_url = build_url(host, 9970)
client_port = 9998
client_url = build_url(host, client_port)
free_port = 9999

path_to_sample_agents = "../../sample_agents/"
