from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

@dataclass
class ToolDecision:
    tool: str
    args: Dict[str, Any]
    requires_confirmation: bool

class PolicyEngine:
    def __init__(self, auto_allow: List[str], confirm_tools: List[str]) -> None:
        self.auto_allow = set(auto_allow)
        self.confirm_tools = set(confirm_tools)
        logger.info("PolicyEngine initialised. Auto=%s Confirm=%s", self.auto_allow, self.confirm_tools)

    def evaluate_tool_call(self, tool_call: Dict[str, Any]) -> ToolDecision:
        tool = tool_call.get("tool")
        args = tool_call.get("args", {})
        logger.info("Evaluating tool call: %s %s", tool, args)
        if tool in self.auto_allow:
            return ToolDecision(tool=tool, args=args, requires_confirmation=False)
        if tool in self.confirm_tools:
            return ToolDecision(tool=tool, args=args, requires_confirmation=True)
        # Default: be conservative
        logger.info("Tool %s is unknown; requiring confirmation.", tool)
        return ToolDecision(tool=tool, args=args, requires_confirmation=True)
