from a2a.types import (
    AgentCard,
)
from a2a.utils import new_agent_text_message

from a2a.server.events import EventQueue

from a2a_acl.agent.acl_agent import ACLAgentExecutor
from a2a_acl.agent.server_utils import run_server
from a2a_acl.protocol.acl_message import ACLMessage
import a2a_acl.protocol.send_acl_message as send_acl_message
from a2a_acl.a2a_utils.card_holder import download_card
from a2a_acl.content_codecs.common import atom_codec_id
from a2a_acl.interface.interface import (
    SkillDeclaration,
    DeclarativeForce,
    ACLAgentCard,
)
from a2a_acl.utils.url import build_url

my_host = "127.0.0.1"
my_port = 9998
my_url = build_url(my_host, my_port)
other_agent_url = build_url(my_host, 9999)

my_skill = SkillDeclaration(
    DeclarativeForce.INPUT, "pong", 0, "Receive a pong answer to a ping request."
)

my_card = ACLAgentCard("Client Agent", "A client agent", [my_skill], [atom_codec_id])


class ClientAgentExecutor(ACLAgentExecutor):
    def __init__(self, url):
        super().__init__(my_card, url)
        self.pong_received = 0

    async def execute_tell(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ) -> None:

        await output_event_queue.enqueue_event(new_agent_text_message("Tell received"))


async def main() -> None:

    # 1) start an a2a server
    run_server(ClientAgentExecutor(my_url), my_host, my_port)

    # 2) query the other a2a agent

    # Fetch Public Agent Card and Initialize Client
    target_agent_card: AgentCard | None = None
    try:
        target_agent_card = await download_card(other_agent_url)

    except Exception:
        print("Client failed to fetch the public agent card. Cannot continue.")
        exit(-1)

    try:
        # Send a message not supported
        await send_acl_message.send_acl_message(
            target_agent_card, "achieve", "ploc", my_url, atom_codec_id
        )
        print("Test KO")

    except send_acl_message.SendFailureException:
        print("Test OK")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
