# Copyright (c) 2025 Microsoft Corporation.
# Licensed under the MIT License

"""
Standalone embedding wrapper for nlweb-dataload.

Simplified version that doesn't depend on nlweb_core.
"""

from typing import Optional, List
import asyncio

from .config import CONFIG


async def get_embedding(
    text: str,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    timeout: int = 30
) -> List[float]:
    """
    Get embedding for the provided text using the specified provider and model.

    Args:
        text: The text to embed
        provider: Optional provider name, defaults to configured provider
        model: Optional model name, defaults to the provider's configured model
        timeout: Maximum time to wait for embedding response in seconds

    Returns:
        List of floats representing the embedding vector
    """
    provider = provider or CONFIG.embedding_provider

    if not provider:
        raise ValueError("No embedding provider configured")

    # Truncate text to 20k characters to avoid token limit issues
    MAX_CHARS = 20000
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    # Get provider config
    provider_config = CONFIG.get_embedding_config(provider)
    if not provider_config:
        raise ValueError(f"Missing configuration for embedding provider '{provider}'")

    # Use the provided model or fall back to the configured model
    model_id = model or provider_config.get('model')
    if not model_id:
        raise ValueError(f"No embedding model specified for provider '{provider}'")

    try:
        # Use config-driven dynamic import
        import_path = provider_config.get('import_path')
        class_name = provider_config.get('class_name')

        if not import_path or not class_name:
            raise ValueError(
                f"No import_path and class_name configured for embedding provider '{provider}'"
            )

        # Dynamic import
        module = __import__(import_path, fromlist=[class_name])
        embedding_callable = getattr(module, class_name)

        # Call the embedding function with timeout
        result = await asyncio.wait_for(
            embedding_callable(text, model=model_id),
            timeout=timeout
        )
        return result

    except (ImportError, AttributeError) as e:
        raise ValueError(f"Failed to load embedding provider '{provider}': {e}")
    except asyncio.TimeoutError:
        raise TimeoutError(f"Embedding request timed out after {timeout} seconds")
