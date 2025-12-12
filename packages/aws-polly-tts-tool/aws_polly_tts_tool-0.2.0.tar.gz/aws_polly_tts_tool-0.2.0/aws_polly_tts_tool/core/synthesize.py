"""
Core text-to-speech synthesis functions for AWS Polly.

This module provides the fundamental TTS operations - converting text
to audio, playing through speakers, and saving to files. By keeping these
functions pure and CLI-independent, we enable both command-line and
programmatic usage while maintaining testability.

The streaming approach minimizes latency by processing audio data in memory
without disk I/O, making the tool responsive for interactive use cases like
voice assistants and real-time narration.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import os
import sys
import warnings
from io import BytesIO
from pathlib import Path
from typing import Any

# Suppress pydub's regex SyntaxWarnings (invalid escape sequences in pydub's own code)
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pydub")

from pydub import AudioSegment  # noqa: E402
from pydub.playback import play  # noqa: E402


def synthesize_audio(
    client: Any,
    text: str,
    voice_id: str,
    output_format: str = "mp3",
    engine: str = "neural",
    text_type: str = "text",
    sample_rate: str | None = None,
) -> tuple[bytes, int]:
    """
    Synthesize text to audio using AWS Polly.

    This is the core TTS operation that streams audio directly from Polly
    without disk I/O for optimal performance. Returns both audio bytes and
    character count to enable cost tracking and billing transparency.

    The function supports all Polly output formats and engines, providing
    flexibility for different use cases from telephony (PCM) to web streaming
    (ogg_vorbis) to general purpose (mp3).

    Args:
        client: boto3 Polly client instance
        text: Plain text or SSML markup to synthesize
        voice_id: Polly voice ID (e.g., 'Joanna', 'Matthew')
        output_format: Audio format ('mp3', 'ogg_vorbis', 'pcm')
        engine: Voice engine ('standard', 'neural', 'generative', 'long-form')
        text_type: Input type ('text' or 'ssml')
        sample_rate: Optional sample rate (e.g., '22050', '24000' for mp3)

    Returns:
        Tuple of (audio_bytes, character_count) for playback and billing

    Raises:
        ValueError: If text exceeds engine-specific character limits
        Exception: If Polly API call fails

    Example:
        >>> client = get_polly_client()
        >>> audio, chars = synthesize_audio(client, "Hello world", "Joanna")
        >>> print(f"Synthesized {chars} characters")
    """
    # Validate text length based on engine
    # WHY: Fail fast with clear error rather than cryptic API error
    max_chars = 100000 if engine == "long-form" else (6000 if text_type == "ssml" else 3000)

    if len(text) > max_chars:
        raise ValueError(
            f"Text length ({len(text)}) exceeds {engine} engine limit ({max_chars} chars).\n\n"
            f"Solutions:\n"
            f"  1. Split text into chunks under {max_chars} characters\n"
            f"  2. Use 'long-form' engine for extended content (100K char limit)\n"
            f"  3. Process content in batches with multiple API calls"
        )

    try:
        # Build synthesis parameters
        params: dict[str, Any] = {
            "Text": text,
            "OutputFormat": output_format,
            "VoiceId": voice_id,
            "Engine": engine,
            "TextType": text_type,
        }

        # Add sample rate if specified
        if sample_rate:
            params["SampleRate"] = sample_rate

        # Call Polly API
        response = client.synthesize_speech(**params)

        # Read audio stream from response
        # WHY: Stream directly to memory for low latency
        audio_bytes = response["AudioStream"].read()

        # Get character count for cost tracking
        char_count = response.get("RequestCharacters", len(text))

        return audio_bytes, char_count

    except Exception as e:
        # WHY: Wrap boto3 errors with context about the operation
        raise Exception(
            f"Speech synthesis failed: {e}\n\n"
            f"Parameters: voice={voice_id}, engine={engine}, format={output_format}\n"
            f"Verify voice supports the specified engine with: aws-polly-tts-tool list-voices"
        ) from e


def play_speech(
    client: Any,
    text: str,
    voice_id: str,
    output_format: str = "mp3",
    engine: str = "neural",
    text_type: str = "text",
) -> int:
    """
    Synthesize text and play through system speakers.

    Provides immediate audio feedback for interactive TTS use cases
    without requiring file management. Uses pydub for cross-platform audio
    playback, supporting macOS, Linux, and Windows.

    Args:
        client: boto3 Polly client instance
        text: Text to synthesize and play
        voice_id: Polly voice ID
        output_format: Audio format (default: mp3)
        engine: Voice engine (default: neural)
        text_type: Input type ('text' or 'ssml')

    Returns:
        Number of characters processed (for cost tracking)

    Raises:
        ValueError: If text is invalid or exceeds limits
        Exception: If synthesis or playback fails

    Example:
        >>> client = get_polly_client()
        >>> chars = play_speech(client, "Hello world", "Joanna")
    """
    # Synthesize audio
    audio_bytes, char_count = synthesize_audio(
        client, text, voice_id, output_format, engine, text_type
    )

    try:
        # Load audio from bytes without disk I/O
        # WHY: In-memory processing for lowest latency
        audio = AudioSegment.from_mp3(BytesIO(audio_bytes))

        # Play through speakers (suppress ffmpeg's verbose output)
        # WHY: ffmpeg/ffplay logs are noisy and not useful for end users
        # Use file descriptor redirection to suppress stderr at OS level
        stderr_fd = sys.stderr.fileno()
        with open(os.devnull, "w") as devnull:
            old_stderr_fd = os.dup(stderr_fd)
            try:
                os.dup2(devnull.fileno(), stderr_fd)
                play(audio)
            finally:
                os.dup2(old_stderr_fd, stderr_fd)
                os.close(old_stderr_fd)

        return char_count

    except Exception as e:
        raise Exception(f"Audio playback failed: {e}\n\nVerify audio system is configured.") from e


def save_speech(
    client: Any,
    text: str,
    voice_id: str,
    output_path: Path,
    output_format: str = "mp3",
    engine: str = "neural",
    text_type: str = "text",
) -> int:
    """
    Synthesize text and save audio to file.

    Enables caching synthesized audio for reuse, reducing API costs
    and latency for frequently played content. Creates parent directories
    automatically to simplify file management.

    Args:
        client: boto3 Polly client instance
        text: Text to synthesize
        voice_id: Polly voice ID
        output_path: File path to save audio
        output_format: Audio format (mp3, ogg_vorbis, pcm)
        engine: Voice engine
        text_type: Input type ('text' or 'ssml')

    Returns:
        Number of characters processed (for cost tracking)

    Raises:
        ValueError: If text is invalid or path is not writable
        Exception: If synthesis or file write fails

    Example:
        >>> from pathlib import Path
        >>> client = get_polly_client()
        >>> chars = save_speech(client, "Hello", "Joanna", Path("output.mp3"))
    """
    # Synthesize audio
    audio_bytes, char_count = synthesize_audio(
        client, text, voice_id, output_format, engine, text_type
    )

    try:
        # Create parent directories if needed
        # WHY: Simplify file management - don't require users to mkdir first
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write audio to file
        output_path.write_bytes(audio_bytes)

        return char_count

    except PermissionError:
        raise ValueError(
            f"Permission denied writing to: {output_path}\n\n"
            f"Solutions:\n"
            f"  1. Check file permissions: ls -la {output_path.parent}\n"
            f"  2. Choose a different output directory\n"
            f"  3. Run with appropriate permissions"
        )
    except Exception as e:
        raise Exception(f"Failed to save audio to {output_path}: {e}") from e


def read_from_stdin() -> str:
    """
    Read text from stdin with validation.

    Enables piping text from other commands and tools, supporting
    Unix-style composability. Validates that stdin is being piped (not
    interactive terminal) and that content is non-empty, providing clear
    error messages for common mistakes.

    Returns:
        Text read from stdin

    Raises:
        ValueError: If stdin is a terminal or input is empty

    Example:
        >>> # From command line:
        >>> # echo "Hello world" | aws-polly-tts-tool synthesize --stdin
    """
    # Check if stdin is being piped or is an interactive terminal
    # WHY: Fail fast with helpful message if user forgets to pipe input
    if sys.stdin.isatty():
        raise ValueError(
            "No input provided via stdin.\n\n"
            "Usage:\n"
            "  echo 'text' | aws-polly-tts-tool synthesize --stdin\n"
            "  cat file.txt | aws-polly-tts-tool synthesize --stdin --voice Matthew\n\n"
            "Or provide text as argument:\n"
            "  aws-polly-tts-tool synthesize 'your text here'"
        )

    # Read and strip whitespace
    text = sys.stdin.read().strip()

    # Validate non-empty
    if not text:
        raise ValueError(
            "Empty input received from stdin.\n\n"
            "Ensure piped content is not empty:\n"
            "  echo 'Hello world' | aws-polly-tts-tool synthesize --stdin"
        )

    return text
