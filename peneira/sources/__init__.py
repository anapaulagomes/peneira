from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ResultBundle:
    """Class that holds a response result and its properties."""

    url: str
    source: str
    results: list[dict] = field(default_factory=list, repr=False)
    created_at: datetime = field(default_factory=datetime.utcnow)
