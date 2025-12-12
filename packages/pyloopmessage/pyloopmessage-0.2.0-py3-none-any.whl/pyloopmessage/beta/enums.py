"""Enums for the LoopMessage Beta API."""

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
    """iMessage reaction types (tapbacks) - inbound only in Beta API."""

    LOVE = "love"
    LIKE = "like"
    DISLIKE = "dislike"
    LAUGH = "laugh"
    EXCLAIM = "exclaim"
    QUESTION = "question"
    UNKNOWN = "unknown"


class MessageStatusEnum(str, Enum):
    """Message status values for Beta API."""

    PROCESSING = "processing"
    FAILED = "failed"
    DELIVERED = "delivered"
    UNKNOWN = "unknown"


class EventType(str, Enum):
    """Webhook event types for Beta API."""

    OPT_IN = "opt-in"
    MESSAGE_FAILED = "message_failed"
    MESSAGE_DELIVERED = "message_delivered"
    MESSAGE_INBOUND = "message_inbound"
    MESSAGE_REACTION = "message_reaction"
    INBOUND_CALL = "inbound_call"
    UNKNOWN = "unknown"


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
