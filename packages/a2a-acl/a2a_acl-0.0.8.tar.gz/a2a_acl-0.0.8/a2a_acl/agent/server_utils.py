import threading

import uvicorn
from a2a.server.agent_execution import AgentExecutor
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard

from a2a_acl.agent.acl_agent import ACLAgentExecutor
from a2a_acl.interface.card_conversion import a2a_card_from_bdi_card
from a2a_acl.utils.url import build_url


def run_a2a_server(
    card: AgentCard, agent_executor: AgentExecutor, host: str, port: int
):

    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor,
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=card,
        http_handler=request_handler,
    )

    def start():
        uvicorn.run(server.build(), host=host, port=port)

    threading.Thread(target=start).start()
    print("-running a2a-server for " + card.name + " agent-")


def run_server(agent_executor: ACLAgentExecutor, host: str, port: int):
    agent_card = a2a_card_from_bdi_card(agent_executor.card, build_url(host, port))
    run_a2a_server(agent_card, agent_executor, host, port)
