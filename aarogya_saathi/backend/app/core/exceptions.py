from typing import Any, Dict, Optional


class AarogyaException(Exception):
    """Base exception for the Aarogya application."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

    def __str__(self):
        return f"{self.message} (Details: {self.details})"


# --- CORE & CONFIGURATION ERRORS ---
class ConfigurationError(AarogyaException):
    """Raised when API keys or env vars are missing."""

    def __init__(self, message: str = "System configuration error."):
        super().__init__(message, status_code=503)


class AuthenticationError(AarogyaException):
    """Raised when authentication (e.g., OTP) fails."""

    def __init__(self, message: str = "Authentication failed."):
        super().__init__(message, status_code=401)


# --- AI SERVICE ERRORS ---
class STTError(AarogyaException):
    """Raised when Deepgram fails."""

    def __init__(
        self, message: str = "Speech-to-Text service failed.", details: dict = None
    ):
        super().__init__(message, status_code=502, details=details)


class LLMError(AarogyaException):
    """Raised when Groq/Llama-3 fails."""

    def __init__(self, message: str = "LLM generation failed.", details: dict = None):
        super().__init__(message, status_code=502, details=details)


class TTSError(AarogyaException):
    """Raised when ElevenLabs fails."""

    def __init__(
        self, message: str = "Text-to-Speech service failed.", details: dict = None
    ):
        super().__init__(message, status_code=502, details=details)


# --- AGENTIC ERRORS ---
class AgentError(AarogyaException):
    """Raised when an agent (Triage/Nudge) enters an invalid state."""

    def __init__(self, agent_name: str, message: str):
        super().__init__(f"[{agent_name}]: {message}", status_code=400)


class SafetyViolationError(AarogyaException):
    """Raised when MedPrompt detects unsafe content."""

    def __init__(self, reason: str):
        super().__init__(f"Safety Violation: {reason}", status_code=422)
