from typing import Any, ClassVar

from . import container, field, types


class Entity(container.TimeStampedModel):
    id: types.PyObjectId = field.IdField(default_factory=types.PyObjectId)

    updatable_fields: ClassVar[set[str]] = set()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)

        fields = set(cls.model_fields.keys())
        if diff := set(cls.updatable_fields) - fields:
            raise ValueError(f"`updatable_fields` must be subset of {fields}, but got {diff}")

    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if key not in self.updatable_fields:
                continue

            setattr(self, key, value)
