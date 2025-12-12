from guillotina import configure
from guillotina.addons import Addon
from guillotina.content import create_content_in_container
from guillotina.event import notify
from guillotina.events import ObjectAddedEvent
from guillotina.events import ObjectRemovedEvent
from guillotina.utils import get_authenticated_user_id


@configure.addon(name="nuclia", title="Nuclia addon")
class NucliaAddon(Addon):
    @classmethod
    async def install(self, site, request):
        user = get_authenticated_user_id()
        chats_folder = await create_content_in_container(
            site,
            "Chats",
            "chats",
            creators=(user,),
            title="Chats folder",
            check_constraints=False,
        )
        await notify(ObjectAddedEvent(chats_folder))

    @classmethod
    async def uninstall(self, site, request):
        if await site.async_contains("chats"):
            chats_folder = await site.async_get("chats")
            await site.async_del("chats")
            await notify(ObjectRemovedEvent(chats_folder))
