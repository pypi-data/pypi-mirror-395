import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

from hot_repository_server import (
    RepositoryAgentExecutor,
    hot_repo_agent_card,
)
from a2a_acl.utils.url import build_url

host = "127.0.0.1"
my_port = 9970
my_url = build_url(host, my_port)

if __name__ == "__main__":

    executor = RepositoryAgentExecutor(my_url)

    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=hot_repo_agent_card(my_url),
        http_handler=request_handler,
    )
    uvicorn.run(server.build(), host=host, port=my_port)
