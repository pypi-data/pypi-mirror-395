"""Tests for enums."""

from pyloopmessage.enums import (
    AlertType,
    AudioFormat,
    DeliveryType,
    MessageEffect,
    MessageStatusEnum,
    MessageType,
    ReactionType,
    ServiceType,
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
    """Test ReactionType enum."""

    def test_positive_reactions(self):
        """Test positive reaction types."""
        assert ReactionType.LOVE == "love"
        assert ReactionType.LIKE == "like"
        assert ReactionType.DISLIKE == "dislike"
        assert ReactionType.LAUGH == "laugh"
        assert ReactionType.EXCLAIM == "exclaim"
        assert ReactionType.QUESTION == "question"

    def test_remove_reactions(self):
        """Test remove reaction types."""
        assert ReactionType.REMOVE_LOVE == "-love"
        assert ReactionType.REMOVE_LIKE == "-like"
        assert ReactionType.REMOVE_DISLIKE == "-dislike"
        assert ReactionType.REMOVE_LAUGH == "-laugh"
        assert ReactionType.REMOVE_EXCLAIM == "-exclaim"
        assert ReactionType.REMOVE_QUESTION == "-question"

    def test_unknown_reaction(self):
        """Test unknown reaction type."""
        assert ReactionType.UNKNOWN == "unknown"


class TestServiceType:
    """Test ServiceType enum."""

    def test_service_types(self):
        """Test service types."""
        assert ServiceType.IMESSAGE == "imessage"
        assert ServiceType.SMS == "sms"


class TestMessageStatusEnum:
    """Test MessageStatusEnum."""

    def test_status_values(self):
        """Test all status values."""
        assert MessageStatusEnum.PROCESSING == "processing"
        assert MessageStatusEnum.SCHEDULED == "scheduled"
        assert MessageStatusEnum.FAILED == "failed"
        assert MessageStatusEnum.SENT == "sent"
        assert MessageStatusEnum.TIMEOUT == "timeout"
        assert MessageStatusEnum.UNKNOWN == "unknown"


class TestAlertType:
    """Test AlertType enum."""

    def test_alert_types(self):
        """Test all alert types."""
        assert AlertType.MESSAGE_SCHEDULED == "message_scheduled"
        assert AlertType.CONVERSATION_INITED == "conversation_inited"
        assert AlertType.MESSAGE_FAILED == "message_failed"
        assert AlertType.MESSAGE_SENT == "message_sent"
        assert AlertType.MESSAGE_INBOUND == "message_inbound"
        assert AlertType.MESSAGE_REACTION == "message_reaction"
        assert AlertType.MESSAGE_TIMEOUT == "message_timeout"
        assert AlertType.GROUP_CREATED == "group_created"
        assert AlertType.INBOUND_CALL == "inbound_call"
        assert AlertType.UNKNOWN == "unknown"


class TestDeliveryType:
    """Test DeliveryType enum."""

    def test_delivery_types(self):
        """Test delivery types."""
        assert DeliveryType.IMESSAGE == "imessage"
        assert DeliveryType.SMS == "sms"


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
