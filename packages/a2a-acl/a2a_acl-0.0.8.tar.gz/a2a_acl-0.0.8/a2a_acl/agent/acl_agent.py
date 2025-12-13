from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import AgentCard

import a2a_acl.content_codecs.common as common
from a2a_acl.protocol.message_codec import bdi_of_a2a
from a2a_acl.protocol.acl_message import Illocution, ACLMessage
from a2a_acl.protocol.send_acl_message import (
    spawn_send_acl_message,
    default_message_handler,
    default_task_handler,
)
from a2a_acl.content_codecs.common import Codec
from a2a_acl.interface.interface import ACLAgentCard

import a2a_acl.content_codecs.python_codec as python_codec
import a2a_acl.content_codecs.atom_codec as atom_codec


class ACLAgentExecutor(AgentExecutor):

    def __init__(self, agentcard: ACLAgentCard, my_url: str):
        self.public_entry_points = [s.functor for s in agentcard.skills]
        self.codecs = agentcard.supported_codecs
        self.print_entry_points()
        self.print_codecs()
        self.card = agentcard
        self.my_url = my_url
        self.codec_objects = {
            common.python_codec_id: python_codec.codec_object,
            common.atom_codec_id: atom_codec.codec_object,
        }

    def print_entry_points(self):
        print("Public entry points:")
        for entry_point in self.public_entry_points:
            print(" " + str(entry_point))

    def print_codecs(self):
        print("Public codecs:")
        for codec in self.codecs:
            print(" " + str(codec))

    def get_codec_object(self, codec_name: str) -> Codec:
        if codec_name in self.codec_objects:
            return self.codec_objects[codec_name]
        else:
            print("Codec " + codec_name + " not supported.")
            raise NotImplementedError

    def firewall_accept(self, m: ACLMessage) -> bool:
        c = self.get_codec_object(m.codec)
        ep = c.extract_entry_point(m.content)
        if ep not in self.public_entry_points:
            print("Received a message on an entry point which is not public: " + ep)
            print("Message not handled.")
            return False
        else:
            return True

    def codec_accept(self, m: ACLMessage) -> bool:
        if m.codec in self.codecs:
            return True
        else:
            print("Codec not supported : " + m.codec)
            print("Message not handled.")
            return False

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        m: ACLMessage = bdi_of_a2a(context)
        if self.codec_accept(m) and self.firewall_accept(m):
            match m.illocution:
                case Illocution.TELL:
                    await self.execute_tell(m, event_queue)
                case Illocution.ACHIEVE:
                    await self.execute_achieve(m, event_queue)
                case Illocution.ASK:
                    await self.execute_ask(m, event_queue)

    # Override-me
    async def execute_tell(self, m: ACLMessage, event_queue: EventQueue) -> None:
        pass

    # Override-me
    async def execute_achieve(self, m: ACLMessage, event_queue: EventQueue) -> None:
        pass

    # Override-me
    async def execute_ask(self, m: ACLMessage, event_queue: EventQueue) -> None:
        pass

    def check_public_entry_point(self, m: ACLMessage, codec: Codec):
        entry_point = codec.extract_entry_point(m.content)
        return entry_point in self.public_entry_points

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("Cancel not supported.")

    def send_message(
        self,
        dest: AgentCard | str,
        illocution: str,
        content: str,
        codec: str,
        message_processor=default_message_handler,
        task_processor=default_task_handler,
    ):
        spawn_send_acl_message(
            dest,
            illocution,
            content,
            self.my_url,
            codec,
            message_processor,
            task_processor,
        )
