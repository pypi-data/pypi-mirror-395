import context

import argparse

from a2a_agentspeak import build_server

if __name__ == "__main__":

    host = "127.0.0.1"

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('port')
    args = parser.parse_args()

    build_server.build_and_run(args.filename, host, int(args.port))
