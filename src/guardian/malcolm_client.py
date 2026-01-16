from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class MalcolmResponse:
    def __init__(self, reply_text: str, tool_calls: Optional[List[Dict[str, Any]]] = None) -> None:
        self.reply_text = reply_text
        self.tool_calls: List[Dict[str, Any]] = tool_calls or []


class MalcolmClient:
    """
    MalcolmClient – Live + Offline Hybrid

    Responsibilities:
    -----------------
    - Talk to Malcolm's live Omni API at {base_url}/omni/command
    - Normalise any JSON reply into:
        * reply_text (always speakable)
        * tool_calls (list[{tool, args}])
    - Fall back to a local stub when the live core is unreachable (network errors).

    Request:
    --------
    POST {base_url}/omni/command
    Headers:
      Authorization: Bearer <api_key>
      Content-Type: application/json

    Body:
      {
        "command": "<user voice command text>",
        "context": { ... arbitrary JSON with guardian/system context ... }
      }

    Response (flexible):
    --------------------
    Common shapes include:

      1) High-level conversational:
         {
           "message": "I've activated your security shield.",
           "actions": [
             { "type": "shield:activate", "details": {} }
           ]
         }

      2) Acknowledgement / echo:
         {
           "received_command": "activate security",
           "status": "executed"
         }

      3) Tool-first:
         {
           "reply_text": "Checking your top processes.",
           "tool_calls": [
             { "tool": "describe_top_processes", "args": { "limit": 5 } }
           ]
         }

    All of these are normalised into:
      MalcolmResponse(
        reply_text="Malcolm says: <natural language summary>",
        tool_calls=[{"tool": "...", "args": {...}}, ...]
      )
    """

    def __init__(self, base_url: str, api_key: str, enabled: bool = False, timeout_seconds: int = 15) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or ""
        self.enabled = enabled
        self.timeout_seconds = timeout_seconds
        logger.info("MalcolmClient initialised. Enabled=%s, Base URL=%s", self.enabled, self.base_url)

    # ------------------------------------------------------------------ #
    # Public entrypoint used by the guardian
    # ------------------------------------------------------------------ #
    def send_text_to_malcolm(self, text: str, context: Dict[str, Any]) -> MalcolmResponse:
        """
        Called by the guardian whenever the user speaks a command
        (after wake-word removal).
        """
        logger.info("Sending to Malcolm Omni API: %s", text)

        # If disabled in config, behave like a pure local stub.
        if not self.enabled:
            reply = f"You said: '{text}'. Malcolm API is currently disabled in config."
            return MalcolmResponse(reply_text=reply, tool_calls=[])

        if not self.base_url:
            logger.error("MalcolmClient is enabled but base_url is empty.")
            return MalcolmResponse(
                reply_text="Malcolm API base_url is not configured. Please check config.yaml.",
                tool_calls=[],
            )

        try:
            data = self._call_omni_command(text, context)

            # Normal live path (even if status isn't 200, we turn it into a message)
            reply_text_raw = self._extract_reply_text(data)
            tool_calls = self._extract_tool_calls(data)

            # Make it obvious in speech that this is Malcolm talking
            if reply_text_raw:
                spoken_reply = f"Malcolm says: {reply_text_raw}"
            else:
                spoken_reply = "Malcolm has no reply text for this command."

            logger.info("Malcolm reply: %s", reply_text_raw)
            logger.info("Malcolm tool_calls: %s", tool_calls)
            return MalcolmResponse(reply_text=spoken_reply, tool_calls=tool_calls)

        except Exception as e:
            logger.exception("Error communicating with Malcolm Omni API: %s", e)
            # On unexpected communication errors, fall back to a local stub.
            return self._offline_stub_response(text)

    # ------------------------------------------------------------------ #
    # Local stub fallback (used when live Malcolm is unreachable)
    # ------------------------------------------------------------------ #
    def _offline_stub_response(self, text: str) -> MalcolmResponse:
        """
        Local fallback when the live Malcolm API is unavailable.
        Behaves like a simple guardian brain: echoes text and triggers
        some intuitive tool calls based on keywords.
        """
        reply = f"Malcolm says: I could not reach my live core just now, but I heard you say: '{text}'. I will respond locally."
        tool_calls: List[Dict[str, Any]] = []
        lowered = text.lower()

        # Simple intent heuristics
        if "quiet mode" in lowered and "exit" not in lowered:
            tool_calls.append({"tool": "enter_quiet_mode", "args": {}})
            reply += " I will enter quiet mode."
        elif "exit quiet" in lowered or "leave quiet" in lowered:
            tool_calls.append({"tool": "exit_quiet_mode", "args": {}})
            reply += " I will exit quiet mode."
        elif "top process" in lowered or "cpu" in lowered or "performance" in lowered:
            tool_calls.append({"tool": "describe_top_processes", "args": {"limit": 5}})
            reply += " Let me check your top processes now."

        return MalcolmResponse(reply_text=reply, tool_calls=tool_calls)

    # ------------------------------------------------------------------ #
    # HTTP helper
    # ------------------------------------------------------------------ #
    def _auth_headers(self) -> Dict[str, str]:
        """
        Build Authorization header.

        We treat the configured `api_key` as a Bearer token.
        If your backend expects a JWT from /login instead,
        that token should be placed in api_key.
        """
        headers: Dict[str, str] = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _call_omni_command(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        POST {base_url}/omni/command with JSON payload.

        If the HTTP status is not 2xx, we return a diagnostic JSON so
        the guardian can speak a clear error instead of a cryptic body.
        """
        url = f"{self.base_url}/omni/command"
        payload: Dict[str, Any] = {
            "command": text,
            "context": context or {},
        }

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            **self._auth_headers(),
        }

        logger.debug("POST %s payload=%s headers=%s", url, payload, headers)
        resp = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=self.timeout_seconds,
        )
        logger.info("Malcolm API POST status: %s", resp.status_code)

        # If status is not 2xx, turn this into a clear error message
        if not resp.ok:
            body_snippet = resp.text.strip()
            if len(body_snippet) > 200:
                body_snippet = body_snippet[:200] + "…"
            return {
                "message": (
                    f"Malcolm API error {resp.status_code} when calling /omni/command. "
                    f"Response was: {body_snippet or 'no body'}."
                ),
                "actions": [],
            }

        # Normal JSON / text handling
        try:
            data = resp.json()
            logger.debug("Raw Malcolm JSON: %s", data)
            return data
        except ValueError:
            text_body = resp.text
            logger.warning("Malcolm responded with non-JSON body: %s", text_body[:500])
            return {"message": text_body}

    # ------------------------------------------------------------------ #
    # Normalisation helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _extract_reply_text(data: Dict[str, Any]) -> str:
        """
        Derive a natural, speakable reply string from Malcolm's JSON.

        Priority:
        1. data["message"], data["reply_text"], data["reply"]
        2. common nested fields in data["data"]
        3. special acknowledgement shapes like {"received_command": "...", "status": "..."}
        4. error / status-only responses
        5. data["response"] (string)
        6. JSON-dumped fallback (for debugging)
        """
        # 1. Top-level preferred keys (most conversational)
        for key in ("message", "reply_text", "reply"):
            val = data.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()

        # 2. Nested "data" dictionary with common keys
        nested = data.get("data")
        if isinstance(nested, dict):
            for key in ("message", "reply", "text", "response"):
                val = nested.get(key)
                if isinstance(val, str) and val.strip():
                    return val.strip()

        # 3. Acknowledgement / echo pattern:
        #    {"received_command": "activate security", "status": "executed"}
        received_command = data.get("received_command")
        status = data.get("status")
        if isinstance(received_command, str) and isinstance(status, str):
            return f"The command '{received_command}' has status: {status}."

        # 4. Error or status-only responses
        error = data.get("error") or data.get("detail") or data.get("message_error")
        if isinstance(error, str) and error.strip():
            return f"There was an error from Malcolm: {error.strip()}"

        if isinstance(status, str) and status.strip() and not received_command:
            return f"Current status reported by Malcolm is: {status.strip()}."

        # 5. Top-level "response" string
        resp = data.get("response")
        if isinstance(resp, str) and resp.strip():
            return resp.strip()

        # 6. Fallback: JSON dump (for debugging, still speakable)
        try:
            return json.dumps(data, indent=2)
        except Exception:
            return str(data)

    @staticmethod
    def _extract_tool_calls(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Normalise action / tool structures into our internal form:

        1) Direct tool_calls:
           {
             "tool_calls": [
               { "tool": "describe_top_processes", "args": { ... } },
               ...
             ]
           }

        2) Daemon-style actions:
           {
             "actions": [
               { "type": "kill_process", "details": { "pid": 1234 } },
               { "type": "describe_top_processes", "details": { "limit": 5 } }
             ]
           }
        """
        tool_calls: List[Dict[str, Any]] = []

        # Style 1: direct tool_calls
        raw_tc = data.get("tool_calls")
        if isinstance(raw_tc, list):
            for tc in raw_tc:
                if not isinstance(tc, dict):
                    continue
                tool = tc.get("tool")
                args = tc.get("args", {}) or {}
                if not tool:
                    continue
                tool_calls.append({"tool": tool, "args": args})

        # Style 2: daemon-style actions
        raw_actions = data.get("actions")
        if isinstance(raw_actions, list):
            for action in raw_actions:
                if not isinstance(action, dict):
                    continue
                tool = action.get("tool") or action.get("type")
                args = (
                    action.get("args")
                    or action.get("details")
                    or action.get("params")
                    or {}
                )
                if not tool:
                    continue
                tool_calls.append({"tool": tool, "args": args})

        return tool_calls
