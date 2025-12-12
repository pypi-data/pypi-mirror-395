from typing import Any, Dict

from loguru import logger
from pydantic import Field

from contextual.graph.factories.langgraph import ExtractorLangGraphFactory
from contextual.graph.models import FilterSchema, ModelDataExtractor, State

from .base import DataExtractor


class DataExtractorLG(DataExtractor):
    """Implementation of a data extractor that uses a prompt-driven graph-based workflow.

    This class extends the `DataExtractor` interface and utilizes a `GraphFactory`
    to extract structured information from raw text using a predefined extractor_schema.
    """

    graph_factory: ExtractorLangGraphFactory = Field(
        ..., description="Factory to build the graph-based extraction pipeline."
    )

    async def extract(
        self, text: str | None, model_schema: FilterSchema, **kwargs: Dict[Any, Any]
    ) -> ModelDataExtractor:
        """Extracts structured data from input text using a extractor_schema and prompt-driven graph.

        The method creates an extraction graph using the provided factory, applies it
        to the input text and extractor_schema, and returns structured extraction results.

        Args:
            text (str | None): Raw input text to be processed.
            **kwargs (Dict[Any, Any]): Optional keyword arguments for customizing the extraction workflow.

        Returns:
            ModelDataExtractor: Returning structured extraction results.
        """
        logger.info(
            f"DataExtractorLG.extract called - has_text: {text is not None}, kwargs: {list(kwargs.keys())}"
        )

        graph = self.graph_factory.build(state=State)
        file_path: str | None = kwargs.get("file_path")  # type: ignore[assignment]

        logger.info(
            f"Building initial state - text_length: {len(text) if text else 0}, file_path: {file_path}"
        )
        initial_state = State(
            text=text, model_schema=model_schema, file_path=file_path, data_extracted={}
        )

        logger.info("Invoking graph with initial state")
        output = await graph.ainvoke(initial_state)
        logger.info(f"Graph execution completed. Output type: {type(output)}")

        # Handle dict output
        if isinstance(output, dict):
            logger.info(f"Output is dict with keys: {list(output.keys())}")
            if "data_extracted" not in output:
                logger.error("Graph output missing data_extracted field")
                raise Exception("Graph output missing data_extracted field")
            logger.info(
                f"Returning ModelDataExtractor with data type: {type(output['data_extracted'])}"
            )
            return ModelDataExtractor(data=output["data_extracted"])

        # Handle State object
        if isinstance(output, State):
            logger.info(
                f"Output is State object. data_extracted type: {type(output.data_extracted)}"
            )
            if output.data_extracted is None:
                logger.error("State data_extracted field is None")
                raise ValueError("State data_extracted field is None")
            return ModelDataExtractor(data=output.data_extracted)

        # Invalid type
        logger.error(f"Invalid output type: {type(output).__name__}")
        raise TypeError(f"Expected State or dict, got {type(output).__name__}")
