import asyncio
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, Field

from contextual.graph.components.extractor_schema import SchemaExtractor

from ...models import FilterSchema, ModelSchemaExtractor, State
from .base import BaseNode


class ExtractorNode(BaseNode):
    """Extracts structured data from text using a extractor_schema and an LLM.

    This node orchestrates a two-step process:
    1. Fetches and parses a specific extractor_schema definition via its extractor.
    2. Uses the parsed extractor_schema to instruct an LLM service to extract data
       from the input text.

    Attributes:
        llm_service: The language model service client for extraction.
        schema_extractor: The component responsible for retrieving the extractor_schema.
    """

    llm_service: Any = Field(..., description="The language model service client.")

    schema_extractor: SchemaExtractor = Field(
        ..., description="The service component to fetch extractor_schema definitions."
    )

    def _get_parsed_schema(
        self, model_schema: Optional[BaseModel | Type[BaseModel] | FilterSchema]
    ) -> Type[BaseModel]:
        """Fetches the extractor_schema and parses it into a usable Pydantic model.

        Returns:
            The dynamically generated Pydantic model class.

        Raises:
            MongoDBCollectionNotFoundException: If the extractor_schema ID is not found.
            ValidationError: If the retrieved extractor_schema data is not valid.
            AttributeError: If the extractor_schema object is invalid.
        """
        schema_descriptor: ModelSchemaExtractor = asyncio.run(
            self.schema_extractor.extract(filters=model_schema)
        )

        pydantic_class = schema_descriptor.as_pydantic_model()
        return pydantic_class

    def _extract_data_with_llm(
        self,
        pydantic_class: Type[BaseModel],
        text_input: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Invokes the LLM service with the parsed extractor_schema to extract data.

        Args:
            pydantic_class: The Pydantic model to structure the output.
            text_input: The input text to process.
            config: Optional runtime configuration for the LLM.

        Returns:
            The structured data extracted by the LLM.

        Raises:
            DataExtractionError: If the LLM service fails during extraction.
        """
        try:
            structured_llm = self.llm_service.with_structured_output(pydantic_class)
            extracted_data = structured_llm.invoke(text_input, config=config)
            return extracted_data
        except Exception as e:
            raise Exception(f"LLM service failed to extract data: {e}") from e

    def process(self, state: State, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Synchronously fetches a extractor_schema and extracts data from the state.

        Args:
            state: The input State object, expected to contain `text`.
            config: Optional runtime configuration passed by the graph.

        Returns:
            A dictionary containing the `data_extracted` field.
        """
        pydantic_class = self._get_parsed_schema(state.model_schema)
        extracted_data = self._extract_data_with_llm(pydantic_class, state.text, config)
        return {"data_extracted": extracted_data, "model_schema": pydantic_class}
