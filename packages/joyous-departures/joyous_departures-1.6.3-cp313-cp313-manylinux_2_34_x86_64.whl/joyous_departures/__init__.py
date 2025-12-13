"""
Joyous Departures - Generate warm, heartfelt sign-off messages

This package provides an async API for generating goodbye messages.
The core implementation is in Rust for performance.
"""

import asyncio
from typing import Optional, Dict, Callable, Awaitable

# Import the Rust extension module (now a submodule of joyous_departures)
from ._joy_generator import generate_goodbye as _generate_goodbye_sync

# Re-export the sync function as well for backwards compatibility
from ._joy_generator import generate_goodbye as generate_goodbye_sync


async def generate_goodbye(
    *,
    language_code: Optional[str] = None,
    template_args: Optional[Dict[str, str]] = None,
    use_emojis: bool = True,
    timezone: str = "Europe/London",
    translator: Optional[Callable[[str, str], Awaitable[str]]] = None,
) -> str:
    """
    Generates a random warm sign-off message (async)

    Note: This function wraps the synchronous Rust implementation in an async executor.
    The Rust core is intentionally synchronous because it performs CPU-bound work
    (string manipulation, random selection, template replacement) with no I/O operations.
    Rust's async is designed for I/O-bound operations; for CPU-bound work, synchronous
    code is more efficient. We provide an async interface here for compatibility with
    async Python codebases, but the actual work runs synchronously in a thread pool.

    Args:
        language_code: Optional ISO 639-1 language code (default: "en-GB")
        template_args: Optional dict with template variables (name, location, date, time)
        use_emojis: Optional bool to include emojis (default: True)
        timezone: Optional IANA timezone identifier (default: "Europe/London")
        translator: Optional async translator callback for custom languages

    Returns:
        str: Generated goodbye message

    Example:
        >>> import asyncio
        >>> from joyous_departures import generate_goodbye
        >>>
        >>> async def main():
        ...     message = await generate_goodbye(template_args={"name": "Alice"})
        ...     print(message)
        >>>
        >>> asyncio.run(main())
    """
    # Call sync function in executor to make it async
    # The Rust implementation is synchronous, so we run it in a thread pool executor
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: _generate_goodbye_sync(
            language_code=language_code,
            template_args=template_args,
            use_emojis=use_emojis,
            timezone=timezone,
        ),
    )

    # If translator provided and language is not en-GB, translate
    if translator and language_code and language_code != "en-GB":
        try:
            result = await translator(language_code, result)
        except Exception:
            # Fallback to original if translation fails
            pass

    return result


__all__ = ["generate_goodbye", "generate_goodbye_sync"]
__version__ = "0.1.0"
