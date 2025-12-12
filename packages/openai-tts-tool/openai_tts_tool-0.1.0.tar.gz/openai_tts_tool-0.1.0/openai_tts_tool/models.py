"""
OpenAI TTS model definitions and validation utilities.

This module provides constants and functions for working with OpenAI's
text-to-speech models, including validation and model information.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

# Model definitions with their characteristics
MODELS: dict[str, dict[str, str]] = {
    "tts-1": {
        "name": "tts-1",
        "quality": "standard",
        "latency": "low",
        "description": "Standard quality model with faster response times",
        "speed": "fast",
    },
    "tts-1-hd": {
        "name": "tts-1-hd",
        "quality": "high",
        "latency": "higher",
        "description": "High definition model with better audio quality",
        "speed": "slow",
    },
}

# Default model for the CLI
DEFAULT_MODEL: str = "tts-1"


def validate_model(model: str) -> str:
    """
    Validate and normalize a model name.

    Args:
        model: The model name to validate

    Returns:
        The normalized model name

    Raises:
        ValueError: If the model is not supported

    Examples:
        >>> validate_model("TTS-1")
        'tts-1'
        >>> validate_model("tts-1-hd")
        'tts-1-hd'
    """
    if not model:
        raise ValueError("Model name cannot be empty")

    # Normalize to lowercase for case-insensitive comparison
    normalized_model = model.lower()

    if normalized_model not in MODELS:
        available_models = ", ".join(MODELS.keys())
        raise ValueError(f"Unsupported model: '{model}'. Available models: {available_models}")

    return normalized_model


def list_models() -> list[dict[str, str]]:
    """
    Get information about all available TTS models.

    Returns:
        List of dictionaries containing model information

    Examples:
        >>> models = list_models()
        >>> len(models)
        2
        >>> models[0]["name"]
        'tts-1'
    """
    return [model_info.copy() for model_info in MODELS.values()]


def get_model_info(model: str) -> dict[str, str] | None:
    """
    Get information about a specific model.

    Args:
        model: The model name to get information for

    Returns:
        Dictionary with model information, or None if model not found

    Examples:
        >>> info = get_model_info("tts-1")
        >>> info["quality"]
        'standard'
        >>> get_model_info("invalid-model")
        None
    """
    try:
        normalized_model = validate_model(model)
        return MODELS[normalized_model].copy()
    except ValueError:
        return None
