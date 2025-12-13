import asyncio
import uuid
from threading import Thread

from a2a.client import ClientFactory, ClientConfig
from a2a.types import (
    AgentCard,
    PushNotificationConfig,
    Message,
    Role,
    TextPart,
    Task,
)

from a2a_acl.a2a_utils.card_holder import download_card


def extract_text_from_message(m: Message) -> str:
    return m.parts[0].root.text


def extract_text_from_task(t: Task) -> str:
    res = ""
    for a in t.artifacts:
        for p in a.parts:
            if p.root.kind == "text":
                res = res + p.root.text
    return res


def default_message_handler(m: Message) -> None:
    print("(Sync reply received (Message): " + extract_text_from_message(m) + ")")


def default_task_handler(t: Task) -> None:
    print("(Sync reply received (Task Artifact): " + extract_text_from_task(t) + ")")


class SendFailureException(Exception):
    pass


# derived from https://github.com/a2aproject/a2a-samples/blob/main/samples/python/agents/number_guessing_game/utils/protocol_wrappers.py
async def send_acl_message(
    target: AgentCard | str,
    illocution: str,
    text: str,
    my_url: str,
    codec: str,
    message_processor=default_message_handler,
    task_processor=default_task_handler,
):
    """Send *text* to the target agent via the A2A ``message/send`` operation.

    Args:
        target: card or url of the target agent.
        illocution : illocution such as 'tell' or 'achieve'
        text: Payload to send as a plain-text message.
        my_url: the url of sender's server for replies.
        codec: the codec used to code the content of the message.
        message_processor: the processor used to process the 'message' text parts.
        task_processor: the processor used to process the 'task' text parts.

    Returns:
        Union[Task, Message]: The final object produced by the agent—normally a
        ``Task`` but may be a plain ``Message`` for very small interactions.
    """
    if isinstance(target, str):
        target = await download_card(target)
    _client_factory = ClientFactory(
        ClientConfig(push_notification_configs=[PushNotificationConfig(url=my_url)])
    )
    client = _client_factory.create(target)
    md: dict[str, str] = {"illocution": illocution, "codec": codec}
    msg = Message(
        kind="message",
        role=Role.agent,
        message_id=uuid.uuid4().hex,
        parts=[TextPart(text=text, metadata=md)],
        task_id=None,
        metadata=md,
    )

    last_message = None

    try:
        async for event in client.send_message(msg):
            # Unwrap tuple from transport implementations
            if isinstance(event, tuple):
                (event, other) = event
                if other is not None:
                    print(
                        "Additional info received with "
                        + str(type(event))
                        + ":"
                        + str(other)
                    )
            if isinstance(event, Message):
                if message_processor is not None:
                    message_processor(event)
                last_message = event
            elif isinstance(event, Task):
                if task_processor is not None:
                    task_processor(event)
            else:
                print("Event not supported: " + str(event))

        if last_message is not None:
            return last_message
        else:
            return None
    except Exception as e:
        print("Send failed.")
        raise SendFailureException


class SendMessageThread(Thread):
    def __init__(
        self,
        dest: AgentCard | str,
        illocution: str,
        content: str,
        sender: str,
        codec: str,
        message_processor=default_message_handler,
        task_processor=default_task_handler,
    ):
        super().__init__()
        self.dest = dest
        self.illocution = illocution
        self.content = content
        self.reply_to = sender
        self.codec = codec
        self.message_processor = message_processor
        self.task_processor = task_processor

    def run(self):
        loop = asyncio.new_event_loop()  # loop = asyncio.get_event_loop()
        loop.run_until_complete(
            send_acl_message(
                self.dest,
                self.illocution,
                self.content,
                self.reply_to,
                self.codec,
                self.message_processor,
                self.task_processor,
            )
        )
        loop.close()


def spawn_send_acl_message(
    dest: AgentCard | str,
    illocution: str,
    content: str,
    sender: str,
    codec: str,
    message_processor=default_message_handler,
    task_processor=default_task_handler,
) -> None:
    t = SendMessageThread(
        dest, illocution, content, sender, codec, message_processor, task_processor
    )
    t.start()
    print("(Send Thread launched.)")
