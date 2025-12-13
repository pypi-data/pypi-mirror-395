package signal

import (
	// Standard library.
	"context"
	"fmt"
	"strconv"
	"strings"
	"time"

	// Third-party libraries.
	"github.com/google/uuid"
	"github.com/h2non/filetype"
	"go.mau.fi/mautrix-signal/pkg/signalmeow"
	"go.mau.fi/mautrix-signal/pkg/signalmeow/events"
	signalpb "go.mau.fi/mautrix-signal/pkg/signalmeow/protobuf"
	"go.mau.fi/mautrix-signal/pkg/signalmeow/types"
)

// EventKind represents all event types recognized by the Python session adapter, as emitted by the
// Go session adapter.
type EventKind int

// The event types handled by the overarching session adapter handler.
const (
	EventUnknown EventKind = iota
	EventLogin
	EventArchiveSync
	EventConnect
	EventLogout
	EventContact
	EventGroup
	EventMessage
	EventTyping
	EventReceipt
	EventCall
)

// EventPayload represents the collected payloads for all event types handled by the overarching
// session adapter handler. Only specific fields will be populated in events emitted by internal
// handlers, see documentation for specific types for more information.
type EventPayload struct {
	Login       Login
	Logout      Logout
	ArchiveSync ArchiveSync
	Connect     Connect
	Contact     Contact
	Group       Group
	Message     Message
	Typing      Typing
	Receipt     Receipt
	Call        Call
}

// HandleEventFunc represents a handler for incoming events sent to the Python adapter, accepting an
// event type and payload.
type HandleEventFunc func(EventKind, *EventPayload)

// Login represents event data for login events, typically carrying QR code information used for
// out-of-band authentication.
type Login struct {
	QRCode   string // An opaque string meant to be rendered as a QR code for pairing.
	DeviceID string // The concrete ID assigned to the paired linked device.
	Error    string // If non-empty, denotes an error during login.
}

// Logout represents event data for logout events, either expected (due to unlinking of a device) or
// unexpected (due to upstream errors).
type Logout struct {
	Reason string // An optional, human-readable reason for the logout.
}

// ArchiveSync represents event data for initial synchronization of chat state during login.
type ArchiveSync struct {
	Error string // If non-empty, denotes an error during archive synchronization.
}

// Connect represents event data for connection events, typically carrying connection errors and
// other metadata.
type Connect struct {
	AccountID   string // The unique account ID corresponding to our connected session.
	PhoneNumber string // The phone-number corresponding to our connected session.
	Error       string // A human-readable error message; if non-empty, indicates a connection error.
}

// A Contact represents any entity that be communicated with directly in Signal. This typically
// represents people, but not a group-chat.
type Contact struct {
	ID          string
	PhoneNumber string
	Name        string
	Avatar      Avatar
}

// A Avatar represents a small image set for a [Contact] or [Group].
type Avatar struct {
	Delete bool   // Whether or not any existing avatar should be removed.
	Data   []byte // The raw avatar data, assumed to be a valid image.
}

// NewContactEvent returns event data meant for [Session.propagateEvent] for the recipient information
// given. Unknown or invalid recipient information will return an [EventUnknown] event with nil data.
func newContactEvent(ctx context.Context, client *signalmeow.Client, event *types.Recipient) (EventKind, *EventPayload) {
	contact, err := newContact(ctx, client, event)
	if err != nil {
		client.Log.Err(err).Msg("Failed to create contact event")
		return EventUnknown, nil
	} else if contact.ID == "" {
		return EventUnknown, nil
	}

	return EventContact, &EventPayload{Contact: contact}
}

// NewContact returns a concrete [Contact] instance for the recipient information given. In cases
// where a valid contact can't be returned, [Contact.ID] will be left empty; most notably, this
// function will not return a contact for our *own* account.
func newContact(ctx context.Context, client *signalmeow.Client, data *types.Recipient) (Contact, error) {
	// Don't return contact for invalid or self IDs.
	switch data.ACI {
	case uuid.Nil, client.Store.ACI:
		return Contact{}, nil
	}

	var contact = Contact{
		ID:          data.ACI.String(),
		PhoneNumber: data.E164,
	}

	if data.Profile.AvatarPath == "clear" {
		contact.Avatar.Delete = true
	} else if data.Profile.AvatarPath != "" {
		avatar, err := client.DownloadUserAvatar(ctx, data.Profile.AvatarPath, data.Profile.Key)
		if err != nil {
			client.Log.Warn().Str("id", data.ACI.String()).AnErr("error", err).Msg("Failed fetching avatar for contact")
		} else {
			contact.Avatar.Data = avatar
		}
	}

	for _, n := range []string{data.Profile.Name, data.ContactName, data.Nickname, data.E164} {
		if n != "" {
			contact.Name = n
			break
		}
	}

	return contact, nil
}

// A Group represents a many-to-many chat containing one or more members, including ourselves.
type Group struct {
	ID          string
	Title       string
	Description string
	Avatar      Avatar
	Members     []GroupMember
}

// A GroupMember represents any source or destination for messages in a [Group].
type GroupMember struct {
	ID    string
	Role  GroupRole
	State GroupMemberState
}

// GroupMemberState represents different state transitions available to members of a [Group].
type GroupMemberState int

const (
	GroupMemberJoined GroupMemberState = iota // The default state, when a member is part of a group.
	GroupMemberLeft                           // A member that's either been kicked or volunterily left a group.
	GroupMemberBanned                         // A member that's been banned by an administrator.
)

// A GroupRole represents any of the different levels of access available to a [GroupMember] in a
// [Group].
type GroupRole int

const (
	GroupRoleMember        GroupRole = iota // A basic member, allowed to send and receive messages in, but not manage a group.
	GroupRoleAdministrator                  // A group administrator, having all access afforded to members while also allowed to manage it.
)

// NewGroupRole converts a raw [signalmeow.GroupMemberRole] to its equivalent [GroupRole].
func newGroupRole(role signalmeow.GroupMemberRole) GroupRole {
	switch role {
	case signalmeow.GroupMember_ADMINISTRATOR:
		return GroupRoleAdministrator
	default:
		return GroupRoleMember
	}
}

// NewGroup instantiates a [Group] from the raw Signal [signalmeow.Group] representation.
func newGroup(ctx context.Context, client *signalmeow.Client, data *signalmeow.Group) (Group, error) {
	var group = Group{
		ID:          data.GroupIdentifier.String(),
		Title:       data.Title,
		Description: data.Description,
	}

	// Process all members in group.
	// TODO: Map access control to affiliations?
	for _, m := range data.Members {
		if m.Role == signalmeow.GroupMember_UNKNOWN {
			continue
		}

		group.Members = append(group.Members, GroupMember{
			ID:    m.ACI.String(),
			Role:  newGroupRole(m.Role),
			State: GroupMemberJoined,
		})
	}

	// Download group avatar, if any.
	if data.AvatarPath == "" {
		group.Avatar.Delete = true
	} else {
		avatar, err := client.DownloadGroupAvatar(ctx, data.AvatarPath, data.GroupMasterKey)
		if err != nil {
			client.Log.Err(err).Str("id", group.ID).Msg("Failed getting group avatar")
		} else {
			group.Avatar.Data = avatar
		}
	}

	client.Log.Debug().Any("group", group).Msg("Group creation event")
	return group, nil
}

// NewContactEvent returns event data meant for [Session.propagateEvent] for the group change
// information given. This function will generally return partial [Group] data, based on changes
// made to the underlying group.
func newGroupChangeEvent(ctx context.Context, client *signalmeow.Client, groupID string, data *signalmeow.GroupChange) (EventKind, *EventPayload) {
	var group = Group{ID: groupID}

	// Handle group info changes.
	if data.ModifyTitle != nil {
		group.Title = *data.ModifyTitle
	}
	if data.ModifyDescription != nil {
		group.Description = *data.ModifyDescription
	}
	if data.ModifyAvatar != nil {
		avatar, err := client.DownloadGroupAvatar(ctx, *data.ModifyAvatar, data.GroupMasterKey)
		if err != nil {
			client.Log.Err(err).Str("id", group.ID).Msg("Failed getting group avatar")
		} else {
			group.Avatar.Data = avatar
		}
	}

	// Handle group membership changes.
	for _, m := range data.PromotePendingMembers {
		group.Members = append(group.Members, GroupMember{
			ID:    m.ACI.String(),
			Role:  GroupRoleMember,
			State: GroupMemberJoined,
		})
	}
	for _, m := range data.PromotePendingPniAciMembers {
		group.Members = append(group.Members, GroupMember{
			ID:    m.ACI.String(),
			Role:  GroupRoleMember,
			State: GroupMemberJoined,
		})
	}
	for _, m := range data.PromoteRequestingMembers {
		group.Members = append(group.Members, GroupMember{
			ID:    m.ACI.String(),
			Role:  newGroupRole(m.Role),
			State: GroupMemberJoined,
		})
	}
	for _, m := range data.AddMembers {
		group.Members = append(group.Members, GroupMember{
			ID:    m.ACI.String(),
			Role:  newGroupRole(m.Role),
			State: GroupMemberJoined,
		})
	}
	for _, m := range data.DeleteMembers {
		group.Members = append(group.Members, GroupMember{
			ID:    m.String(),
			State: GroupMemberLeft,
		})
	}
	for _, m := range data.AddBannedMembers {
		device, err := client.Store.DeviceStore.DeviceByPNI(ctx, m.ServiceID.UUID)
		if err != nil {
			client.Log.Err(err).Str("id", group.ID).Msg("Failed getting banned user ID")
		} else if device != nil {
			group.Members = append(group.Members, GroupMember{
				ID:    device.ACI.String(),
				State: GroupMemberBanned,
			})
		}
	}
	for _, m := range data.ModifyMemberRoles {
		group.Members = append(group.Members, GroupMember{
			ID:    m.ACI.String(),
			Role:  newGroupRole(m.Role),
			State: GroupMemberJoined,
		})
	}

	client.Log.Debug().Any("group", group).Msg("Group change event")
	return EventGroup, &EventPayload{Group: group}
}

const (
	// The character that separates account IDs from timestamps in generated message IDs.
	messageIDSeparator = "|"
)

// MakeMessageID returns a generated message ID for the sender account ID and message timestamp given.
func makeMessageID[ID interface{ uuid.UUID | string }](senderID ID, timestamp uint64) string {
	return fmt.Sprintf("%s%s%d", senderID, messageIDSeparator, timestamp)
}

// ParseMessageID accepts message IDs typically generated by [makeMessageID], and returns their
// constituent account IDs and timestamps.
func parseMessageID(id string) (uuid.UUID, uint64) {
	id, ts, ok := strings.Cut(id, messageIDSeparator)
	if !ok {
		return uuid.Nil, 0
	}

	messageID, err := uuid.Parse(id)
	if err != nil {
		return uuid.Nil, 0
	}

	timestamp, err := strconv.Atoi(ts)
	if err != nil {
		return uuid.Nil, 0
	}

	return messageID, uint64(timestamp)
}

// TimestampFromMessageID returns the timestamp part for the (semi-opaque) message ID given.
func TimestampFromMessageID(id string) uint64 {
	_, ts := parseMessageID(id)
	return ts
}

// MakeMessageTimestamp returns a generated timestamp for a given (presumably outgoing) message.
func makeMessageTimestamp() uint64 {
	return uint64(time.Now().UnixMilli())
}

// MessageKind represents all concrete message types (plain-text messages, edit messages, reactions)
// recognized by the Python session adapter.
type MessageKind int

// The message types handled by the overarching session event handler.
const (
	MessagePlain MessageKind = iota
	MessageAttachment
	MessageReaction
	MessageEdit
	MessageDelete
)

// A Message represents one of many kinds of bidirectional communication payloads, for example, a
// text message, a file (image, video) attachment, an emoji reaction, etc. Messages of different
// kinds are denoted as such, and re-use fields where the semantics overlap.
type Message struct {
	Kind        MessageKind  // The concrete message kind being sent or received.
	ID          string       // The unique message ID, used for referring to a specific Message instance.
	ChatID      string       // The account or group ID this message concerns.
	SenderID    string       // The account ID that sent this message.
	TargetID    string       // For messages that refer to other messages, the target message ID.
	Body        string       // The plain-text message body. For attachment messages, this can be a caption.
	Timestamp   uint64       // The Unix timestamp denoting when this message was created.
	IsCarbon    bool         // Whether or not this message concerns the gateway user themselves.
	IsGroup     bool         // Whether or not this is a group-chat message.
	Typing      Typing       // The typing state embedded in this message, if any.
	Reaction    Reaction     // The emoji reaction contained in this message, if any.
	ReplyTo     Reply        // A reference to the message being replied to, if any.
	Attachments []Attachment // The list of binary contents (e.g. media) attached to this message.
}

// NewMessage returns a new, plain-text [Message] instance for the data given. In general, text
// messages will contain a number of additional, optional fields (such as attachments) and can be
// composed of several sub-types (such as reactions) which are not handled here, but are rather
// part of event handling itself, see [newMessageEvent] for more.
func newMessage(_ context.Context, client *signalmeow.Client, senderID, chatID string, data *signalpb.DataMessage) Message {
	var msg = Message{
		Kind:      MessagePlain,
		ID:        makeMessageID(senderID, data.GetTimestamp()),
		SenderID:  senderID,
		ChatID:    chatID,
		Body:      data.GetBody(),
		Timestamp: data.GetTimestamp(),
		IsCarbon:  senderID == client.Store.ACI.String(),
		IsGroup:   data.GroupV2 != nil,
	}

	if q := data.GetQuote(); q != nil {
		msg.ReplyTo.ID = makeMessageID(q.GetAuthorAci(), q.GetId())
		msg.ReplyTo.AuthorID = q.GetAuthorAci()
		msg.ReplyTo.Body = q.GetText()
	}

	return msg
}

// A Reaction is a quick, emoji response to an existing message. Signal generally allows only a
// single reaction to messages, and has special rules around removal of reactions.
type Reaction struct {
	Emoji  string // The emoji being reacted with.
	Remove bool   // Whether or not we should remove the emoji contained in the message, if any.
}

// A Reply represents a reference to a previous message being replied to, with partial data set.
type Reply struct {
	ID       string
	AuthorID string
	Body     string
}

// A Attachment represents any binary data provided alongside a [Message], for instance, an image
// or voice message.
type Attachment struct {
	ContentType string // The MIME type for this attachment.
	Filename    string // The name given to this attachment, if any.
	Data        []byte // The raw attachment data.
}

const (
	// The content type used for sending long, plain-text messages as attachments over Signal.
	contentTypeLongText = "text/x-signal-plain"
)

// DetectContentType returns a valid MIME type for the given data, or "application/octet-stream" if
// data does not match any known type.
func detectContentType(buf []byte) string {
	m, _ := filetype.Match(buf)
	if m == filetype.Unknown {
		return "application/octet-stream"
	}
	return m.MIME.Value
}

// NewAttachment returns a concrete [Attachment] instance from the given Signal attachment pointer,
// downloading and converting incoming data as required. Any errors returned will result in an empty
// [Attachment] being returned.
func newAttachment(ctx context.Context, ptr *signalpb.AttachmentPointer) (Attachment, error) {
	var attachment = Attachment{
		ContentType: ptr.GetContentType(),
		Filename:    ptr.GetFileName(),
	}

	// TODO: Pass in attachment hash for back-filled attacments.
	data, err := signalmeow.DownloadAttachmentWithPointer(ctx, ptr, nil)
	if err != nil {
		return Attachment{}, err
	}

	attachment.Data = data

	// Infer content type from data if none was set in incoming attachment data.
	if attachment.ContentType == "" {
		attachment.ContentType = detectContentType(attachment.Data)
	}

	return attachment, nil
}

// NewMessageEvent returns event data meant for [Session.proparageEvent] for the message data given.
// Messages are defined fairly broadly in Signal, and can represent plain-text message, media
// messages, as well as other "protocol" message such as edits etc.
func newMessageEvent(ctx context.Context, client *signalmeow.Client, event *events.ChatEvent) (EventKind, *EventPayload) {
	var msg Message
	switch e := event.Event.(type) {
	case *signalpb.DataMessage:
		switch {
		// Handle group change sub-events.
		case e.GetGroupV2().GetGroupChange() != nil:
			c, err := client.DecryptGroupChange(ctx, e.GetGroupV2())
			if err != nil {
				client.Log.Err(err).Msg("Failed processing incoming group change")
				return EventUnknown, nil
			}
			return newGroupChangeEvent(ctx, client, event.Info.ChatID, c)
		}

		msg = newMessage(ctx, client, event.Info.Sender.String(), event.Info.ChatID, e)

		switch {
		// Process any attachments in message.
		case e.GetAttachments() != nil:
			for _, ptr := range e.GetAttachments() {
				a, err := newAttachment(ctx, ptr)
				if err != nil {
					client.Log.Err(err).Msg("Failed to process incoming attachment")
				} else {
					msg.Attachments = append(msg.Attachments, a)
				}
			}

			// Downloading attachments failed completely, don't handle message at all.
			if len(msg.Attachments) == 0 {
				return EventUnknown, nil
			}

			// Handle long text attachments as plain-text messages.
			if len(msg.Attachments) == 1 && msg.Attachments[0].ContentType == contentTypeLongText {
				msg.Body = string(msg.Attachments[0].Data)
			} else {
				msg.Kind = MessageAttachment
			}
		// Process sticker.
		case e.GetSticker() != nil:
			a, err := newAttachment(ctx, e.GetSticker().GetData())
			if err != nil {
				return EventUnknown, nil
			}

			msg.Kind = MessageAttachment
			msg.Attachments = []Attachment{a}
		// Extend message with incoming reactions.
		case e.GetReaction() != nil:
			msg.Kind = MessageReaction
			msg.TargetID = makeMessageID(e.GetReaction().GetTargetAuthorAci(), e.GetReaction().GetTargetSentTimestamp())
			msg.Reaction = Reaction{Emoji: e.GetReaction().GetEmoji(), Remove: e.GetReaction().GetRemove()}
		// Process message deletion event.
		case e.GetDelete() != nil:
			msg.Kind = MessageDelete
			msg.TargetID = makeMessageID(event.Info.Sender.String(), e.GetDelete().GetTargetSentTimestamp())
		}
	case *signalpb.TypingMessage:
		return newTypingEvent(ctx, event.Info.Sender.String(), event.Info.ChatID, e)
	case *signalpb.EditMessage:
		msg = newMessage(ctx, client, event.Info.Sender.String(), event.Info.ChatID, e.GetDataMessage())
		msg.Kind = MessageEdit
		msg.TargetID = makeMessageID(event.Info.Sender, e.GetTargetSentTimestamp())
	}

	// No message ID means message wasn't processed correctly, don't try to handle.
	if msg.ID == "" {
		return EventUnknown, nil
	}

	return EventMessage, &EventPayload{Message: msg}
}

// A TypingState represents different states of typing notificates for incoming and outgoing messages.
type TypingState int

// ToSignal converts the given [TypingState] value to its equivalent for use by the Signal client
// library.
func (s TypingState) toSignal() signalpb.TypingMessage_Action {
	if s == TypingStateStarted {
		return signalpb.TypingMessage_STARTED
	}
	return signalpb.TypingMessage_STOPPED
}

// The distinct typing states handled by the overarching session event handler.
const (
	TypingStateStopped TypingState = iota
	TypingStateStarted
)

// Typing contains event data related to typing notifications.
type Typing struct {
	State    TypingState // The distinct typing state.
	SenderID string      // The ID for the sender for this typing notification.
	ChatID   string      // The account or group ID this message concerns.
	IsGroup  bool        // Whether or not this is a group-chat message.
}

// NewTypingEvent returns event data meant for [Session.propagateEvent] for the primive typing event
// given. Unknown or invalid typing states will return an [EventUnknown] event with nil data.
func newTypingEvent(_ context.Context, senderID, chatID string, event *signalpb.TypingMessage) (EventKind, *EventPayload) {
	var typing = Typing{
		SenderID: senderID,
		ChatID:   chatID,
		IsGroup:  event.GetGroupId() != nil,
	}

	switch event.GetAction() {
	case signalpb.TypingMessage_STARTED:
		typing.State = TypingStateStarted
	case signalpb.TypingMessage_STOPPED:
		typing.State = TypingStateStopped
	default:
		return EventUnknown, nil
	}

	return EventTyping, &EventPayload{Typing: typing}
}

// ReceiptKind represents the different types of delivery receipts possible in Signal.
type ReceiptKind int

// The delivery receipts handled by the overarching session event handler.
const (
	ReceiptUnknown ReceiptKind = iota
	ReceiptDelivered
	ReceiptRead
)

// A Receipt represents a notice of delivery or presentation for [Message] instances sent or
// received. Receipts can be delivered for many messages at once, but are generally all delivered
// under one specific state at a time.
type Receipt struct {
	Kind       ReceiptKind // The distinct kind of receipt presented.
	SenderID   string      // The ID for the sender for this receipt.
	Timestamps []uint64    // The list of message timestamps to mark for receipt.
	IsCarbon   bool        // Whether or not this receipt is coming from ourselves.
}

// NewReceiptEvent returns event data meant for [Session.propagateEvent] for the primive receipt
// event given. Unknown or invalid receipts will return an [EventUnknown] event with nil data.
func newReceiptEvent(_ context.Context, client *signalmeow.Client, event *events.Receipt) (EventKind, *EventPayload) {
	var receipt = Receipt{
		SenderID:   event.Sender.String(),
		Timestamps: event.Content.Timestamp,
		IsCarbon:   event.Sender == client.Store.ACI,
	}

	if len(receipt.Timestamps) == 0 {
		return EventUnknown, nil
	}

	switch event.Content.GetType() {
	case signalpb.ReceiptMessage_DELIVERY:
		receipt.Kind = ReceiptDelivered
	case signalpb.ReceiptMessage_READ:
		receipt.Kind = ReceiptRead
	}

	return EventReceipt, &EventPayload{Receipt: receipt}
}

// NewSelfReceiptEvent returns event data meant for [Session.proparageEvent] for the carbon receipt
// data given.
func newSelfReceiptEvent(_ context.Context, event *signalpb.SyncMessage_Read) (EventKind, *EventPayload) {
	return EventReceipt, &EventPayload{
		Receipt: Receipt{
			SenderID:   event.GetSenderAci(),
			Timestamps: []uint64{event.GetTimestamp()},
			IsCarbon:   true,
		},
	}
}

// CallState represents the state of an ongoing or completed call.
type CallState int

// The call states handled by the overarching session event handler.
const (
	CallUnknown CallState = iota
	CallIncoming
	CallMissed
)

// A Call represents an incoming or outgoing voice/video call made over Signal. Full support for
// calls is currently not implemented, and this structure contains the bare minimum data required
// for notifying on missed calls.
type Call struct {
	State     CallState // The state of this call.
	SenderID  string    // The ID for the sender for this typing notification.
	ChatID    string    // The account or group ID this message concerns.
	Timestamp uint64    // The time the call state was changed.
}

// NewCallEvent returns event data meant for [Session.propagateEvent] for the call metadata given.
func newCallEvent(_ context.Context, event *events.Call) (EventKind, *EventPayload) {
	var state = CallIncoming
	if !event.IsRinging {
		state = CallMissed
	}
	return EventCall, &EventPayload{
		Call: Call{
			State:     state,
			SenderID:  event.Info.Sender.String(),
			ChatID:    event.Info.ChatID,
			Timestamp: event.Timestamp,
		},
	}
}
