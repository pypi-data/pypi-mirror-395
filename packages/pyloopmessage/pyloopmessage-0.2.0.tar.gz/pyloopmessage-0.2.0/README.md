# PyLoopMessage

A modern Python client for the LoopMessage iMessage API.

## Features

- ✨ Full support for LoopMessage REST API
- 🔒 Type-safe with comprehensive type hints
- 📱 Send messages, reactions, and audio messages
- 👥 Support for group messaging
- 📞 Webhook handling for real-time events
- 🧪 Async/await support
- 🛡️ Built-in error handling and retries

## Installation

```bash
pip install pyloopmessage
```

## Quick Start

```python
from pyloopmessage import LoopMessageClient

# Initialize the client
client = LoopMessageClient(
    authorization_key="your_auth_key",
    secret_key="your_secret_key"
)

# Send a message
response = await client.send_message(
    recipient="+1234567890",
    text="Hello from PyLoopMessage!",
    sender_name="YourSenderName"
)

print(f"Message sent with ID: {response.message_id}")
```

## API Support

### Sending Messages
- ✅ Send text messages to individuals
- ✅ Send messages to groups
- ✅ Send audio messages
- ✅ Send reactions
- ✅ Message effects (slam, loud, gentle, etc.)
- ✅ Attachments support
- ✅ Reply-to functionality

### Message Status
- ✅ Check message status
- ✅ Webhook event handling
- ✅ Real-time status updates

### Advanced Features
- ✅ Typing indicators
- ✅ Read status
- ✅ Sandbox mode
- ✅ Error handling with detailed error codes

## Documentation

For detailed documentation and examples, visit our [GitHub repository](https://github.com/yourusername/pyloopmessage).

## License

MIT License - see LICENSE file for details.