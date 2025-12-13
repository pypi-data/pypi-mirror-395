from typing import TYPE_CHECKING
from uuid import UUID

from slidge import LegacyContact, LegacyRoster
from slidge.util.types import Avatar
from slixmpp.exceptions import XMPPError

from .generated import signal

if TYPE_CHECKING:
    from .session import Session


class Contact(LegacyContact[str]):
    session: "Session"

    CORRECTION = True
    REACTIONS_SINGLE_EMOJI = True

    async def update_info(self, data: signal.Contact | None = None) -> None:
        """
        Set fields for contact based on data given, or if none was, as retrieved from Signal.
        """
        if not data:
            try:
                data = self.session.signal.GetContact(self.legacy_id)
            except RuntimeError as e:
                raise XMPPError(
                    "internal-server-error",
                    f"Is {self.legacy_id} is a valid signal ID? {e}",
                )
            if not data:
                raise XMPPError("item-not-found", "Contact not found")
        self.name = data.Name
        self.is_friend = True
        self.set_vcard(full_name=data.Name, phone=str(data.PhoneNumber))
        if data.Avatar.Data:
            await self.set_avatar(Avatar(data=bytes(data.Avatar.Data)))
        elif data.Avatar.Delete:
            await self.set_avatar(None)
        self.online()


class Roster(LegacyRoster[str, Contact]):
    session: "Session"

    async def fill(self):
        """
        Retrieve contacts, subscribing to their presence and adding to local roster.
        """
        for data in self.session.signal.ListContacts():
            contact = await self.by_legacy_id(data.ID)
            await contact.update_info(data)
            yield contact

    async def jid_username_to_legacy_id(self, jid_username: str) -> str:
        """
        Convert JID username part to legacy message ID, throwing an error if the username is not
        formatted correctly.
        """
        try:
            UUID(jid_username)
        except ValueError:
            raise XMPPError("item-not-found", f"Invalid contact ID {jid_username}")
        return await super().jid_username_to_legacy_id(jid_username)
