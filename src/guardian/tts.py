import logging
import threading
from queue import Queue, Empty
from typing import Optional

import pyttsx3

logger = logging.getLogger(__name__)


class TTSVoice:
    """
    Robust, per-utterance TTS wrapper around pyttsx3.

    - Uses a single worker thread and a queue.
    - For each queued text, the worker creates a *fresh* pyttsx3 engine,
      speaks the text, then disposes it.
    - Guarantees only one runAndWait() at a time, avoiding both:
        * 'run loop already started'
        * long-lived engine getting stuck forever
    """

    def __init__(self, rate: int = 180, volume: float = 1.0, voice_name: Optional[str] = None) -> None:
        self.rate = rate
        self.volume = volume
        self.voice_name = voice_name

        self._queue: "Queue[Optional[str]]" = Queue()
        self._running = True
        self._worker = threading.Thread(target=self._loop, daemon=True)
        self._worker.start()

        logger.info("TTSVoice initialised (per-utterance queued mode).")

    # ------------------------------------------------------------------ #
    # Worker loop
    # ------------------------------------------------------------------ #
    def _loop(self) -> None:
        while self._running:
            try:
                text = self._queue.get(timeout=0.5)
            except Empty:
                continue

            if text is None:
                # Shutdown signal
                break

            self._speak_once(text)

    def _speak_once(self, text: str) -> None:
        """
        Create a fresh engine, speak the text, then dispose it.
        """
        try:
            logger.info("pyttsx3 engine BEGIN speaking text: %s", text)
            engine = pyttsx3.init()

            # Base properties
            try:
                engine.setProperty("rate", self.rate)
            except Exception as e:
                logger.warning("Could not set TTS rate: %s", e)

            try:
                engine.setProperty("volume", self.volume)
            except Exception as e:
                logger.warning("Could not set TTS volume: %s", e)

            # Optional voice selection
            if self.voice_name:
                try:
                    voices = engine.getProperty("voices")
                    for v in voices:
                        if self.voice_name.lower() in v.name.lower():
                            engine.setProperty("voice", v.id)
                            break
                except Exception as e:
                    logger.warning("Could not set custom voice '%s': %s", self.voice_name, e)

            engine.say(text)
            engine.runAndWait()
            logger.info("pyttsx3 engine FINISHED speaking.")

            try:
                engine.stop()
            except Exception:
                pass

        except Exception as e:
            logger.exception("TTS error while speaking: %s", e)

    # ------------------------------------------------------------------ #
    # Public API used by guardian
    # ------------------------------------------------------------------ #
    def speak(self, text: str) -> None:
        """
        Enqueue text to be spoken by the worker thread.
        """
        if not text or not text.strip():
            return
        logger.info("TTS speaking: %s", text)
        self._queue.put(text)

    def shutdown(self) -> None:
        """
        Stop the worker cleanly.
        """
        logger.info("TTSVoice shutdown requested.")
        self._running = False
        self._queue.put(None)
        logger.info("TTSVoice shut down.")
