This example needs a running repository server :

   ```bash
   python3 ../../hot_repository/run_hot_repository_server.py
   ```

It relies on the selector agent :

```bash
python3 run_asp_agent.py agent_selector 9980
```

Then you can run the agents you want among those ones :

```bash
python3 run_asp_agent.py ../../sample_agents/requirement_generators/bad_requirement_manager 9993
```

```bash
python3 run_asp_agent.py ../../sample_agents/requirement_generators/naive_requirement_manager 9995
```

```bash
python3 run_requirement_manager_agent_on_mistral.py
```

```bash
python3 run_requirement_manager_agent_on_openai.py
```

```bash
python3 run_asp_agent.py ../../sample_agents/robots/robot 9990
```

```bash
python3 run_asp_agent.py ../../sample_agents/requirement_generators/stub_requirement_manager 9996
```

And finally you run the process with the client :

```bash
python3 run_test_client.py
```

Fine-tuning : you can change the sleep time in llm agents to relax or stress the rate limit of the LLM provider.