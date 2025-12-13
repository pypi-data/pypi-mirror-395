#!/bin/sh

python3 ../../hot_repository/run_hot_repository_server.py &
python3 run_agent_selector_agent.py &
python3 run_bad_requirement_manager_agent.py &
python3 run_naive_requirement_manager_agent.py &
#python3 run_requirement_manager_on_mistral.py &
#python3 run_requirement_manager_on_openai.py &
python3 run_robot_agent.py &
python3 run_stub_requirement_manager_agent.py &

sleep 3
python3 run_test_client.py