from enum import Enum
from typing import get_args, get_origin
from pydantic import BaseModel, model_validator


class Model(BaseModel):
    model_config = {
        "json_encoders": {
            BaseModel: lambda v: v.model_dump()
        }
    }

    @model_validator(mode="before")
    @classmethod
    def self_heal(cls, data):
        def heal_enum(enum_class, value):
            if isinstance(value, enum_class):
                return value

            value_str = str(value).strip()

            # Direct init attempt
            try:
                return enum_class(value_str)
            except Exception:
                pass

            # Case-insensitive or partial match
            for enum_item in enum_class:
                enum_str = str(enum_item.value)
                if value_str.lower() == enum_str.lower():
                    return enum_item
                if value_str.lower().startswith(enum_str.lower()):
                    return enum_item

            raise ValueError(
                f"Value '{value}' is not a valid member of enum {enum_class.__name__}"
            )

        def process_value(field_type, value):
            if value is None:
                return value

            origin = get_origin(field_type)
            args = get_args(field_type)

            # Handle lists
            if origin is list and args:
                inner_type = args[0]
                if not isinstance(value, list):
                    value = [value]
                return [process_value(inner_type, v) for v in value]

            # Nested models
            if isinstance(value, dict) and hasattr(field_type, "model_fields"):
                return field_type.self_heal(value)

            if isinstance(value, BaseModel):
                return value

            # Enums
            if isinstance(field_type, type) and issubclass(field_type, Enum):
                return heal_enum(field_type, value)

            return value

        if isinstance(data, dict):
            healed = {}
            for field_name, value in data.items():
                field = cls.model_fields.get(field_name)
                if field is None:
                    healed[field_name] = value
                    continue
                healed[field_name] = process_value(field.annotation, value)
            return healed

        return data
