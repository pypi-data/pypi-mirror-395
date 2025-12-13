from a2a.server.agent_execution import RequestContext
from a2a.types import (
    SendMessageRequest,
    MessageSendParams,
    SendMessageResponse,
    SendMessageSuccessResponse,
    Message,
    MessageSendConfiguration,
    PushNotificationConfig,
)

from typing import Any
from uuid import uuid4

from a2a_acl.protocol.acl_message import ACLMessage


def extract_text(response: SendMessageResponse):
    """Extract text from synchronous replies"""
    if isinstance(response, SendMessageResponse):
        if isinstance(response.root, SendMessageSuccessResponse):
            if isinstance(response.root.result, Message):
                return response.root.result.parts[0].root.text
            else:
                print(
                    "Warning: Result of type: "
                    + str(type(response.root.result))
                    + " instead of Message."
                )
        else:
            print(
                "Warning: Root of type: "
                + str(type(response.root))
                + " instead of SendMessageSuccessResponse."
            )
    else:
        print(
            "Warning: Response of type: "
            + str(type(response))
            + " instead of SendMessageResponse."
        )

    return response.model_dump(mode="json", exclude_none=True)


def build_basic_message(
    illoc: str, content: str, c: MessageSendConfiguration, codec
) -> dict[str, Any]:
    return {
        "message": {
            "role": "user",
            "parts": [
                {
                    "kind": "text",
                    "metadata": {"illocution": illoc, "codec": codec},
                    "text": content,
                }
            ],
            "messageId": uuid4().hex,
        },
        "configuration": c,
    }


def build_basic_bdi_request(
    illoc: str, content: str, reply_to_url: str, codec: str
) -> SendMessageRequest:
    c = MessageSendConfiguration(
        push_notification_config=PushNotificationConfig(url=reply_to_url)
    )
    params = MessageSendParams(**build_basic_message(illoc, content, c, codec))
    return SendMessageRequest(id=str(uuid4()), params=params)


def bdi_of_a2a(context: RequestContext) -> ACLMessage:
    if (context.configuration is None) or (
        context.configuration.push_notification_config is None
    ):
        sender = None
    else:
        sender = context.configuration.push_notification_config.url
    if context.message.parts[0].root.metadata is None:
        error_message = "Incoming message not in BDI format (missing metadata)."
        print(error_message)
        raise Exception(error_message)
    else:
        i = context.message.parts[0].root.metadata["illocution"]
        c = context.message.parts[0].root.metadata["codec"]

    return ACLMessage(
        i, context.get_user_input(), sender, c, task_id=context.message.task_id
    )
