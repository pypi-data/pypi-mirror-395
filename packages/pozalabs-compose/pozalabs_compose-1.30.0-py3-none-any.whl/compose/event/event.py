from .. import container, field, types


class Event(container.BaseModel):
    id: types.PyObjectId = field.IdField(default_factory=types.PyObjectId)
    published_at: types.DateTime = field.DateTimeField()
