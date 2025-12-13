# adsmedia

Official Python SDK for ADSMedia Email API.

## Installation

```bash
pip install adsmedia
```

## Quick Start

```python
from adsmedia import ADSMedia

client = ADSMedia(api_key='your-api-key')

# Test connection
result = client.ping()
print(f"API is working! User ID: {result['userId']}")

# Send a single email
result = client.send(
    to='recipient@example.com',
    subject='Hello!',
    html='<h1>Welcome!</h1>',
)
print(f"Email sent! Message ID: {result['message_id']}")
```

## Features

- ✅ Full API coverage
- ✅ Type hints for IDE support
- ✅ Simple, Pythonic interface
- ✅ Automatic error handling
- ✅ Supports Python 3.8+

## Usage Examples

### Send Single Email (Transactional)

```python
result = client.send(
    to='user@example.com',
    to_name='John Doe',
    subject='Welcome to our service!',
    html='<h1>Hello John!</h1><p>Thanks for signing up.</p>',
    text='Hello John! Thanks for signing up.',
    from_name='Support Team',
    reply_to='support@yourcompany.com',
)
```

### Send Batch Emails (Marketing)

```python
result = client.send_batch(
    recipients=[
        {'email': 'user1@example.com', 'name': 'User 1'},
        {'email': 'user2@example.com', 'name': 'User 2'},
    ],
    subject='Hello %%First Name%%!',
    html='<h1>Hi %%First Name%%!</h1><p>Check out our latest offers.</p>',
    preheader='Exclusive deals inside',
    from_name='Marketing Team',
)
print(f"Queued {result['recipients_count']} emails. Task ID: {result['task_id']}")
```

### Campaign Management

```python
# Create a campaign
campaign = client.create_campaign(
    name='Newsletter Q1 2025',
    subject='Monthly Update',
    html='<h1>Newsletter</h1><p>Latest news...</p>',
    preheader='Your monthly update is here',
)

# Get all campaigns
campaigns = client.get_campaigns()

# Update a campaign
client.update_campaign(campaign['id'], subject='Updated Subject')

# Delete a campaign
client.delete_campaign(campaign['id'])
```

### Contact Lists

```python
# Create a list
list_result = client.create_list(name='Newsletter Subscribers')

# Add contacts
client.add_contacts(list_result['id'], [
    {'email': 'john@example.com', 'firstName': 'John', 'lastName': 'Doe'},
    {'email': 'jane@example.com', 'firstName': 'Jane', 'lastName': 'Smith'},
])

# Get contacts
contacts = client.get_contacts(list_result['id'], limit=100)

# Split large list
client.split_list(list_result['id'], max_size=35000)

# Remove contacts
client.remove_contacts(list_result['id'], ['john@example.com'])
```

### Schedule Sending

```python
# Create a schedule
schedule = client.create_schedule(
    campaign_id=45,
    list_id=123,
    server_id=1,
    sender_name='John from Company',
    schedule='2025-12-15 10:00:00',
)

# Update schedule
client.update_schedule(schedule['id'], sender_name='New Name')

# Pause/Resume/Stop
client.pause_schedule(schedule['id'])
client.resume_schedule(schedule['id'])
client.stop_schedule(schedule['id'])
```

### Statistics

```python
# Get overview stats
overview = client.get_overview_stats()
print(f"Total sent: {overview['sent']}, Opens: {overview['opens']}")

# Get campaign-specific stats
stats = client.get_campaign_stats(task_id=123)

# Get geographic stats
countries = client.get_country_stats(task_id=123)

# Get provider breakdown
providers = client.get_provider_stats(task_id=123)

# Get bounce details
bounces = client.get_bounce_details(task_id=123)

# Get events
opens = client.get_events(task_id=123, type='open', limit=100)
```

### Domain Verification

```python
verification = client.verify_domain(server_id=1)
print(f"SPF: {verification['checks']['spf']['status']}")
print(f"DKIM: {verification['checks']['dkim']['status']}")
print(f"DMARC: {verification['checks']['dmarc']['status']}")
```

### Suppression Check

```python
result = client.check_suppression('user@example.com')
if result.get('suppressed'):
    print(f"Email is suppressed: {result['reason']}")
```

## Error Handling

```python
from adsmedia import ADSMedia, ADSMediaError

client = ADSMedia(api_key='your-api-key')

try:
    result = client.send(to='invalid', subject='Test', html='<p>Test</p>')
except ADSMediaError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
```

## Configuration

```python
client = ADSMedia(
    api_key='your-api-key',      # Required
    base_url='https://api.adsmedia.live/v1',  # Optional
    timeout=30,                   # Optional: request timeout in seconds
)
```

## Personalization Placeholders

Use these in subject and HTML content:

| Placeholder | Description |
|-------------|-------------|
| `%%First Name%%` | Recipient's first name |
| `%%Last Name%%` | Recipient's last name |
| `%%emailaddress%%` | Recipient's email |
| `%%Sender Name%%` | Sender display name |
| `%%unsubscribelink%%` | Unsubscribe URL |
| `%%webversion%%` | View in browser link |

## Links

- [API Documentation](https://www.adsmedia.ai/api-docs)
- [GitHub Repository](https://github.com/ADSMedia-ai/ADSMedia)
- [Report Issues](https://github.com/ADSMedia-ai/ADSMedia/issues)

## License

MIT © [ADSMedia](https://www.adsmedia.ai)

