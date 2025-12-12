"""
Voice management for AWS Polly TTS.

This module provides dynamic voice discovery and selection to ensure
users always have access to the latest Polly voices without manual updates.
The VoiceManager fetches voice metadata directly from the Polly API, enabling
filtering by engine, language, and gender for flexible voice selection.

This approach prioritizes real-time accuracy over caching, ensuring
compatibility with new voices as AWS releases them without requiring tool
updates.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class VoiceProfile:
    """
    AWS Polly voice profile with metadata.

    Type-safe representation of voice information that includes all
    relevant attributes for voice selection and filtering. This structure
    makes voice data easy to work with in both CLI and library contexts.

    Attributes:
        voice_id: AWS Polly voice identifier (e.g., 'Joanna')
        name: Display name of the voice
        gender: Voice gender ('Female', 'Male', 'Neutral')
        language_code: ISO language code (e.g., 'en-US')
        language_name: Human-readable language name (e.g., 'US English')
        supported_engines: List of compatible engines
        description: Optional voice description or characteristics
    """

    voice_id: str
    name: str
    gender: str
    language_code: str
    language_name: str
    supported_engines: list[str]
    description: str = ""


class VoiceManager:
    """
    Manages AWS Polly voice discovery and selection.

    Centralizes voice lookup logic to provide consistent voice resolution
    across CLI commands and library usage. By fetching voices dynamically from
    the API, this class ensures users can access newly released voices without
    tool updates.

    The class maintains a session-based cache to avoid redundant API calls
    within a single execution, balancing performance with real-time accuracy.

    Attributes:
        client: boto3 Polly client for API calls
        _voices: Cached voice profiles (None until first fetch)
    """

    def __init__(self, client: Any):
        """
        Initialize VoiceManager with Polly client.

        WHY: Requires client to be provided externally for better testability
        and to allow CLI commands to control client initialization with
        region selection.

        Args:
            client: boto3 Polly client instance
        """
        self.client = client
        self._voices: dict[str, VoiceProfile] | None = None

    def _load_voices(self) -> dict[str, VoiceProfile]:
        """
        Fetch voices from Polly API.

        WHY: Makes a single API call to retrieve all available voices,
        converting AWS response format into our VoiceProfile structure.
        This normalization simplifies voice filtering and display logic.

        Returns:
            Dictionary mapping lowercase voice names to VoiceProfile objects

        Raises:
            Exception: If Polly API call fails
        """
        try:
            # Call Polly API to get all voices
            # WHY: Single call gets all voices across all languages/engines
            response = self.client.describe_voices()

            voices: dict[str, VoiceProfile] = {}

            for voice_data in response["Voices"]:
                # Extract voice attributes
                voice_id = voice_data["Id"]
                name = voice_data["Name"]

                # Store with lowercase key for case-insensitive lookup
                # WHY: Users shouldn't have to remember exact capitalization
                key = name.lower()

                voices[key] = VoiceProfile(
                    voice_id=voice_id,
                    name=name,
                    gender=voice_data.get("Gender", "Unknown"),
                    language_code=voice_data.get("LanguageCode", ""),
                    language_name=voice_data.get("LanguageName", ""),
                    supported_engines=voice_data.get("SupportedEngines", []),
                )

            return voices

        except Exception as e:
            raise Exception(f"Failed to fetch voices from Polly API: {e}") from e

    def get_voice_id(self, voice_name: str) -> str:
        """
        Get voice ID from voice name (case-insensitive).

        WHY: Provides flexible voice resolution by accepting either friendly
        names or direct voice IDs. Case-insensitive matching improves UX by
        not requiring exact capitalization. Falls back to treating input as
        voice ID if not found in voice list.

        Args:
            voice_name: Voice name or ID (case-insensitive)

        Returns:
            AWS Polly voice ID

        Raises:
            ValueError: If voice name not found and doesn't look like voice ID

        Example:
            >>> manager = VoiceManager(client)
            >>> voice_id = manager.get_voice_id("joanna")  # Case-insensitive
            >>> print(voice_id)  # 'Joanna'
        """
        # Load voices if not cached
        if self._voices is None:
            self._voices = self._load_voices()

        # Try case-insensitive name lookup
        normalized_name = voice_name.lower().strip()
        profile = self._voices.get(normalized_name)

        if profile:
            return profile.voice_id

        # Check if it's already a voice ID (AWS voice names match IDs)
        # WHY: Allow users to provide voice IDs directly for programmatic use
        for voice_profile in self._voices.values():
            if voice_profile.voice_id == voice_name:
                return voice_name

        # Voice not found - provide helpful error with suggestions
        available_sample = ", ".join(sorted(list(self._voices.keys())[:10]))
        raise ValueError(
            f"Voice '{voice_name}' not found.\n\n"
            f"Sample voices: {available_sample}...\n\n"
            f"Use 'aws-polly-tts-tool list-voices' to see all {len(self._voices)} available voices."
        )

    def list_voices(
        self,
        engine: str | None = None,
        language: str | None = None,
        gender: str | None = None,
    ) -> list[tuple[str, VoiceProfile]]:
        """
        List all voices with optional filtering.

        WHY: Enables voice discovery with flexible filtering by engine,
        language, or gender. This helps users find appropriate voices for
        their specific use case without manually reviewing all 60+ options.

        Args:
            engine: Filter by engine ('standard', 'neural', 'generative', 'long-form')
            language: Filter by language code (e.g., 'en-US') - partial match
            gender: Filter by gender ('Female', 'Male')

        Returns:
            List of (voice_name, VoiceProfile) tuples sorted by name

        Example:
            >>> manager = VoiceManager(client)
            >>> # Get all neural US English female voices
            >>> voices = manager.list_voices(
            ...     engine='neural',
            ...     language='en-US',
            ...     gender='Female'
            ... )
        """
        # Load voices if not cached
        if self._voices is None:
            self._voices = self._load_voices()

        # Apply filters
        filtered_voices = []

        for name, profile in self._voices.items():
            # Filter by engine
            if engine and engine.lower() not in [e.lower() for e in profile.supported_engines]:
                continue

            # Filter by language (partial match for flexibility)
            # WHY: Allow matching 'en' to get all English variants
            if language and not profile.language_code.lower().startswith(language.lower()):
                continue

            # Filter by gender (case-insensitive)
            if gender and profile.gender.lower() != gender.lower():
                continue

            filtered_voices.append((name, profile))

        # Sort by voice name for consistent display
        return sorted(filtered_voices, key=lambda x: x[0])

    def refresh_voices(self) -> None:
        """
        Force refresh of voice cache from API.

        WHY: Allows users to explicitly refresh voice data if AWS releases
        new voices mid-session or if they suspect stale data.

        Example:
            >>> manager = VoiceManager(client)
            >>> manager.refresh_voices()  # Force API call
        """
        self._voices = self._load_voices()
