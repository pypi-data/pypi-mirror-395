from dataclasses import dataclass
from typing import Optional


@dataclass
class ServerSentEvent:
    id: Optional[str] = None
    # SSE Spec: 'The default event type is "message".'
    type: str = "message"
    data: Optional[str] = None
    retry: Optional[int] = None
