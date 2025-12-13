
This test is the counterpart of the half_ping test, but with a pure Java A2A agent instead of an AgentSpeak A2A agent.

To launch this test, you must first run the Pingable Java agent, then run the test client :
```bash
cd pingable
mvn quarkus:dev
```

```bash
python3 run_test_client.py
```

Note that the HTTP client used in the Pingable agent to send pong message must use HTTP 1.1 to talk with the uvicorn server run in the test python agent (default Client builder in a2a-java use HTTP 2).

