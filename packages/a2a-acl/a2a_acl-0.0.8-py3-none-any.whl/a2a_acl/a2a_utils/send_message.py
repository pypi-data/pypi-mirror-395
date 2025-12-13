from uuid import uuid4

import httpx
from a2a.client import A2AClient, A2AClientTimeoutError
from a2a.server.events import EventQueue
from a2a.types import (
    SendMessageRequest,
    MessageSendConfiguration,
    PushNotificationConfig,
    MessageSendParams,
    AgentCard,
)
from a2a.utils import new_agent_text_message

from a2a_acl.protocol.message_codec import extract_text


async def send_a2a_request(
    client: A2AClient, request: SendMessageRequest
) -> str | None:
    try:
        response = await client.send_message(request)
        t = extract_text(response)
        print("(Synchronous reply received: " + str(t) + ")")
        return t
    except A2AClientTimeoutError:
        print("Warning: No acknowledgement received before timeout.")
        return None


async def send_a2a_message(dest: AgentCard | str, request: SendMessageRequest):
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=30)) as httpx_client:
        if isinstance(dest, AgentCard):
            client = A2AClient(httpx_client=httpx_client, agent_card=dest)
        else:
            client = A2AClient(httpx_client=httpx_client, url=dest)

        res = await send_a2a_request(client, request)
        return res


async def sync_reply(output_event_queue: EventQueue, r: str):
    await output_event_queue.enqueue_event(new_agent_text_message(r))


def build_basic_text_request(content: str, reply_to_url: str) -> SendMessageRequest:
    c = MessageSendConfiguration(
        push_notification_config=PushNotificationConfig(url=reply_to_url)
    )
    m = {
        "message": {
            "role": "user",
            "parts": [
                {
                    "kind": "text",
                    "text": content,
                }
            ],
            "messageId": uuid4().hex,
        },
        "configuration": c,
    }
    params = MessageSendParams(**m)
    return SendMessageRequest(id=str(uuid4()), params=params)
