from collections.abc import Callable
from typing import Any

import bson
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class PyObjectId(bson.ObjectId):
    @classmethod
    def validate(
        cls, v: bson.ObjectId | bytes, _: core_schema.ValidationInfo = None
    ) -> bson.ObjectId:
        return cls._validate(v)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.with_info_plain_validator_function(
            cls.validate, serialization=core_schema.to_string_ser_schema()
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        schema: core_schema.CoreSchema,
        handler: Callable[[Any], core_schema.CoreSchema],
    ) -> CoreSchema:
        return dict(type="string")

    @classmethod
    def _validate(cls, v: bson.ObjectId | bytes) -> bson.ObjectId:
        if not bson.ObjectId.is_valid(v):
            raise ValueError("Invalid object id")
        return bson.ObjectId(v)
