"""
OpenAI client functionality for TTS operations.

This module provides a centralized way to create and configure OpenAI clients
with proper error handling and credential validation.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import os

from openai import APIStatusError, OpenAI, OpenAIError

from openai_tts_tool.logging_config import get_logger

logger = get_logger(__name__)


def get_openai_client() -> OpenAI:
    """
    Create and return an OpenAI client instance.

    Uses the OPENAI_API_KEY environment variable for authentication.

    Returns:
        OpenAI: Configured OpenAI client instance

    Raises:
        EnvironmentError: If OPENAI_API_KEY is not set
        ValueError: If OPENAI_API_KEY is empty or invalid format
        APIStatusError: If API key authentication fails
        OpenAIError: For other OpenAI-related errors
    """
    logger.debug("Creating OpenAI client")
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key is None:
        logger.error("OPENAI_API_KEY environment variable is not set")
        raise OSError(
            "OPENAI_API_KEY environment variable is not set. "
            "Please set it using: export OPENAI_API_KEY='your-api-key-here' "
            "or add it to your shell profile."
        )

    if not api_key.strip():
        logger.error("OPENAI_API_KEY is set but empty")
        raise ValueError("OPENAI_API_KEY is set but empty. Please provide a valid OpenAI API key.")

    if not api_key.startswith("sk-"):
        logger.error("OPENAI_API_KEY format is invalid: does not start with 'sk-'")
        raise ValueError(
            "OPENAI_API_KEY format is invalid. "
            "OpenAI API keys typically start with 'sk-'. "
            "Please verify your API key."
        )

    try:
        client = OpenAI(api_key=api_key)
        logger.debug("OpenAI client created successfully")
        return client
    except APIStatusError as e:
        logger.debug("OpenAI API authentication error: %s", e)
        raise APIStatusError(
            message=f"Failed to authenticate with OpenAI using the provided API key: {e}. "
            "Please verify your API key is correct and active.",
            response=e.response,
            body=e.body,
        ) from e
    except OpenAIError as e:
        logger.debug("OpenAI client creation error: %s", e)
        raise OpenAIError(
            f"Failed to create OpenAI client: {e}. "
            "Please check your network connection and API key."
        ) from e
    except Exception as e:
        logger.debug("Unexpected error creating OpenAI client: %s", e)
        logger.debug("Full traceback:", exc_info=True)
        raise OpenAIError(
            f"Unexpected error creating OpenAI client: {e}. "
            "Please contact support if this persists."
        ) from e


def test_credentials() -> bool:
    """
    Test if the OpenAI API credentials are valid and working.

    Makes a lightweight API call to verify the credentials.

    Returns:
        bool: True if credentials are valid, False otherwise

    Raises:
        EnvironmentError: If OPENAI_API_KEY is not set
        ValueError: If OPENAI_API_KEY format is invalid
        APIStatusError: If API key authentication fails
        OpenAIError: If API call fails for other reasons
    """
    try:
        client = get_openai_client()

        # Make a simple API call to test credentials
        # Using models.list() as it's a lightweight read operation
        client.models.list()

        # If we get here without an exception, credentials are valid
        return True

    except APIStatusError as e:
        raise APIStatusError(
            message=f"OpenAI API credentials are invalid or inactive: {e}. "
            "Please check your API key in the OpenAI dashboard.",
            response=e.response,
            body=e.body,
        ) from e
    except OpenAIError as e:
        raise OpenAIError(
            f"Failed to test OpenAI credentials: {e}. "
            "Please check your network connection and try again."
        ) from e
    except Exception as e:
        raise OpenAIError(
            f"Unexpected error testing OpenAI credentials: {e}. "
            "Please contact support if this persists."
        ) from e


# Prevent pytest from collecting test_credentials as a test function
# mypy doesn't understand pytest's __test__ attribute
test_credentials.__test__ = False  # type: ignore[attr-defined]


def get_api_info() -> dict[str, str | int | list[str]]:
    """
    Get information about the OpenAI API and available TTS models.

    Returns:
        dict: Information about available TTS models and API limits

    Raises:
        OpenAIError: If unable to retrieve API information
    """
    try:
        client = get_openai_client()

        # Get available models
        models = client.models.list()

        # Filter for TTS models
        tts_models = [model.id for model in models.data if "tts" in model.id.lower()]

        return {
            "available_tts_models": sorted(tts_models),
            "api_status": "connected",
            "models_count": len(models.data),
        }

    except OpenAIError as e:
        raise OpenAIError(f"Failed to retrieve OpenAI API information: {e}") from e
    except Exception as e:
        raise OpenAIError(f"Unexpected error retrieving API information: {e}") from e
