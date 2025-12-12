from pydantic import ConfigDict

from .. import container, schema, types


class Command(container.BaseModel): ...


class UserCommand(Command):
    user_id: types.PyObjectId | None = None

    model_config = ConfigDict(json_schema_extra=schema.extra.schema_excludes("user_id"))
