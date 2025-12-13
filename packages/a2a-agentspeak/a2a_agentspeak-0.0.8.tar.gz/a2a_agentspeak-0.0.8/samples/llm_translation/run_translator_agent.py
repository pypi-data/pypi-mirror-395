import context
from a2a_acl.agent.server_utils import run_a2a_server
from a2a_acl.a2a_utils.card_holder import download_card
from sample_agents.python_agents.translator.translator_agent import build_card, A2AtoACLAgentExecutor
from a2a_acl.utils.url import build_url

the_host = context.host
acl_agent_port = 9999
my_port = context.translator_agent_port
my_url = build_url(the_host, my_port)


async def main() -> None:
    target_agent_url = build_url(the_host, acl_agent_port)
    try:

        c = await download_card(target_agent_url)
    except Exception:
        print(
            "Failed to download target agent card at "
            + target_agent_url
            + ". Cannot continue."
        )
        exit(-1)

    run_a2a_server(build_card(my_url), A2AtoACLAgentExecutor(c), the_host, my_port)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
    input("Press Enter to exit...\n")
