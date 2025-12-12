# Notify Africa Python SMS SDK

A Python SDK for integrating with Notify Africa SMS service, allowing developers to easily send SMS messages through their Python applications. This SDK matches the Node.js SDK structure for consistency across platforms.

## Features

- **Send Single SMS** - Send SMS to individual recipients
- **Send Batch SMS** - Send SMS to multiple recipients at once
- **Check Message Status** - Track SMS delivery status
- **Developer Friendly** - Type hints, error handling, and comprehensive documentation
- **Node.js Compatible** - Matches the Node.js SDK structure for easy migration

## Installation

```bash
pip install git+https://github.com/iPFSoftwares/notify-africa-python-sdk.git
```

## Quick Start

```python
from notify_africa import NotifyAfrica

# Initialize client
client = NotifyAfrica(
    apiToken="your_api_token_here"
)

# Send a single SMS
response = client.send_single_message(
    phoneNumber="2556XXXXXXXX",
    message="Hello from Notify Africa!",
    senderId="164"
)

print(f"Message ID: {response.messageId}")
print(f"Status: {response.status}")
```

## Usage Examples

### Send Single SMS

```python
from notify_africa import NotifyAfrica

client = NotifyAfrica(apiToken="your_api_token")

response = client.send_single_message(
    phoneNumber="2556XXXXXXXXX",
    message="Hello, this is a test message!",
    senderId="164"
)

print(f"Message ID: {response.messageId}")
print(f"Status: {response.status}")
# Output: Message ID: 165102
# Output: Status: PROCESSING
```

### Send Batch SMS

```python
from notify_africa import NotifyAfrica

client = NotifyAfrica(apiToken="your_api_token")

phone_numbers = [
    "2556XXXXXXXXXX",
    "255XXXXXXXX",
    "255XXXXXXXX"
]

response = client.send_batch_messages(
    phoneNumbers=phone_numbers,
    message="Bulk SMS message to all recipients",
    senderId="164"
)

print(f"Message Count: {response.messageCount}")
print(f"Credits Deducted: {response.creditsDeducted}")
print(f"Remaining Balance: {response.remainingBalance}")
```

### Check Message Status

```python
from notify_africa import NotifyAfrica

client = NotifyAfrica(apiToken="your_api_token")

# First, send a message
send_response = client.send_single_message(
    phoneNumber="2556XXXXXXX",
    message="Test message",
    senderId="164"
)

message_id = send_response.messageId

# Then check its status
status = client.check_message_status(messageId=message_id)

print(f"Message ID: {status.messageId}")
print(f"Status: {status.status}")
print(f"Sent At: {status.sentAt}")
print(f"Delivered At: {status.deliveredAt}")
```

## API Reference

### NotifyAfrica Class

#### Constructor

```python
NotifyAfrica(apiToken: str, baseUrl: str = "https://api.notify.africa")
```

**Parameters:**
- `apiToken` (str, required): Your Notify Africa API token
- `baseUrl` (str, optional): Base URL for the API. Defaults to `https://api.notify.africa`

**Example:**
```python
client = NotifyAfrica(apiToken="ntfy_...")
```

#### Methods

##### send_single_message

Sends a single SMS message.

```python
send_single_message(
    phoneNumber: str,
    message: str,
    senderId: str
) -> SendSingleResponse
```

**Parameters:**
- `phoneNumber` (str): The recipient's phone number (e.g., "2556XXXXX")
- `message` (str): The message content
- `senderId` (str): The sender ID (e.g., "164")

**Returns:** `SendSingleResponse` with:
- `messageId` (str): Unique identifier assigned to the message
- `status` (str): Processing or delivery status (e.g., "PROCESSING", "SENT", "DELIVERED")

**Example:**
```python
response = client.send_single_message(
    phoneNumber="2556XXXXXXXX",
    message="Hello from API!",
    senderId="164"
)
```

##### send_batch_messages

Sends a batch of SMS messages to multiple recipients.

```python
send_batch_messages(
    phoneNumbers: List[str],
    message: str,
    senderId: str
) -> SendBatchResponse
```

**Parameters:**
- `phoneNumbers` (List[str]): Array of recipient phone numbers
- `message` (str): The message content to send to all recipients
- `senderId` (str): The sender ID

**Returns:** `SendBatchResponse` with:
- `messageCount` (int): Number of messages attempted or sent
- `creditsDeducted` (int): Credits used for the batch send
- `remainingBalance` (int): Remaining account balance or credits

**Example:**
```python
response = client.send_batch_messages(
    phoneNumbers=["2556XXXXXXX", "2557XXXXXX"],
    message="Batch message to all recipients",
    senderId="164"
)
```

##### check_message_status

Checks the status of a sent message.

```python
check_message_status(messageId: str) -> MessageStatusResponse
```

**Parameters:**
- `messageId` (str): The ID of the message to check (e.g., "165102")

**Returns:** `MessageStatusResponse` with:
- `messageId` (str): Unique identifier of the message
- `status` (str): Current delivery or processing status
- `sentAt` (str | None): ISO8601 timestamp when the message was sent, or None if not sent
- `deliveredAt` (str | None): ISO8601 timestamp when the message was delivered, or None if not delivered

**Example:**
```python
status = client.check_message_status(messageId="165102")
```

## Response Models

### SendSingleResponse

```python
@dataclass
class SendSingleResponse:
    messageId: str
    status: str
```

### SendBatchResponse

```python
@dataclass
class SendBatchResponse:
    messageCount: int
    creditsDeducted: int
    remainingBalance: int
```

### MessageStatusResponse

```python
@dataclass
class MessageStatusResponse:
    messageId: str
    status: str
    sentAt: str | None
    deliveredAt: str | None
```

## Error Handling

The SDK provides comprehensive error handling through custom exceptions:

```python
from notify_africa import NotifyAfrica
from notify_africa.exceptions import (
    NotifyAfricaException,
    NetworkError
)

client = NotifyAfrica(apiToken="your_api_token")

try:
    response = client.send_single_message(
        phoneNumber="2556XXXXXXX",
        message="Test message",
        senderId="164"
    )
    print(f"Success! Message ID: {response.messageId}")
except NotifyAfricaException as e:
    print(f"API error: {e}")
    if e.status_code:
        print(f"Status code: {e.status_code}")
except NetworkError as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Exception Types

- `NotifyAfricaException`: Base exception for all API errors
- `NetworkError`: Raised when network request fails
- `AuthenticationError`: Raised when authentication fails
- `ValidationError`: Raised when request validation fails
- `InsufficientCreditsError`: Raised when user has insufficient SMS credits

## Advanced Usage

### Complete Workflow Example

```python
from notify_africa import NotifyAfrica
from notify_africa.exceptions import NotifyAfricaException, NetworkError

def send_and_track_sms(client, phone_number, message, sender_id):
    """Send SMS and track its delivery status"""
    try:
        # Send the message
        send_response = client.send_single_message(
            phoneNumber=phone_number,
            message=message,
            senderId=sender_id
        )
        
        print(f"Message sent! ID: {send_response.messageId}")
        print(f"Initial status: {send_response.status}")
        
        # Wait a bit for processing
        import time
        time.sleep(2)
        
        # Check status
        status = client.check_message_status(send_response.messageId)
        print(f"Current status: {status.status}")
        if status.sentAt:
            print(f"Sent at: {status.sentAt}")
        if status.deliveredAt:
            print(f"Delivered at: {status.deliveredAt}")
        
        return status
        
    except NotifyAfricaException as e:
        print(f"API error: {e}")
        return None
    except NetworkError as e:
        print(f"Network error: {e}")
        return None

# Usage
client = NotifyAfrica(apiToken="your_api_token")
send_and_track_sms(
    client=client,
    phone_number="2556XXXXXXXX",
    message="Hello from Python SDK!",
    sender_id="164"
)
```

### Batch Processing with Status Tracking

```python
from notify_africa import NotifyAfrica
import time

def send_batch_and_track(client, phone_numbers, message, sender_id):
    """Send batch messages and track each one"""
    # Send batch
    batch_response = client.send_batch_messages(
        phoneNumbers=phone_numbers,
        message=message,
        senderId=sender_id
    )
    
    print(f"Batch sent: {batch_response.messageCount} messages")
    print(f"Credits deducted: {batch_response.creditsDeducted}")
    print(f"Remaining balance: {batch_response.remainingBalance}")
    
    # Note: For batch messages, you'll need to track individual message IDs
    # if the API provides them in the response
    
    return batch_response

# Usage
client = NotifyAfrica(apiToken="your_api_token")
send_batch_and_track(
    client=client,
    phone_numbers=["255XXXXX", "255XXXXXX"],
    message="Batch test message",
    sender_id="164"
)
```

### Error Handling Best Practices

```python
from notify_africa import NotifyAfrica
from notify_africa.exceptions import (
    NotifyAfricaException,
    NetworkError,
    AuthenticationError,
    ValidationError,
    InsufficientCreditsError
)

def safe_send_sms(client, phone_number, message, sender_id):
    """Safely send SMS with comprehensive error handling"""
    try:
        response = client.send_single_message(
            phoneNumber=phone_number,
            message=message,
            senderId=sender_id
        )
        return response
    except AuthenticationError:
        print("❌ Authentication failed. Please check your API token.")
        return None
    except InsufficientCreditsError:
        print("❌ Insufficient credits. Please recharge your account.")
        return None
    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        return None
    except NetworkError as e:
        print(f"❌ Network error: {e}. Please check your internet connection.")
        return None
    except NotifyAfricaException as e:
        print(f"❌ API error: {e}")
        if e.status_code:
            print(f"   Status code: {e.status_code}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

# Usage
client = NotifyAfrica(apiToken="your_api_token")
result = safe_send_sms(
    client=client,
    phone_number="2556XXXXXXXX",
    message="Safe send test",
    sender_id="164"
)

if result:
    print(f"✅ Success! Message ID: {result.messageId}")
```

## SMS Status Codes

The following status codes are commonly returned:

| Status Code | Description |
|-------------|-------------|
| `PROCESSING` | SMS is being processed |
| `QUEUED` | SMS is queued for delivery |
| `SENT` | SMS has been sent to the carrier |
| `DELIVERED` | SMS was successfully delivered |
| `FAILED` | SMS delivery failed |
| `EXPIRED` | SMS expired before delivery |
| `REJECTED` | SMS was rejected by the carrier |

## Environment Variables

You can use environment variables to store your API token:

```bash
export NOTIFY_AFRICA_API_TOKEN="your_api_token_here"
```

Then in your Python code:

```python
import os
from notify_africa import NotifyAfrica

client = NotifyAfrica(apiToken=os.getenv("NOTIFY_AFRICA_API_TOKEN"))
```

## Requirements

- Python 3.7+
- requests library

## License

See LICENSE file for details.

## Support

For issues, questions, or contributions, please visit the project repository or contact support@notifyafrica.com.

## Changelog

### Version 1.0.0
- Initial release matching Node.js SDK structure
- Support for sending single and batch SMS messages
- Message status checking functionality
- Comprehensive error handling
