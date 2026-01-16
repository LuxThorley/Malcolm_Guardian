from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

@dataclass
class PreferenceEvent:
    tool: str
    confirmed: bool

class LearningEngine:
    def __init__(self, enabled: bool, log_dir: Path) -> None:
        self.enabled = enabled
        self.log_file = log_dir / "preferences.log"
        logger.info("LearningEngine initialised. Enabled=%s", self.enabled)

    def record_preference(self, event: PreferenceEvent) -> None:
        if not self.enabled:
            return
        try:
            with self.log_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"tool": event.tool, "confirmed": event.confirmed}) + "\n")
            logger.info("Recorded preference: %s", event)
        except Exception as e:
            logger.warning("Failed to record preference: %s", e)
