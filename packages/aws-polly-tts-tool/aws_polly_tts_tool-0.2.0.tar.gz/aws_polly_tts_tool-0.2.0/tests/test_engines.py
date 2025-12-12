"""Tests for engines module (no pydub dependency)."""

from aws_polly_tts_tool.engines import get_engine_info, list_all_engines, validate_engine


def test_validate_engine() -> None:
    """Test engine validation."""
    assert validate_engine("neural") == "neural"
    assert validate_engine("NEURAL") == "neural"
    assert validate_engine("standard") == "standard"

    try:
        validate_engine("invalid")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid engine ID" in str(e)


def test_get_engine_info() -> None:
    """Test getting engine info."""
    info = get_engine_info("neural")
    assert info.name == "Neural"
    assert info.pricing_per_million == 16.00


def test_list_all_engines() -> None:
    """Test listing all engines."""
    engines = list_all_engines()
    assert len(engines) == 4
    assert all(isinstance(engine_id, str) for engine_id, _ in engines)
