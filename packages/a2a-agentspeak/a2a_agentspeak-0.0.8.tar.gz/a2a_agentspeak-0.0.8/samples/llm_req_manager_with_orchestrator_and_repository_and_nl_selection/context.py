import os
import sys

from a2a_acl.utils.url import build_url

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

solution_agent_urls = [
    "http://127.0.0.1:9990/",  # robot
    "http://127.0.0.1:9992/",  # opeanai requirement manager
    "http://127.0.0.1:9993/",  # bad requirement manager
    "http://127.0.0.1:9991/",  # mistral requirement manager
    "http://127.0.0.1:9995/",  # naive requirement manager
    "http://127.0.0.1:9996/",  # stub requirement manager
]

orchestrator_agent_url = "http://127.0.0.1:9980/"

spec1 = "A function to compare two words."

repository_url = build_url("127.0.0.1", 9970)
