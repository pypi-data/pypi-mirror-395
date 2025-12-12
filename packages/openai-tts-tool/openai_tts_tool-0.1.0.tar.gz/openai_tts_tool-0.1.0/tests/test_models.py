"""Tests for openai_tts_tool.models module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import pytest

from openai_tts_tool.models import (
    DEFAULT_MODEL,
    MODELS,
    get_model_info,
    list_models,
    validate_model,
)


def test_validate_model_valid() -> None:
    """Test validate_model with valid model names."""
    result = validate_model("tts-1")
    assert result == "tts-1"

    result = validate_model("TTS-1")
    assert result == "tts-1"

    result = validate_model("tts-1-hd")
    assert result == "tts-1-hd"


def test_validate_model_invalid() -> None:
    """Test validate_model with invalid model name."""
    with pytest.raises(ValueError, match="Unsupported model: 'invalid-model'"):
        validate_model("invalid-model")


def test_validate_model_empty() -> None:
    """Test validate_model with empty string."""
    with pytest.raises(ValueError, match="Model name cannot be empty"):
        validate_model("")


def test_validate_model_whitespace() -> None:
    """Test validate_model with whitespace only."""
    with pytest.raises(ValueError, match="Unsupported model: '   '"):
        validate_model("   ")


def test_list_models() -> None:
    """Test list_models returns all models with information."""
    models = list_models()
    assert len(models) == len(MODELS)

    # Check that it's a list of dictionaries
    assert all(isinstance(model, dict) for model in models)

    # Check that each model has required fields
    for model in models:
        assert "name" in model
        assert "quality" in model
        assert "latency" in model
        assert "description" in model
        assert "speed" in model
        assert model["name"] in MODELS
        assert model == MODELS[model["name"]]


def test_list_models_contains_default() -> None:
    """Test that list_models contains the default model."""
    models = list_models()
    model_names = [model["name"] for model in models]
    assert DEFAULT_MODEL in model_names


def test_get_model_info_valid() -> None:
    """Test get_model_info with valid model."""
    info = get_model_info("tts-1")
    assert info == MODELS["tts-1"]

    info = get_model_info("TTS-1")
    assert info == MODELS["tts-1"]


def test_get_model_info_invalid() -> None:
    """Test get_model_info with invalid model."""
    result = get_model_info("invalid-model")
    assert result is None


def test_get_model_info_empty() -> None:
    """Test get_model_info with empty string."""
    result = get_model_info("")
    assert result is None


def test_get_model_info_copy() -> None:
    """Test that get_model_info returns a copy, not reference."""
    info = get_model_info("tts-1")
    info["test"] = "modified"

    # Original should be unchanged
    original = get_model_info("tts-1")
    assert "test" not in original


def test_models_constants() -> None:
    """Test that models constants are properly defined."""
    assert isinstance(MODELS, dict)
    assert len(MODELS) > 0
    assert isinstance(DEFAULT_MODEL, str)
    assert DEFAULT_MODEL in MODELS

    # Check that all models have required fields
    for model_name, model_info in MODELS.items():
        assert isinstance(model_name, str)
        assert isinstance(model_info, dict)

        required_fields = ["name", "quality", "latency", "description", "speed"]
        for field in required_fields:
            assert field in model_info
            assert isinstance(model_info[field], str)
            assert len(model_info[field].strip()) > 0


def test_model_names_lowercase() -> None:
    """Test that all model names are lowercase."""
    for model_name in MODELS.keys():
        assert model_name == model_name.lower()


def test_validate_model_case_insensitive() -> None:
    """Test that validate_model works with different cases."""
    test_cases = ["TTS-1", "Tts-1", "tTS-1", "tts-1"]
    for case in test_cases:
        result = validate_model(case)
        assert result == "tts-1"


def test_list_models_immutability() -> None:
    """Test that list_models doesn't modify internal state."""
    models1 = list_models()
    models2 = list_models()
    assert models1 == models2

    # Modify returned list and ensure original is unchanged
    models1.append({"name": "fake-model", "quality": "fake"})
    models3 = list_models()
    assert len(models3) == len(MODELS)
    assert "fake-model" not in [model["name"] for model in models3]


def test_model_info_structure() -> None:
    """Test that model info has expected structure and values."""
    for model_name, model_info in MODELS.items():
        # Check that name matches the key
        assert model_info["name"] == model_name

        # Check that quality has expected values
        assert model_info["quality"] in ["standard", "high"]

        # Check that latency has expected values
        assert model_info["latency"] in ["low", "higher"]

        # Check that speed has expected values
        assert model_info["speed"] in ["fast", "slow"]


def test_tts1_model_info() -> None:
    """Test specific characteristics of tts-1 model."""
    tts1_info = MODELS["tts-1"]
    assert tts1_info["quality"] == "standard"
    assert tts1_info["latency"] == "low"
    assert tts1_info["speed"] == "fast"


def test_tts1_hd_model_info() -> None:
    """Test specific characteristics of tts-1-hd model."""
    tts1_hd_info = MODELS["tts-1-hd"]
    assert tts1_hd_info["quality"] == "high"
    assert tts1_hd_info["latency"] == "higher"
    assert tts1_hd_info["speed"] == "slow"
