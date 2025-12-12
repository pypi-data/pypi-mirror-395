from guillotina import schema
from guillotina.interfaces import IFolder
from guillotina.interfaces import IItem


class IChats(IFolder):
    pass


MESSAGE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "author": {"type": "string"},
        "text": {"type": "string"},
    },
    "required": ["text", "author"],
}


class IChat(IItem):
    history = schema.List(
        title="Chat history",
        value_type=schema.JSONField(schema=MESSAGE_SCHEMA),
        required=False,
        default=[],
        missing_value=[],
        defaultFactory=list,
    )

    responses = schema.List(
        title="Responses",
        value_type=schema.TextLine(),
        required=False,
        default=[],
        missing_value=[],
        defaultFactory=list,
    )

    context = schema.List(
        title="Context",
        value_type=schema.TextLine(),
        required=False,
        default=[],
        missing_value=[],
        defaultFactory=list,
    )
