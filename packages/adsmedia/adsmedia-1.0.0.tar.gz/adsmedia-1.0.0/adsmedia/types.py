"""Type definitions for ADSMedia SDK"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class SendEmailOptions:
    """Options for sending a single email"""
    to: str
    subject: str
    html: Optional[str] = None
    text: Optional[str] = None
    to_name: Optional[str] = None
    type: Optional[int] = None  # 1=HTML+text, 2=HTML only, 3=text only
    from_name: Optional[str] = None
    reply_to: Optional[str] = None
    server_id: Optional[int] = None
    unsubscribe_url: Optional[str] = None


@dataclass
class BatchRecipient:
    """Recipient for batch sending"""
    email: str
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    custom1: Optional[str] = None
    custom2: Optional[str] = None


@dataclass
class SendBatchOptions:
    """Options for batch sending"""
    recipients: List[BatchRecipient]
    subject: str
    html: str
    text: Optional[str] = None
    preheader: Optional[str] = None
    from_name: Optional[str] = None
    server_id: Optional[int] = None


@dataclass
class Campaign:
    """Campaign model"""
    id: int
    name: str
    subject: str
    html: str
    text: Optional[str] = None
    preheader: Optional[str] = None
    type: int = 1
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class ContactList:
    """Contact list model"""
    id: int
    name: str
    type: int
    count: int
    created_at: Optional[str] = None


@dataclass
class Contact:
    """Contact model"""
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    custom1: Optional[str] = None
    custom2: Optional[str] = None


@dataclass
class Schedule:
    """Schedule/Task model"""
    id: int
    campaign_id: int
    list_id: int
    server_id: int
    sender_name: Optional[str] = None
    scheduled_at: Optional[str] = None
    status: str = "queue"
    created_at: Optional[str] = None


@dataclass
class Server:
    """Server model"""
    id: int
    domain: str
    status: str
    daily_limit: int
    sent_today: int


@dataclass
class Stats:
    """Statistics model"""
    sent: int = 0
    delivered: int = 0
    opens: int = 0
    clicks: int = 0
    bounces: int = 0
    unsubscribes: int = 0
    complaints: int = 0

