"""Enums for the LoopMessage API."""

from enum import Enum


class MessageEffect(str, Enum):
    """iMessage effects that can be applied to messages."""

    SLAM = "slam"
    LOUD = "loud"
    GENTLE = "gentle"
    INVISIBLE_INK = "invisibleInk"
    ECHO = "echo"
    SPOTLIGHT = "spotlight"
    BALLOONS = "balloons"
    CONFETTI = "confetti"
    LOVE = "love"
    LASERS = "lasers"
    FIREWORKS = "fireworks"
    SHOOTING_STAR = "shootingStar"
    CELEBRATION = "celebration"


class ReactionType(str, Enum):
    """iMessage reaction types (tapbacks)."""

    LOVE = "love"
    LIKE = "like"
    DISLIKE = "dislike"
    LAUGH = "laugh"
    EXCLAIM = "exclaim"
    QUESTION = "question"

    # Remove reactions (prefix with -)
    REMOVE_LOVE = "-love"
    REMOVE_LIKE = "-like"
    REMOVE_DISLIKE = "-dislike"
    REMOVE_LAUGH = "-laugh"
    REMOVE_EXCLAIM = "-exclaim"
    REMOVE_QUESTION = "-question"

    # Unknown reaction (from webhooks)
    UNKNOWN = "unknown"


class ServiceType(str, Enum):
    """Service types for message delivery."""

    IMESSAGE = "imessage"
    SMS = "sms"


class MessageStatusEnum(str, Enum):
    """Message status values."""

    PROCESSING = "processing"
    SCHEDULED = "scheduled"
    FAILED = "failed"
    SENT = "sent"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


class AlertType(str, Enum):
    """Webhook alert types."""

    MESSAGE_SCHEDULED = "message_scheduled"
    CONVERSATION_INITED = "conversation_inited"
    MESSAGE_FAILED = "message_failed"
    MESSAGE_SENT = "message_sent"
    MESSAGE_INBOUND = "message_inbound"
    MESSAGE_REACTION = "message_reaction"
    MESSAGE_TIMEOUT = "message_timeout"
    GROUP_CREATED = "group_created"
    INBOUND_CALL = "inbound_call"
    UNKNOWN = "unknown"


class DeliveryType(str, Enum):
    """Message delivery types."""

    IMESSAGE = "imessage"
    SMS = "sms"


class MessageType(str, Enum):
    """Inbound message types."""

    TEXT = "text"
    REACTION = "reaction"
    AUDIO = "audio"
    ATTACHMENTS = "attachments"
    STICKER = "sticker"
    LOCATION = "location"


class AudioFormat(str, Enum):
    """Supported audio file formats."""

    MP3 = "mp3"
    WAV = "wav"
    M4A = "m4a"
    CAF = "caf"
    AAC = "aac"
