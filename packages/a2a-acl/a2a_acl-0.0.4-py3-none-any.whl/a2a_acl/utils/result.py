from dataclasses import dataclass


@dataclass
class Result:
    success: bool
    reason: str | None
