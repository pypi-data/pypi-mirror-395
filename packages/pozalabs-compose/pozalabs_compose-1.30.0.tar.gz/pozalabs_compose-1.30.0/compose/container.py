from __future__ import annotations

import json
from typing import Any, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict
from typing_extensions import Self

from . import field, types

type AbstractSetIntStr = set[int] | set[str]
type MappingIntStrAny = dict[int, Any] | dict[str, Any]

type IncEx = set[int] | set[str] | dict[int, Any] | dict[str, Any] | None
Model = TypeVar("Model", bound=PydanticBaseModel)


class BaseModel(PydanticBaseModel):
    @classmethod
    def from_model(cls, model: BaseModel) -> Self:
        return cls.model_validate(model.model_dump())

    def json(
        self,
        indent: int | None = None,
        include: IncEx = None,
        exclude: IncEx = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
    ) -> str:
        return self.model_dump_json(
            indent=indent,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=True,
        )

    def dict(
        self,
        include: IncEx = None,
        exclude: IncEx = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
    ):
        return self.model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=True,
        )

    def copy(
        self,
        *,
        include: AbstractSetIntStr | MappingIntStrAny | None = None,
        exclude: AbstractSetIntStr | MappingIntStrAny | None = None,
        update: dict[str, Any] | None = None,
        deep: bool = False,
        validate: bool = False,
    ) -> Model:
        result = super().model_copy(update=update, deep=deep)
        if not validate:
            return result

        return self.__class__.model_validate(result.model_dump_json(warnings=False))

    def model_copy(
        self,
        *,
        update: dict[str, Any] | None = None,
        deep: bool = False,
        validate: bool = False,
    ) -> Self:
        result = super().model_copy(update=update, deep=deep)
        if not validate:
            return result

        return self.__class__.model_validate(result.model_dump_json(warnings=False))

    def encode(
        self,
        *,
        indent: int | None = None,
        include: IncEx = None,
        exclude: IncEx = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
    ) -> dict[str, Any]:
        return json.loads(
            self.model_dump_json(
                indent=indent,
                include=include,
                exclude=exclude,
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                round_trip=round_trip,
                warnings=warnings,
            )
        )

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
    )


class TimeStampedModel(BaseModel):
    created_at: types.DateTime = field.DateTimeField()
    updated_at: types.DateTime = field.DateTimeField()
