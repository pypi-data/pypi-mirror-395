from guillotina import configure
from guillotina.content import Folder
from guillotina.content import Item
from guillotina_nuclia.interfaces.chat import IChat
from guillotina_nuclia.interfaces.chat import IChats


@configure.contenttype(
    type_name="Chats",
    schema=IChats,
    behaviors=["guillotina.behaviors.dublincore.IDublinCore"],
    allowed_types=["Chat"],
    globally_addable=False,
)
class Chats(Folder):
    pass


@configure.contenttype(
    type_name="Chat",
    schema=IChat,
    add_permission="guillotina.AddContent",
    behaviors=["guillotina.behaviors.dublincore.IDublinCore"],
    globally_addable=False,
)
class Chat(Item):
    pass
