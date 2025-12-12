"""
Data models for Notify Africa SDK
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any


# Request Models
@dataclass
class SendSingleRequest:
    """
    Request to send a single SMS message.
    
    Attributes:
        phone_number: Recipient phone number (usually E.164 format).
        message: Message body to send.
        sender_id: Identifier of the sender (alphanumeric short name).
    """
    phone_number: str
    message: str
    sender_id: str


@dataclass
class SendBatchRequest:
    """
    Request to send the same message to multiple recipients in a single batch.
    
    Attributes:
        phone_numbers: Array of recipient phone numbers.
        message: Message body to send to all recipients.
        sender_id: Identifier of the sender.
    """
    phone_numbers: List[str]
    message: str
    sender_id: str


# Response Models
@dataclass
class SendSingleResponse:
    """
    Response returned after attempting to send a single message.
    
    Attributes:
        messageId: Unique identifier assigned to the message by the provider.
        status: Processing or delivery status (e.g. "queued", "sent", "failed").
    """
    messageId: str
    status: str


@dataclass
class SendBatchResponse:
    """
    Response returned after sending a batch of messages.
    
    Attributes:
        messageCount: Number of messages attempted or sent.
        creditsDeducted: Credits used for the batch send.
        remainingBalance: Remaining account balance or credits.
    """
    messageCount: int
    creditsDeducted: int
    remainingBalance: int


@dataclass
class MessageStatusResponse:
    """
    Status information for a previously sent message.
    
    Attributes:
        messageId: Unique identifier of the message.
        status: Current delivery or processing status.
        sentAt: ISO8601 timestamp when the message was sent, or None if not sent.
        deliveredAt: ISO8601 timestamp when the message was delivered, or None if not delivered.
    """
    messageId: str
    status: str
    sentAt: Optional[str] = None
    deliveredAt: Optional[str] = None


# Legacy models for backward compatibility
@dataclass
class SMSResponse:
    """Response model for SMS operations (legacy)"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    status_code: Optional[int] = None
    balance: Optional[float] = None
    credits_spent: Optional[int] = None
    sms_id: Optional[str] = None


@dataclass
class BulkSMSResponse:
    """Response model for bulk SMS operations (legacy)"""
    success: bool
    message: str
    total_messages: int
    successful_messages: int
    failed_messages: int
    balance: Optional[float] = None
    total_credits: Optional[int] = None
    messages: Optional[List[Dict[str, Any]]] = None


@dataclass
class DeliveryStatus:
    """Delivery status model (legacy)"""
    sms_id: str
    recipient: str
    status: str
    status_description: str
    delivered_at: Optional[datetime] = None
    credits: Optional[int] = None


@dataclass
class SenderID:
    """Sender ID model"""
    id: int
    name: str
    status: str
    purpose: str
    access: str
    created_at: datetime