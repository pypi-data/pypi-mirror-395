import os
import sys

import config

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

sys.path.remove(os.getcwd())
port_player = 9997
