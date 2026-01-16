from dataclasses import dataclass, field
from typing import Any, Dict
import time

@dataclass
class SecurityEvent:
    event_type: str
    description: str
    severity: str = "info"
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
