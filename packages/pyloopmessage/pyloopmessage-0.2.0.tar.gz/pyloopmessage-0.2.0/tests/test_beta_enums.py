"""Tests for beta enums."""

from pyloopmessage.beta import (
    AudioFormat,
    EventType,
    MessageEffect,
    MessageStatusEnum,
    MessageType,
    ReactionType,
)


class TestMessageEffect:
    """Test MessageEffect enum."""

    def test_message_effects(self):
        """Test all message effects."""
        assert MessageEffect.SLAM == "slam"
        assert MessageEffect.LOUD == "loud"
        assert MessageEffect.GENTLE == "gentle"
        assert MessageEffect.INVISIBLE_INK == "invisibleInk"
        assert MessageEffect.ECHO == "echo"
        assert MessageEffect.SPOTLIGHT == "spotlight"
        assert MessageEffect.BALLOONS == "balloons"
        assert MessageEffect.CONFETTI == "confetti"
        assert MessageEffect.LOVE == "love"
        assert MessageEffect.LASERS == "lasers"
        assert MessageEffect.FIREWORKS == "fireworks"
        assert MessageEffect.SHOOTING_STAR == "shootingStar"
        assert MessageEffect.CELEBRATION == "celebration"


class TestReactionType:
    """Test ReactionType enum (inbound only in Beta API)."""

    def test_reaction_types(self):
        """Test reaction types."""
        assert ReactionType.LOVE == "love"
        assert ReactionType.LIKE == "like"
        assert ReactionType.DISLIKE == "dislike"
        assert ReactionType.LAUGH == "laugh"
        assert ReactionType.EXCLAIM == "exclaim"
        assert ReactionType.QUESTION == "question"
        assert ReactionType.UNKNOWN == "unknown"


class TestMessageStatusEnum:
    """Test MessageStatusEnum for Beta API."""

    def test_status_values(self):
        """Test all status values."""
        assert MessageStatusEnum.PROCESSING == "processing"
        assert MessageStatusEnum.FAILED == "failed"
        assert MessageStatusEnum.DELIVERED == "delivered"
        assert MessageStatusEnum.UNKNOWN == "unknown"

    def test_no_sent_status(self):
        """Test that 'sent' status doesn't exist in Beta (replaced by 'delivered')."""
        status_values = [s.value for s in MessageStatusEnum]
        assert "sent" not in status_values
        assert "delivered" in status_values

    def test_no_timeout_or_scheduled(self):
        """Test that timeout and scheduled statuses don't exist in Beta."""
        status_values = [s.value for s in MessageStatusEnum]
        assert "timeout" not in status_values
        assert "scheduled" not in status_values


class TestEventType:
    """Test EventType enum for Beta API."""

    def test_event_types(self):
        """Test all event types."""
        assert EventType.OPT_IN == "opt-in"
        assert EventType.MESSAGE_FAILED == "message_failed"
        assert EventType.MESSAGE_DELIVERED == "message_delivered"
        assert EventType.MESSAGE_INBOUND == "message_inbound"
        assert EventType.MESSAGE_REACTION == "message_reaction"
        assert EventType.INBOUND_CALL == "inbound_call"
        assert EventType.UNKNOWN == "unknown"

    def test_no_message_sent_event(self):
        """Test that 'message_sent' event doesn't exist in Beta (replaced by 'message_delivered')."""
        event_values = [e.value for e in EventType]
        assert "message_sent" not in event_values
        assert "message_delivered" in event_values

    def test_opt_in_event_exists(self):
        """Test that opt-in event exists in Beta."""
        event_values = [e.value for e in EventType]
        assert "opt-in" in event_values


class TestMessageType:
    """Test MessageType enum."""

    def test_message_types(self):
        """Test all message types."""
        assert MessageType.TEXT == "text"
        assert MessageType.REACTION == "reaction"
        assert MessageType.AUDIO == "audio"
        assert MessageType.ATTACHMENTS == "attachments"
        assert MessageType.STICKER == "sticker"
        assert MessageType.LOCATION == "location"


class TestAudioFormat:
    """Test AudioFormat enum."""

    def test_audio_formats(self):
        """Test all audio formats."""
        assert AudioFormat.MP3 == "mp3"
        assert AudioFormat.WAV == "wav"
        assert AudioFormat.M4A == "m4a"
        assert AudioFormat.CAF == "caf"
        assert AudioFormat.AAC == "aac"
