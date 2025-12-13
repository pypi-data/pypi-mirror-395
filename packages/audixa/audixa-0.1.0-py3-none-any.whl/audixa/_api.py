"""
Audixa SDK Module-Level API Functions.

Provides convenience functions that use global configuration and default clients.
These functions are exposed at the top level of the audixa package.
"""

from __future__ import annotations

from typing import Any

from .async_client import AsyncAudixaClient
from .client import AudixaClient
from .config import get_config

# =============================================================================
# Default Client Singletons
# =============================================================================

_default_client: AudixaClient | None = None
_default_async_client: AsyncAudixaClient | None = None


def _get_default_client() -> AudixaClient:
    """Get or create the default synchronous client."""
    global _default_client
    if _default_client is None:
        _default_client = AudixaClient()
    return _default_client


def _get_default_async_client() -> AsyncAudixaClient:
    """Get or create the default asynchronous client."""
    global _default_async_client
    if _default_async_client is None:
        _default_async_client = AsyncAudixaClient()
    return _default_async_client


# =============================================================================
# Synchronous API Functions
# =============================================================================

def tts(
    text: str,
    voice_id: str | None = None,
    **kwargs: Any,
) -> str:
    """
    Generate speech from text (synchronous).
    
    This initiates TTS generation and returns a generation ID.
    Use status() to check progress, or tts_and_wait() for convenience.
    
    Args:
        text: The text to convert to speech.
        voice_id: Optional voice ID. Uses default voice if not specified.
        **kwargs: Additional parameters passed to the API.
        
    Returns:
        The generation ID for tracking the request.
        
    Example:
        >>> import audixa
        >>> audixa.set_api_key("your-key")
        >>> gen_id = audixa.tts("Hello, world!")
        >>> print(gen_id)
    """
    return _get_default_client().tts(text, voice_id=voice_id, **kwargs)


def status(generation_id: str) -> dict[str, Any]:
    """
    Check the status of a TTS generation (synchronous).
    
    Args:
        generation_id: The generation ID from tts().
        
    Returns:
        Status dictionary with 'status', 'audio_url', etc.
        
    Example:
        >>> status = audixa.status("gen_abc123")
        >>> print(status["status"])
    """
    return _get_default_client().status(generation_id)


def tts_and_wait(
    text: str,
    voice_id: str | None = None,
    poll_interval: float | None = None,
    timeout: float | None = None,
    **kwargs: Any,
) -> str:
    """
    Generate speech and wait for completion (synchronous).
    
    Args:
        text: The text to convert to speech.
        voice_id: Optional voice ID.
        poll_interval: Time between status checks in seconds.
        timeout: Maximum time to wait in seconds.
        **kwargs: Additional parameters passed to the API.
        
    Returns:
        The audio URL for the completed generation.
        
    Example:
        >>> audio_url = audixa.tts_and_wait("Hello!")
        >>> print(audio_url)
    """
    config = get_config()
    return _get_default_client().tts_and_wait(
        text,
        voice_id=voice_id,
        poll_interval=poll_interval or config.poll_interval,
        timeout=timeout or config.wait_timeout,
        **kwargs,
    )


def tts_to_file(
    text: str,
    filepath: str,
    voice_id: str | None = None,
    poll_interval: float | None = None,
    timeout: float | None = None,
    **kwargs: Any,
) -> str:
    """
    Generate speech and save to a file (synchronous).
    
    Args:
        text: The text to convert to speech.
        filepath: Output file path. Must have .wav extension.
        voice_id: Optional voice ID.
        poll_interval: Time between status checks in seconds.
        timeout: Maximum time to wait in seconds.
        **kwargs: Additional parameters passed to the API.
        
    Returns:
        The path to the saved audio file.
        
    Example:
        >>> audixa.tts_to_file("Hello!", "output.wav")
    """
    config = get_config()
    return _get_default_client().tts_to_file(
        text,
        filepath,
        voice_id=voice_id,
        poll_interval=poll_interval or config.poll_interval,
        timeout=timeout or config.wait_timeout,
        **kwargs,
    )


def list_voices() -> list[dict[str, Any]]:
    """
    List available voices (synchronous).
    
    Returns:
        List of voice dictionaries.
        
    Example:
        >>> voices = audixa.list_voices()
        >>> for v in voices:
        ...     print(v["name"])
    """
    return _get_default_client().list_voices()


# =============================================================================
# Asynchronous API Functions
# =============================================================================

async def atts(
    text: str,
    voice_id: str | None = None,
    **kwargs: Any,
) -> str:
    """
    Generate speech from text (asynchronous).
    
    Args:
        text: The text to convert to speech.
        voice_id: Optional voice ID.
        **kwargs: Additional parameters passed to the API.
        
    Returns:
        The generation ID for tracking the request.
        
    Example:
        >>> gen_id = await audixa.atts("Hello!")
    """
    return await _get_default_async_client().tts(text, voice_id=voice_id, **kwargs)


async def astatus(generation_id: str) -> dict[str, Any]:
    """
    Check the status of a TTS generation (asynchronous).
    
    Args:
        generation_id: The generation ID from atts().
        
    Returns:
        Status dictionary with 'status', 'audio_url', etc.
        
    Example:
        >>> status = await audixa.astatus("gen_abc123")
    """
    return await _get_default_async_client().status(generation_id)


async def atts_and_wait(
    text: str,
    voice_id: str | None = None,
    poll_interval: float | None = None,
    timeout: float | None = None,
    **kwargs: Any,
) -> str:
    """
    Generate speech and wait for completion (asynchronous).
    
    Args:
        text: The text to convert to speech.
        voice_id: Optional voice ID.
        poll_interval: Time between status checks in seconds.
        timeout: Maximum time to wait in seconds.
        **kwargs: Additional parameters passed to the API.
        
    Returns:
        The audio URL for the completed generation.
        
    Example:
        >>> audio_url = await audixa.atts_and_wait("Hello!")
    """
    config = get_config()
    return await _get_default_async_client().tts_and_wait(
        text,
        voice_id=voice_id,
        poll_interval=poll_interval or config.poll_interval,
        timeout=timeout or config.wait_timeout,
        **kwargs,
    )


async def atts_to_file(
    text: str,
    filepath: str,
    voice_id: str | None = None,
    poll_interval: float | None = None,
    timeout: float | None = None,
    **kwargs: Any,
) -> str:
    """
    Generate speech and save to a file (asynchronous).
    
    Args:
        text: The text to convert to speech.
        filepath: Output file path. Must have .wav extension.
        voice_id: Optional voice ID.
        poll_interval: Time between status checks in seconds.
        timeout: Maximum time to wait in seconds.
        **kwargs: Additional parameters passed to the API.
        
    Returns:
        The path to the saved audio file.
        
    Example:
        >>> await audixa.atts_to_file("Hello!", "output.wav")
    """
    config = get_config()
    return await _get_default_async_client().tts_to_file(
        text,
        filepath,
        voice_id=voice_id,
        poll_interval=poll_interval or config.poll_interval,
        timeout=timeout or config.wait_timeout,
        **kwargs,
    )


async def alist_voices() -> list[dict[str, Any]]:
    """
    List available voices (asynchronous).
    
    Returns:
        List of voice dictionaries.
        
    Example:
        >>> voices = await audixa.alist_voices()
    """
    return await _get_default_async_client().list_voices()
