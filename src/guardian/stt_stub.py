import logging
from typing import Optional

import speech_recognition as sr

logger = logging.getLogger(__name__)

class STTEngine:
    """Simple wrapper around SpeechRecognition.

    Default backend: Google Web Speech API (free, but cloud-based).
    You can swap this for another backend if you prefer.
    """

    def __init__(self, language: str = "en-GB") -> None:
        self.recognizer = sr.Recognizer()
        self.language = language

    def phrase_to_text(self, audio: sr.AudioData) -> Optional[str]:
        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.info("STT recognised: %s", text)
            return text
        except sr.UnknownValueError:
            logger.info("STT could not understand audio.")
            return None
        except sr.RequestError as e:
            logger.warning("STT request error: %s", e)
            return None
