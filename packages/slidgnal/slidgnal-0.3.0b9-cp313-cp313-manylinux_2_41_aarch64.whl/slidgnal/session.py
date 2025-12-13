import asyncio
from datetime import datetime, timezone
from functools import wraps
from os.path import basename
from pathlib import Path

from aiohttp import ClientSession
from slidge import BaseSession, GatewayUser, global_config
from slidge.util.types import LegacyAttachment, MessageReference
from slixmpp.exceptions import XMPPError

from .contact import Contact, Roster
from .gateway import Gateway
from .generated import go, signal
from .group import MUC, Participant

MESSAGE_LOGIN_SUCCESS = (
    "Login successful! You might need to repeat this process in the future if the Linked Device "
    "is re-registered from your main device."
)

MESSAGE_LOGGED_OUT = (
    "You have been logged out, please use the re-login adhoc command and re-scan the QR code on "
    "your main device."
)

Recipient = Contact | MUC


class Session(BaseSession[str, Recipient]):
    contacts: "Roster"
    xmpp: "Gateway"

    def __init__(self, user: GatewayUser):
        super().__init__(user)
        try:
            device = signal.LinkedDevice(
                ID=self.user.legacy_module_data["device_id"],
                ArchiveSynced=self.user.legacy_module_data.get("archive_synced", False),
            )
        except KeyError:
            device = signal.LinkedDevice()
        self.signal = signal.NewSession(self.xmpp.signal, device)
        self.__handle_event = make_sync(self.handle_event, self.xmpp.loop)
        self.signal.SetEventHandler(self.__handle_event)
        self.__message_ids: dict[str, str] = {}
        self.__message_timestamps: dict[float, str] = {}
        self.__message_reactions: dict[str, str] = {}

    async def login(self):
        self.__reset_connected()
        self.signal.Login()
        return await self.__connected

    async def handle_event(self, event, ptr):
        """
        Handle incoming event, as propagated by the Signal adapter. Typically, events carry all
        state required for processing by the Gateway itself, and will do minimal processing
        themselves.
        """
        data = signal.EventPayload(handle=ptr)
        if event == signal.EventLogin:
            await self.handle_login(data.Login)
        elif event == signal.EventConnect:
            await self.handle_connect(data.Connect)
        elif event == signal.EventLogout:
            await self.handle_logout(data.Logout)
        elif event == signal.EventArchiveSync:
            await self.handle_archive_sync(data.ArchiveSync)
        elif event == signal.EventContact:
            await self.handle_contact(data.Contact)
        elif event == signal.EventGroup:
            await self.handle_group(data.Group)
        elif event == signal.EventMessage:
            await self.handle_message(data.Message)
        elif event == signal.EventTyping:
            await self.handle_typing(data.Typing)
        elif event == signal.EventReceipt:
            await self.handle_receipt(data.Receipt)
        elif event == signal.EventCall:
            await self.handle_call(data.Call)

    async def handle_login(self, data: signal.Login):
        """
        Handle login event, which either has us complete device linking out-of-bounds with a given
        QR code or completes linking with device credentials.
        """
        if data.QRCode:
            self.send_gateway_status("QR Scan Needed…", show="dnd")
            self.send_gateway_message(data.QRCode)
            await self.send_qr(data.QRCode)
        elif data.DeviceID:
            self.send_gateway_status("Linking device…", show="dnd")
            self.send_gateway_message(MESSAGE_LOGIN_SUCCESS)
            self.legacy_module_data_set({"device_id": data.DeviceID})
        elif data.Error:
            self.send_gateway_status("Login error", show="dnd")
            self.xmpp.loop.call_soon_threadsafe(
                self.__connected.set_exception,
                XMPPError("internal-server-error", data.Error),
            )

    async def handle_connect(self, data: signal.Connect):
        """
        Handle connection event, ensuring that the session is set up correctly for future events.
        """
        if self.__connected.done():
            if data.Error:
                self.send_gateway_status("Connection error", show="dnd")
                self.send_gateway_message(data.Error)
            else:
                self.contacts.user_legacy_id = data.AccountID
                self.user_phone = data.PhoneNumber
                self.send_gateway_status(f"Connected as {self.user_phone}", show="chat")
        elif data.Error:
            self.xmpp.loop.call_soon_threadsafe(
                self.__connected.set_exception,
                XMPPError("internal-server-error", data.Error),
            )
        else:
            self.contacts.user_legacy_id = data.AccountID
            self.user_phone = data.PhoneNumber
            self.xmpp.loop.call_soon_threadsafe(
                self.__connected.set_result, f"Connected as {self.user_phone}"
            )

    async def handle_archive_sync(self, data: signal.ArchiveSync):
        """
        Handle chat archive synchronization event, setting state for the session that ensures that
        we won't be making future requests to fetch from the archive.
        """
        self.legacy_module_data_update({"archive_synced": True})
        if data.Error:
            self.send_gateway_message(f"Failed synchronizing archive: {data.Error}")

    async def handle_logout(self, data: signal.Logout):
        """
        Handle remote Signal logout event, propagating status to gateway.
        """
        self.logged = False
        message = MESSAGE_LOGGED_OUT
        if data.Reason:
            message += f"\nReason: {data.Reason}"
        self.send_gateway_status("Logged out", show="away")
        self.send_gateway_message(message)

    async def handle_contact(self, data: signal.Contact):
        """
        Handle incoming contact event, updating information from data given and adding to roster if
        needed.
        """
        contact = await self.contacts.by_legacy_id(data.ID)
        await contact.update_info(data)
        await contact.add_to_roster()

    async def handle_group(self, data: signal.Group):
        """
        Handle incoming group event, updating information from data given and adding to bookmarks if
        needed.
        """
        muc = await self.bookmarks.by_legacy_id(data.ID)
        await muc.update_info(data)

    async def handle_message(self, data: signal.Message):
        """
        Handle incoming message, which is typically a plain-text message but can also denote more
        complex interactions such as reactions, message edits, etc.
        """
        recipient = await self.__get_recipient(
            data.SenderID, data.ChatID, data.IsCarbon, data.IsGroup
        )
        message_id = str(
            self.__get_original_message_id(data.TargetID) or data.TargetID or data.ID,
        )
        message_timestamp = (
            datetime.fromtimestamp(data.Timestamp / 1000, tz=timezone.utc)
            if data.Timestamp > 0
            else None
        )
        if data.Kind == signal.MessagePlain:
            recipient.send_text(
                body=data.Body,
                legacy_msg_id=message_id,
                when=message_timestamp,
                reply_to=await self.__get_reply_to(data.ReplyTo),
                carbon=data.IsCarbon,
            )
            self.__set_message_id_for_timestamp(message_id, data.Timestamp)
        elif data.Kind == signal.MessageAttachment:
            attachments = await Attachment.from_list(data.Attachments)
            await recipient.send_files(
                attachments=attachments,
                body=data.Body,
                legacy_msg_id=message_id,
                when=message_timestamp,
                reply_to=await self.__get_reply_to(data.ReplyTo),
                carbon=data.IsCarbon,
            )
            for attachment in attachments:
                if global_config.NO_UPLOAD_METHOD != "symlink":
                    self.log.debug("Removing '%s' from disk", attachment.path)
                    if attachment.path is None:
                        continue
                    Path(attachment.path).unlink(missing_ok=True)
            self.__set_message_id_for_timestamp(message_id, data.Timestamp)
        elif data.Kind == signal.MessageReaction:
            emojis = [] if data.Reaction.Remove else [data.Reaction.Emoji]
            recipient.react(
                legacy_msg_id=message_id,
                emojis=emojis,
                carbon=data.IsCarbon,
            )
        elif data.Kind == signal.MessageEdit:
            recipient.correct(
                legacy_msg_id=message_id,
                new_text=data.Body,
                when=message_timestamp,
                reply_to=await self.__get_reply_to(data.ReplyTo),
                carbon=data.IsCarbon,
            )
            self.__set_message_id_for_timestamp(data.ID, data.Timestamp)
            self.__set_original_message_id(data.ID, message_id)
        elif data.Kind == signal.MessageDelete:
            recipient.retract(legacy_msg_id=message_id, carbon=data.IsCarbon)

    async def handle_typing(self, data: signal.Typing):
        """
        Handle incoming typing notification, as propagated by the Signal adapter.
        """
        recipient = await self.__get_recipient(
            data.SenderID, data.ChatID, is_group=data.IsGroup
        )
        if data.State == signal.TypingStateStarted:
            recipient.composing()
        elif data.State == signal.TypingStateStopped:
            recipient.paused()

    async def handle_receipt(self, data: signal.Receipt):
        """
        Handle incoming delivered/read receipt, as propagated by the Signal adapter.
        """
        recipient = await self.__get_recipient(data.SenderID)
        for timestamp in data.Timestamps:
            message_id = self.__get_message_id_for_timestamp(timestamp)
            if message_id is not None:
                if data.Kind == signal.ReceiptDelivered:
                    recipient.received(message_id)
                elif data.Kind == signal.ReceiptRead:
                    recipient.displayed(legacy_msg_id=message_id, carbon=data.IsCarbon)

    async def handle_call(self, data: signal.Call):
        """
        Handle incoming call notification, as propagated by the Signal adapter.
        """
        recipient = await self.__get_recipient(data.SenderID)
        text = f"from {recipient.name or 'tel:' + str(recipient.jid.local)} (xmpp:{recipient.jid.bare})"
        if data.State == signal.CallIncoming:
            text = "Incoming call " + text
        elif data.State == signal.CallMissed:
            text = "Missed call " + text
        else:
            text = "Call " + text
        if data.Timestamp > 0:
            call_at = datetime.fromtimestamp(data.Timestamp / 1000, tz=timezone.utc)
            text = text + f" at {call_at}"
        self.send_gateway_message(text)

    async def on_text(
        self,
        chat: Recipient,
        text: str,
        *,
        reply_to_msg_id: str | None = None,
        reply_to_fallback_text: str | None = None,
        reply_to=None,
        **_,
    ):
        """
        Send outgoing plain-text message to given Signal contact.
        """
        message = signal.Message(
            Kind=signal.MessagePlain,
            ChatID=chat.legacy_id,
            Body=text,
        )
        message = self.__set_reply_to(
            chat, message, reply_to_msg_id, reply_to_fallback_text, reply_to
        )
        message_id = self.signal.SendMessage(message)
        self.__set_message_id_for_timestamp(
            message_id, signal.TimestampFromMessageID(message_id)
        )
        return message_id

    async def on_file(
        self,
        chat: Recipient,
        url: str,
        http_response,
        reply_to_msg_id: str | None = None,
        reply_to_fallback_text: str | None = None,
        reply_to=None,
        **_,
    ):
        """
        Send outgoing media message (i.e. audio, image, document) to given Signal contact.
        """
        data = await get_url_bytes(self.http, url)
        if not data:
            raise XMPPError(
                "internal-server-error",
                "Unable to retrieve file from XMPP server, try again",
            )
        message_attachment = signal.Attachment(
            ContentType=http_response.content_type,
            Filename=basename(url),
            Data=go.Slice_byte.from_bytes(data),
        )
        message = signal.Message(
            Kind=signal.MessageAttachment,
            ChatID=chat.legacy_id,
            Attachments=signal.Slice_signal_Attachment([message_attachment]),
        )
        message = self.__set_reply_to(
            chat, message, reply_to_msg_id, reply_to_fallback_text, reply_to
        )
        message_id = self.signal.SendMessage(message)
        self.__set_message_id_for_timestamp(
            message_id, signal.TimestampFromMessageID(message_id)
        )
        return message_id

    async def on_react(
        self, chat: Recipient, legacy_msg_id: str, emojis: list[str], thread=None
    ):
        """
        Send or remove emoji reaction to existing Signal message. Slidge core makes sure that the
        emojis parameter is always empty or a *single* emoji.
        """
        message = signal.Message(
            Kind=signal.MessageReaction,
            ID=legacy_msg_id,
            ChatID=chat.legacy_id,
        )
        if emojis:
            message.Reaction = signal.Reaction(Emoji=emojis[0], Remove=False)
        else:
            previous_reaction = self.__get_message_reaction(legacy_msg_id)
            if not previous_reaction:
                raise XMPPError(
                    "not-acceptable", "Existing reaction not found, cannot remove"
                )
            message.Reaction = signal.Reaction(Emoji=previous_reaction, Remove=True)
        self.signal.SendMessage(message)
        if emojis:
            self.__set_message_reaction(legacy_msg_id, emojis[0])

    async def on_correct(
        self,
        chat: Recipient,
        text: str,
        legacy_msg_id: str,
        thread=None,
        link_previews=(),
        mentions=None,
    ):
        """
        Request correction (aka editing) for a given Signal message.
        """
        message = signal.Message(
            Kind=signal.MessageEdit,
            ID=legacy_msg_id,
            ChatID=chat.legacy_id,
            Body=text,
        )
        message_id = self.signal.SendMessage(message)
        self.__set_message_id_for_timestamp(
            message_id, signal.TimestampFromMessageID(message_id)
        )
        return message_id

    async def on_presence(self, *args, **kwargs):
        """
        Signal doesn't support contact presence, so calls to this function are no-ops.
        """
        pass

    async def on_active(self, *args, **kwargs):
        """
        Signal has no equivalent to the "active" chat state, so calls to this function are no-ops.
        """
        pass

    async def on_inactive(self, *args, **kwargs):
        """
        Signal has no equivalent to the "inactive" chat state, so calls to this function are no-ops.
        """
        pass

    async def on_composing(self, chat: Recipient, thread=None):
        """
        Send "started" typing state to given Signal contact, signifying that a message is currently
        being composed.
        """
        typing = signal.Typing(
            ChatID=chat.legacy_id,
            Typing=signal.Typing(State=signal.TypingStateStarted),
        )
        self.signal.SendTyping(typing)

    async def on_paused(self, chat: Recipient, thread=None):
        """
        Send "stopped" typing state to given Signal contact, signifying that an (unsent) message is
        no longer being composed.
        """
        typing = signal.Typing(
            ChatID=chat.legacy_id,
            Typing=signal.Typing(State=signal.TypingStateStopped),
        )
        self.signal.SendTyping(typing)

    async def on_displayed(self, chat: Recipient, legacy_msg_id: str, thread=None):
        """
        Send "read" receipt, signifying that the Signal message sent has been displayed on the XMPP
        client.
        """
        message_timestamp = signal.TimestampFromMessageID(legacy_msg_id)
        receipt = signal.Receipt(
            SenderID=chat.legacy_id,
            Timestamps=go.Slice_uint64([message_timestamp]),
        )
        self.signal.SendReceipt(receipt)

    async def on_retract(self, chat: Recipient, legacy_msg_id: str, thread=None):
        """
        Request deletion (aka retraction) for a given Signal message.
        """
        message = signal.Message(
            Kind=signal.MessageDelete,
            ChatID=chat.legacy_id,
            TargetID=legacy_msg_id,
        )
        self.signal.SendMessage(message)

    async def __get_recipient(
        self,
        legacy_sender_id: str,
        legacy_chat_id: str | None = None,
        is_carbon: bool = False,
        is_group: bool = False,
    ) -> Contact | Participant:
        """
        Return correct recipient for given references to sender and chat IDs, the latter of which
        can either represent another contact, or a group-chat.
        """
        if is_group:
            muc = await self.bookmarks.by_legacy_id(legacy_chat_id)
            return await muc.get_participant_by_legacy_id(legacy_sender_id)
        if is_carbon:
            return await self.contacts.by_legacy_id(legacy_chat_id)
        else:
            return await self.contacts.by_legacy_id(legacy_sender_id)

    async def __get_reply_to(self, data: signal.Reply) -> MessageReference | None:
        """
        Get message reference for reply data, or return None.
        """
        if not data.ID:
            return None
        reply_to = MessageReference(
            legacy_id=data.ID,
            body=data.Body,
        )
        if data.AuthorID == self.contacts.user_legacy_id:
            reply_to.author = "user"
        else:
            reply_to.author = await self.contacts.by_legacy_id(data.AuthorID)
        return reply_to

    def __set_reply_to(
        self,
        chat: Recipient,
        message: signal.Message,
        reply_to_msg_id: str | None = None,
        reply_to_fallback_text: str | None = None,
        reply_to=None,
    ):
        """
        Sets ReplyTo fields for given Message, returning the Message.
        """
        if reply_to_msg_id:
            message.ReplyTo.ID = reply_to_msg_id
        if reply_to:
            message.ReplyTo.AuthorID = (
                reply_to.contact.legacy_id if chat.is_group else chat.legacy_id
            )
        if reply_to_fallback_text:
            message.ReplyTo.Body = strip_quote_prefix(reply_to_fallback_text)
            message.Body = message.Body.lstrip()
        return message

    def __set_original_message_id(
        self,
        new_legacy_msg_id: str,
        original_legacy_msg_id: str,
    ) -> None:
        """
        Set new message ID to original message ID mapping.
        """
        self.__message_ids[new_legacy_msg_id] = original_legacy_msg_id

    def __get_original_message_id(
        self,
        new_legacy_msg_id: str,
    ) -> str | None:
        """
        Get original message ID for given new message ID.
        """
        return self.__message_ids.get(new_legacy_msg_id, None)

    def __set_message_id_for_timestamp(
        self,
        legacy_message_id: str,
        message_timestamp: float,
    ) -> None:
        """
        Set message ID to message timestamp mapping.
        """
        self.__message_timestamps[message_timestamp] = legacy_message_id

    def __get_message_id_for_timestamp(
        self,
        message_timestamp: float,
    ) -> str | None:
        """
        Get message ID for given message timestamp.
        """
        return self.__message_timestamps.get(message_timestamp, None)

    def __set_message_reaction(
        self,
        legacy_msg_id: str,
        emoji: str,
    ) -> None:
        """
        Set message reaction reference for a legacy message ID.
        """
        self.__message_reactions[legacy_msg_id] = emoji

    def __get_message_reaction(
        self,
        legacy_msg_id: str,
    ) -> str | None:
        """
        Get message reaction reference for a legacy message ID.
        """
        return self.__message_reactions.get(legacy_msg_id, None)

    def __reset_connected(self):
        if hasattr(self, "_connected") and not self.__connected.done():
            self.xmpp.loop.call_soon_threadsafe(self.__connected.cancel)
        self.__connected: asyncio.Future[str] = self.xmpp.loop.create_future()


class Attachment(LegacyAttachment):
    @staticmethod
    async def from_list(attachments: list[signal.Attachment]) -> list["Attachment"]:
        return [await Attachment.from_signal(attachment) for attachment in attachments]

    @staticmethod
    async def from_signal(attachment: signal.Attachment) -> "Attachment":
        return Attachment(
            content_type=attachment.ContentType,
            data=bytes(attachment.Data),
        )


async def get_url_bytes(client: ClientSession, url: str) -> bytes | None:
    """
    Get data from URL as raw bytes, if possible.
    """
    async with client.get(url) as resp:
        if resp.status == 200:
            return await resp.read()
    return None


def strip_quote_prefix(text: str):
    """
    Return multi-line text without leading quote marks (i.e. the ">" character).
    """
    return "\n".join(x.lstrip(">").strip() for x in text.split("\n")).strip()


def make_sync(func, loop):
    """
    Wrap async function in synchronous operation, running against the given loop in thread-safe mode.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if asyncio.iscoroutine(result):
            future = asyncio.run_coroutine_threadsafe(result, loop)
            return future.result()
        return result

    return wrapper
