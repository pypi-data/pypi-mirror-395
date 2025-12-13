from a2a.server.events import EventQueue

import a2a_acl
from a2a_acl.agent.acl_agent import ACLAgentExecutor

from a2a_acl.protocol.acl_message import ACLMessage
from a2a_acl.a2a_utils.send_message import sync_reply

from a2a_acl.interface import asi_parser
from a2a_acl.interface.interface import ACLAgentCard


my_card = asi_parser.read_file("pingable.asi").add_codecs(
    [a2a_acl.content_codecs.common.atom_codec_id]
)


class PingableAgentExecutor(ACLAgentExecutor):

    def __init__(self, card: ACLAgentCard, url):
        super().__init__(agentcard=card, my_url=url)
        print(
            "Warning: launching a pure python A2A agent, unable to check .asi interface against python body."
        )

    async def execute_achieve(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ):
        print("(Received a message: " + str(m) + ")")
        match m.content:
            case "ping":
                print("Received a ping from " + m.sender)
                self.send_message(
                    m.sender,
                    "tell",
                    "pong",
                    a2a_acl.content_codecs.common.atom_codec_id,
                )
                await sync_reply(output_event_queue, "Achieve received")
                return

    async def execute_tell(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ):
        pass

    async def execute_ask(
        self,
        m: ACLMessage,
        output_event_queue: EventQueue,
    ):
        pass
