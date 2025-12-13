This example needs a running repository server :

   ```bash
   python3 ../../hot_repository/run_hot_repository_server.py
   ```

It relies on the selector agent :

```bash
python3 run_agent_selector_agent.py
```

Then you can run the agents you want among those ones :

```bash
python3 run_bad_requirement_manager_agent.py
```

```bash
python3 run_naive_requirement_manager_agent.py
```

```bash
python3 run_requirement_manager_agent_on_mistral.py
```

```bash
python3 run_requirement_manager_agent_on_openai.py
```

```bash
python3 run_robot_agent.py
```

```bash
python3 run_stub_requirement_manager_agent.py
```

And finally you run the process with the client :

```bash
python3 run_test_client.py
```

Fine tuning : you can change the sleep time in llm agents to relax or stress the rate limit of the LLM provider.