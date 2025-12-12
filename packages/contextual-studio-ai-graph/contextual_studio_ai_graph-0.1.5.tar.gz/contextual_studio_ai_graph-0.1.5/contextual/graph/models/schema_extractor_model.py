import datetime
from typing import Any, Dict, Optional, Tuple, Type

from pydantic import BaseModel, Field, create_model


class SchemaField(BaseModel):
    """Represents a single field in a extractor_schema definition.

    Attributes:
        name (str): The name of the field.
        required (bool): Indicates whether the field is mandatory.
        field_type (str): The data type of the field. Defaults to "string".
    """

    name: str
    required: bool
    field_type: str = "string"
    description: str


class ModelSchemaExtractor(BaseModel):
    """Represents the overall extractor_schema structure with associated fields and business rules.

    Attributes:
        _id (str): Unique identifier of the extractor_schema.
        name (str): Human-readable name of the extractor_schema.
        fields (Tuple[SchemaField, ...]): A tuple of field definitions.
    """

    _id: str
    name: str
    fields: Tuple[SchemaField, ...]

    @classmethod
    def create(cls, id_schema: str, raw_data: Dict[str, Any]) -> "ModelSchemaExtractor":
        """Creates a ModelSchemaExtractor instance from raw dictionary data.

        This version is adapted to parse a 'fields' key that is a list
        of field dictionaries.

        Args:
            id_schema (str): Unique identifier of the extractor_schema.
            raw_data (dict): Raw extractor_schema data containing fields and business rules.

        Returns:
            ModelSchemaExtractor: A populated instance based on the input data.
        """

        fields_data_list = raw_data.get("fields", [])
        parsed_fields = [SchemaField(**field_data) for field_data in fields_data_list]

        # Convert id_schema to string if it's an ObjectId
        schema_id = str(id_schema) if id_schema else "unknown"

        return cls(
            _id=schema_id,
            name=raw_data.get("name", "Unnamed Schema"),
            fields=tuple(parsed_fields),
        )

    @property
    def all_fields(self) -> Tuple[str, ...]:
        """Returns a tuple of all field names in the extractor_schema.

        Combines both required and optional fields.

        Returns:
            Tuple[str, ...]: All field names defined in the extractor_schema.
        """
        return tuple(f.name for f in self.fields)

    def as_pydantic_model(self) -> Type[BaseModel]:
        """Dynamically generates a Pydantic BaseModel class from extractor_schema fields.

        This method iterates over the `fields` attribute of the instance
        and uses Pydantic's `create_model` utility to build a new `BaseModel`
        class on the fly. This class is compatible with LLM "structured output"
        or "function calling" features.

        Field descriptions are included, and a hint for the expected date
        format ("YYYY-MM-DD") is appended to 'date' type fields to guide
        the language model's output and ensure successful validation.

        Returns:
            Type[BaseModel]: A dynamically created Pydantic BaseModel class.

        Raises:
            ValueError: If the resulting model name is invalid after sanitization.
        """
        type_map: Dict[str, Any] = {
            "string": str,
            "number": float,
            "date": datetime.date,
            "boolean": bool,
        }

        field_definitions: Dict[str, Any] = {}

        for field in self.fields:
            py_type = type_map.get(field.field_type, Any)
            field_description = field.description

            if field.field_type == "date":
                field_description = f"{field_description}. Expected format: YYYY-MM-DD."

            if field.required:
                field_definitions[field.name] = (py_type, Field(..., description=field_description))
            else:
                field_definitions[field.name] = (
                    Optional[py_type],
                    Field(default=None, description=field_description),
                )

        safe_name = self.name or "UnnamedModel"

        if not (safe_name[0].isalpha() or safe_name[0] == "_"):
            safe_name = f"Model_{safe_name}"

        # Replace common special characters with underscores
        safe_name = safe_name.replace("-", "_").replace(".", "_").replace(":", "_")
        safe_name = safe_name.replace(" ", "_").replace(",", "_").replace("y", "_")

        # Remove any remaining non-identifier characters
        safe_name = "".join(c if c.isalnum() or c == "_" else "_" for c in safe_name)

        if not safe_name.isidentifier():
            raise ValueError(
                f"Failed to create a valid model name from '{self.name}'. "
                f"Resulted in '{safe_name}'."
            )

        DynamicModel = create_model(safe_name, **field_definitions, __base__=BaseModel)

        return DynamicModel
