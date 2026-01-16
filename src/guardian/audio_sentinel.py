from __future__ import annotations

import logging
import threading
from typing import Callable, Optional

import speech_recognition as sr

from .stt_stub import STTEngine

logger = logging.getLogger(__name__)

class AudioSentinel:
    def __init__(
        self,
        wake_word: str,
        stt_language: str,
        on_command: Callable[[str], None],
    ) -> None:
        self.wake_word = wake_word.lower()
        self.stt = STTEngine(language=stt_language)
        self.on_command = on_command
        self._stop_flag = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        logger.info("AudioSentinel starting background listener.")
        self._thread.start()

    def stop(self) -> None:
        logger.info("AudioSentinel stopping.")
        self._stop_flag.set()

    def _run(self) -> None:
        recognizer = self.stt.recognizer
        mic = sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            logger.info("Calibrated microphone for ambient noise.")
            while not self._stop_flag.is_set():
                try:
                    logger.info("Listening for speech...")
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=10)
                except Exception as e:
                    logger.warning("Error while listening: %s", e)
                    continue

                text = self.stt.phrase_to_text(audio)
                if not text:
                    continue
                lowered = text.lower()
                if self.wake_word in lowered:
                    # Strip wake word so only the command remains
                    command = lowered.replace(self.wake_word, "", 1).strip()
                    if not command:
                        command = text  # fallback: full text
                    logger.info("Wake word detected. Command: %s", command)
                    self.on_command(command)
                else:
                    logger.info("Heard speech but no wake word: %s", text)
