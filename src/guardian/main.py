from __future__ import annotations

import logging
import threading
from pathlib import Path
from typing import Any, Dict

import yaml

from .audio_sentinel import AudioSentinel
from .malcolm_client import MalcolmClient
from .policy_engine import PolicyEngine
from .security_watchdog import SecurityWatchdog
from .tools import execute_tool
from .learning import LearningEngine, PreferenceEvent
from .tts import TTSVoice
from .events import SecurityEvent
from .utils.logging_utils import setup_logging

logger = logging.getLogger(__name__)

def load_config(config_path: Path) -> Dict[str, Any]:
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

class MalcolmGuardian:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.config = load_config(root_dir / "config" / "config.yaml")

        logs_dir = root_dir / "logs"
        setup_logging(logs_dir)

        # TTS
        tts_cfg = self.config.get("tts", {})
        self.tts = TTSVoice(
            rate=tts_cfg.get("rate", 180),
            volume=tts_cfg.get("volume", 1.0),
            voice_name=tts_cfg.get("voice_name"),
        ) if tts_cfg.get("enabled", True) else None

        # Malcolm Client
        m_cfg = self.config.get("malcolm_api", {})
        self.malcolm = MalcolmClient(
            base_url=m_cfg.get("base_url", ""),
            api_key=m_cfg.get("api_key", ""),
            enabled=m_cfg.get("enabled", False),
            timeout_seconds=m_cfg.get("timeout_seconds", 15),
        )

        # Policy Engine
        p_cfg = self.config.get("policy", {})
        self.policy = PolicyEngine(
            auto_allow=p_cfg.get("auto_allow_tools", []),
            confirm_tools=p_cfg.get("confirm_tools", []),
        )

        # Learning
        l_cfg = self.config.get("learning", {})
        self.learning = LearningEngine(
            enabled=l_cfg.get("enabled", True),
            log_dir=logs_dir,
        )

        # Audio
        a_cfg = self.config.get("audio", {})
        self.audio_sentinel = AudioSentinel(
            wake_word=a_cfg.get("wake_word", "malcolm"),
            stt_language=self.config.get("stt", {}).get("language", "en-GB"),
            on_command=self.handle_voice_command,
        )

        # Security Watchdog
        s_cfg = self.config.get("security", {})
        self.security_watchdog = SecurityWatchdog(
            interval_seconds=s_cfg.get("process_scan_interval_seconds", 15),
            suspicious_cpu_threshold=s_cfg.get("suspicious_cpu_threshold", 75.0),
            suspicious_names=s_cfg.get("suspicious_names", []),
            on_event=self.handle_security_event,
        )

        self._quiet_mode = a_cfg.get("quiet_mode", False)
        logger.info("MalcolmGuardian initialised (quiet_mode=%s).", self._quiet_mode)

    # --- Event handlers ---

    def handle_voice_command(self, command: str) -> None:
        logger.info("Handling voice command: %s", command)
        context = {
            "source": "voice",
            "quiet_mode": self._quiet_mode,
        }
        response = self.malcolm.send_text_to_malcolm(command, context=context)

        # Speak reply
                # Speak reply (always, as long as TTS is enabled)
        if self.tts and response.reply_text:
            self.tts.speak(response.reply_text)


        # Handle tool calls
        for tc in response.tool_calls:
            decision = self.policy.evaluate_tool_call(tc)
            if decision.requires_confirmation:
                summary = f"Malcolm wants to execute '{decision.tool}'. Allow?"
                logger.info(summary)
                if self.tts and not self._quiet_mode:
                    self.tts.speak(summary + " Please answer in the console with Y or N.")
                allow = self._ask_console_confirmation(decision)
                self.learning.record_preference(PreferenceEvent(tool=decision.tool, confirmed=allow))
                if not allow:
                    logger.info("User denied tool %s.", decision.tool)
                    continue
            result = execute_tool(decision.tool, decision.args)
            logger.info("Tool result: %s", result)
            self._maybe_update_local_state(decision.tool)

    def handle_security_event(self, event: SecurityEvent) -> None:
        logger.info("Security event: %s", event.description)
        if self._quiet_mode:
            return
        if self.tts:
            self.tts.speak(f"Security note: {event.description}")

    def _ask_console_confirmation(self, decision) -> bool:
        while True:
            ans = input(f"Allow Malcolm to execute '{decision.tool}' with args {decision.args}? [y/n]: ").strip().lower()
            if ans in {"y", "yes"}:
                return True
            if ans in {"n", "no"}:
                return False

    def _maybe_update_local_state(self, tool: str) -> None:
        if tool == "enter_quiet_mode":
            self._quiet_mode = True
        elif tool == "exit_quiet_mode":
            self._quiet_mode = False

    # --- Lifecycle ---

    def start(self) -> None:
        logger.info("Starting MalcolmGuardian subsystems.")
        self.audio_sentinel.start()
        self.security_watchdog.start()
        if self.tts and not self._quiet_mode:
            self.tts.speak("Malcolm Guardian is now active.")

    def stop(self) -> None:
        logger.info("Stopping MalcolmGuardian.")
        self.audio_sentinel.stop()
        self.security_watchdog.stop()
        if self.tts:
            self.tts.shutdown()

def run_guardian() -> None:
    root_dir = Path(__file__).resolve().parents[2]
    guardian = MalcolmGuardian(root_dir=root_dir)
    guardian.start()
    try:
        # Keep main thread alive
        threading.Event().wait()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received; shutting down.")
        guardian.stop()
