import context
from a2a_agentspeak import build_server
from sample_agents.requirement_generators import mistral_requirement_actions

if __name__ == "__main__":

    host = "127.0.0.1"
    port = 9991
    name = "../../sample_agents/requirement_generators/llm_based_requirement_manager"

    build_server.build_and_run(
        name,
        host,
        port,
        [
            mistral_requirement_actions.action_prompt_completeness,
            mistral_requirement_actions.action_prompt_generate,
        ],
    )
