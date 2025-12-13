from dataclasses import dataclass
from enum import StrEnum


class Illocution(StrEnum):
    """Illocutions that are used in messages."""

    TELL = "tell"
    ACHIEVE = "achieve"
    ASK = "ask"


@dataclass
class ACLMessage:
    illocution: Illocution
    content: str
    sender: str
    codec: str
    task_id: str | None = None
