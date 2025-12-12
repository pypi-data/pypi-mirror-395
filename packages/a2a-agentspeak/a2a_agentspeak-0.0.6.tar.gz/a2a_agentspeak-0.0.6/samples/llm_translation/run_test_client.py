import context
from a2a.types import AgentCard

from a2a_acl.a2a_utils.send_message import build_basic_text_request, send_a2a_message
from a2a_acl.a2a_utils.card_holder import download_card

from a2a_acl.utils.url import build_url

request1 = "Please move dear robot."
request2 = "Your target is located at position 20."
request3 = "Please move by 3 cm."


async def main() -> None:
    print("A2A client with no A2A server.")
    host = context.host
    my_port = context.test_client_port

    other_agent_url = build_url(host, context.translator_agent_port)
    my_url = build_url(host, my_port)

    print("Getting A2A agent card of the translator agent.")
    final_agent_card_to_use: AgentCard | None = None
    try:
        final_agent_card_to_use = await download_card(other_agent_url)

    except Exception:
        print("Client failed to fetch the public agent card. Cannot continue.")
        exit(-1)

    print("Send three messages to the translator.")
    # First message
    await send_a2a_message(
        final_agent_card_to_use, build_basic_text_request(request1, my_url)
    )
    # Second message
    await send_a2a_message(
        final_agent_card_to_use, build_basic_text_request(request2, my_url)
    )
    # Third message
    await send_a2a_message(
        final_agent_card_to_use, build_basic_text_request(request3, my_url)
    )

    print("End.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
