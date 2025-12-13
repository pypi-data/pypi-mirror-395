"""
ADSMedia Email API SDK for Python
Official Python SDK for ADSMedia Email API

Example usage:
    from adsmedia import ADSMedia
    
    client = ADSMedia(api_key='your-api-key')
    result = client.send(
        to='user@example.com',
        subject='Hello!',
        html='<h1>Welcome!</h1>'
    )
"""

from .client import ADSMedia, ADSMediaError
from .types import (
    SendEmailOptions,
    BatchRecipient,
    SendBatchOptions,
    Campaign,
    ContactList,
    Contact,
    Schedule,
    Server,
    Stats,
)

__version__ = "1.0.0"
__all__ = [
    "ADSMedia",
    "ADSMediaError",
    "SendEmailOptions",
    "BatchRecipient", 
    "SendBatchOptions",
    "Campaign",
    "ContactList",
    "Contact",
    "Schedule",
    "Server",
    "Stats",
]

