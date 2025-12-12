import os
from typing import Any, Dict

from langchain_google_genai import ChatGoogleGenerativeAI

from ...exceptions.factories.llm_services.llm_service_exceptions import (
    LLMServiceConnectionException,
)


class GoogleLLMFactory:
    """Concrete factory for creating Google Generative AI LLM services using ChatGoogleGenerativeAI."""

    @staticmethod
    def create(**kwargs: Dict[Any, Any]) -> ChatGoogleGenerativeAI:
        """Creates an instance of ChatGoogleGenerativeAI.

        Checks for the 'GOOGLE_API_KEY' environment variable and uses
        default model parameters, which can be overridden by kwargs.
        Args:
            **kwargs (Dict[Any, Any]): Optional keyword arguments for customizing the extraction workflow.

        Returns:
            ChatGoogleGenerativeAI: An instance of the Google LLM client.

        Raises:
            ValueError: If the GOOGLE_API_KEY environment variable is not set.
        """
        if "GOOGLE_API_KEY" not in os.environ:
            raise LLMServiceConnectionException("GOOGLE_API_KEY environment variable not set.")

        default_config = {
            "model": "gemini-2.5-flash",
            "temperature": 0,
            "max_tokens": None,
            "timeout": None,
            "max_retries": 2,
        }
        final_config = {**default_config, **kwargs}
        return ChatGoogleGenerativeAI(**final_config)
