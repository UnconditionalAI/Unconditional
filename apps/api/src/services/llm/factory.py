"""LLM service factory.

Provides centralized model configuration for pydantic-ai Agents.
Returns model name that can be passed directly to Agent() constructor.
"""

import os


def get_llm_model() -> str:
    """
    Get configured LLM model identifier.

    Returns:
        Model identifier string in pydantic-ai format (e.g., "openai:gpt-5.1")

    Safety reasoning:
        - Single point of model configuration
        - Environment-driven model selection
        - pydantic-ai handles all provider-specific logic
        - Supports all pydantic-ai model providers

    Supported providers (via pydantic-ai):
        - openai: OpenAI models (gpt-5.1, gpt-4, etc.)
        - anthropic: Anthropic models (claude-sonnet-4-0, etc.)
        - gemini: Google Gemini models
        - vertexai: Google Vertex AI
        - groq: Groq models
        - mistral: Mistral AI models
        - ollama: Local Ollama models
        - And many more...

    Usage:
        ```python
        from pydantic_ai import Agent
        from services.llm.factory import get_llm_model

        agent = Agent(get_llm_model(), instructions="...")
        ```
    """
    # Get provider and model from environment
    # Format: "provider:model-name" (e.g., "openai:gpt-5.1")
    model = os.getenv("LLM_MODEL", "openai:gpt-5.1")

    # Legacy support: if LLM_PROVIDER is set, construct model string
    provider = os.getenv("LLM_PROVIDER")
    if provider:
        provider = provider.lower()
        if provider == "openai":
            model = "openai:gpt-5.1"
        elif provider == "anthropic":
            model = "anthropic:claude-sonnet-4-0"
        # Add more legacy provider mappings as needed

    return model
