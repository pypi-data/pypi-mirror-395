from typing import TYPE_CHECKING, AsyncIterator

from slidge.group import LegacyBookmarks, LegacyMUC, LegacyParticipant, MucType
from slidge.util.types import Avatar, HoleBound
from slixmpp.exceptions import XMPPError

from .generated import signal

if TYPE_CHECKING:
    from .contact import Contact
    from .session import Session


class Participant(LegacyParticipant):
    contact: "Contact"
    muc: "MUC"

    def parse_member(self, member: signal.GroupMember) -> None:
        if member.State == signal.GroupMemberBanned:
            self.muc.remove_participant(self, ban=True)
        elif member.State == signal.GroupMemberLeft:
            self.muc.remove_participant(self)
        elif member.State == signal.GroupMemberJoined:
            if member.Role == signal.GroupRoleMember:
                self.affiliation = "member"
                self.role = "participant"
            elif member.Role == signal.GroupRoleAdministrator:
                self.affiliation = "owner"
                self.role = "moderator"


class MUC(LegacyMUC[str, str, Participant, str]):
    session: "Session"

    HAS_DESCRIPTION = False
    REACTIONS_SINGLE_EMOJI = True
    _ALL_INFO_FILLED_ON_STARTUP = True

    def get_signal_group(self) -> signal.Group:
        try:
            data = self.session.signal.GetGroup(self.legacy_id)
        except RuntimeError as e:
            raise XMPPError("internal-server-error", f"Error: {e}")
        if not data:
            raise XMPPError("item-not-found", "Group not found")
        return data

    async def update_info(self, data: signal.Group | None = None) -> None:
        """
        Set fields for group based on data given, or if none was, as retrieved from Signal.
        """
        if data is None:
            data = self.get_signal_group()

        self.type = MucType.GROUP

        if data.Title:
            self.name = data.Title
        if data.Description:
            self.subject = data.Description

        if data.Members:
            self.n_participants = len(data.Members)
        for member in data.Members:
            participant = await self.get_participant_by_legacy_id(member.ID)
            participant.parse_member(member)

        if data.Avatar.Data:
            await self.set_avatar(Avatar(data=bytes(data.Avatar.Data)))
        elif data.Avatar.Delete:
            await self.set_avatar(None)
        await self.add_to_bookmarks()


class Bookmarks(LegacyBookmarks[str, MUC]):
    session: "Session"

    async def fill(self):
        """
        Retrieve groups, adding to bookmarks.
        """
        for data in self.session.signal.ListGroups():
            muc = await self.by_legacy_id(data.ID)
            await muc.update_info(data)
