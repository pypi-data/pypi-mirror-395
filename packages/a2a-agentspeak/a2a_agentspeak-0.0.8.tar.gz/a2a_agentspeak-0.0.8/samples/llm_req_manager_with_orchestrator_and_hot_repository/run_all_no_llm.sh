#!/bin/sh

python3 ../../hot_repository/run_hot_repository_server.py &
python3 run_asp_agent.py agent_selector 9980 &
python3 run_asp_agent.py ../../sample_agents/requirement_generators/bad_requirement_manager 9993 &
python3 run_asp_agent.py ../../sample_agents/requirement_generators/naive_requirement_manager 9995 &
python3 run_asp_agent.py ../../sample_agents/robots/robot 9990 &
python3 run_asp_agent.py ../../sample_agents/requirement_generators/stub_requirement_manager 9996 &


sleep 3
python3 run_test_client.py