import context

from a2a_agentspeak import build_server

from sample_agents.requirement_generators import openai_requirement_actions


if __name__ == "__main__":

    host = "127.0.0.1"
    port = 9992

    name = "../../sample_agents/requirement_generators/llm_based_requirement_manager"

    build_server.build_and_run(
        name,
        host,
        port,
        [
            openai_requirement_actions.action_prompt_completeness,
            openai_requirement_actions.action_prompt_generation,
        ],
    )

    # Below : to prevent the process to finish while some threads are running.
    input("Press RETURN to finish")
