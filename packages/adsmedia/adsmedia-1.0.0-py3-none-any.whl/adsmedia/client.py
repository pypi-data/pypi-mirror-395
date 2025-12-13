"""ADSMedia API Client"""

import requests
from typing import Optional, List, Dict, Any, Union
from urllib.parse import urlencode

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


class ADSMediaError(Exception):
    """ADSMedia API Error"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ADSMedia:
    """
    ADSMedia Email API Client
    
    Example:
        client = ADSMedia(api_key='your-api-key')
        result = client.send(to='user@example.com', subject='Hello', html='<h1>Hi!</h1>')
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.adsmedia.live/v1",
        timeout: int = 30
    ):
        if not api_key:
            raise ValueError("API key is required")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make API request"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                timeout=self.timeout,
            )
            
            data = response.json()
            
            if not response.ok:
                error_msg = data.get("error", {}).get("message", f"HTTP {response.status_code}")
                raise ADSMediaError(error_msg, response.status_code)
            
            if not data.get("success", True):
                raise ADSMediaError(data.get("error", "Unknown error"))
            
            return data.get("data", data)
            
        except requests.exceptions.Timeout:
            raise ADSMediaError("Request timeout", 408)
        except requests.exceptions.RequestException as e:
            raise ADSMediaError(str(e))
    
    # ===== Connection =====
    
    def ping(self) -> Dict[str, Any]:
        """Test API connectivity and authentication"""
        return self._request("GET", "/ping")
    
    # ===== Email =====
    
    def send(
        self,
        to: str,
        subject: str,
        html: Optional[str] = None,
        text: Optional[str] = None,
        to_name: Optional[str] = None,
        type: Optional[int] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        server_id: Optional[int] = None,
        unsubscribe_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send a single transactional email
        
        Args:
            to: Recipient email address
            subject: Email subject line
            html: HTML content
            text: Plain text version
            to_name: Recipient name
            type: 1=HTML+text, 2=HTML only, 3=text only
            from_name: Sender display name
            reply_to: Reply-to email address
            server_id: Specific server ID
            unsubscribe_url: URL for List-Unsubscribe header
            
        Returns:
            dict with message_id, send_id, status
        """
        body = {"to": to, "subject": subject}
        
        if html: body["html"] = html
        if text: body["text"] = text
        if to_name: body["to_name"] = to_name
        if type: body["type"] = type
        if from_name: body["from_name"] = from_name
        if reply_to: body["reply_to"] = reply_to
        if server_id: body["server_id"] = server_id
        if unsubscribe_url: body["unsubscribe_url"] = unsubscribe_url
        
        return self._request("POST", "/send", json=body)
    
    def send_batch(
        self,
        recipients: List[Union[Dict[str, str], BatchRecipient]],
        subject: str,
        html: str,
        text: Optional[str] = None,
        preheader: Optional[str] = None,
        from_name: Optional[str] = None,
        server_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Send batch marketing emails (up to 1000)
        
        Args:
            recipients: List of recipients [{email, name?}]
            subject: Email subject (supports %%First Name%% etc)
            html: HTML content
            text: Plain text version
            preheader: Email preheader
            from_name: Sender display name
            server_id: Specific server ID
            
        Returns:
            dict with task_id, queued count
        """
        # Convert BatchRecipient to dict if needed
        recipient_list = []
        for r in recipients:
            if isinstance(r, BatchRecipient):
                recipient_list.append({
                    "email": r.email,
                    "name": r.name,
                })
            else:
                recipient_list.append(r)
        
        body = {
            "recipients": recipient_list,
            "subject": subject,
            "html": html,
        }
        
        if text: body["text"] = text
        if preheader: body["preheader"] = preheader
        if from_name: body["from_name"] = from_name
        if server_id: body["server_id"] = server_id
        
        return self._request("POST", "/send/batch", json=body)
    
    def get_status(
        self,
        message_id: Optional[str] = None,
        send_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get email delivery status"""
        params = {}
        if message_id:
            params["message_id"] = message_id
        elif send_id:
            params["id"] = send_id
        else:
            raise ValueError("Either message_id or send_id is required")
        
        return self._request("GET", "/send/status", params=params)
    
    # ===== Campaigns =====
    
    def get_campaigns(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all campaigns"""
        return self._request("GET", "/campaigns", params={"limit": limit, "offset": offset})
    
    def get_campaign(self, id: int) -> Dict[str, Any]:
        """Get a specific campaign"""
        return self._request("GET", "/campaigns/get", params={"id": id})
    
    def create_campaign(
        self,
        name: str,
        subject: str,
        html: str,
        text: Optional[str] = None,
        preheader: Optional[str] = None,
        type: int = 1,
    ) -> Dict[str, Any]:
        """Create a new campaign"""
        body = {"name": name, "subject": subject, "html": html, "type": type}
        if text: body["text"] = text
        if preheader: body["preheader"] = preheader
        return self._request("POST", "/campaigns/create", json=body)
    
    def update_campaign(self, id: int, **kwargs) -> Dict[str, Any]:
        """Update a campaign"""
        return self._request("POST", f"/campaigns/update", params={"id": id}, json=kwargs)
    
    def delete_campaign(self, id: int) -> Dict[str, Any]:
        """Delete a campaign"""
        return self._request("DELETE", "/campaigns/delete", params={"id": id})
    
    # ===== Lists =====
    
    def get_lists(self) -> List[Dict[str, Any]]:
        """Get all lists"""
        return self._request("GET", "/lists")
    
    def get_list(self, id: int) -> Dict[str, Any]:
        """Get a specific list"""
        return self._request("GET", "/lists/get", params={"id": id})
    
    def create_list(self, name: str, type: int = 1) -> Dict[str, Any]:
        """Create a new list (type: 1=email, 3=phone)"""
        return self._request("POST", "/lists/create", json={"name": name, "type": type})
    
    def delete_list(self, id: int) -> Dict[str, Any]:
        """Delete a list"""
        return self._request("DELETE", "/lists/delete", params={"id": id})
    
    def split_list(self, id: int, max_size: int = 35000) -> Dict[str, Any]:
        """Split a large list into smaller ones"""
        return self._request("POST", "/lists/split", params={"id": id}, json={"max_size": max_size})
    
    # ===== Contacts =====
    
    def get_contacts(self, list_id: int, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get contacts from a list"""
        return self._request("GET", "/lists/contacts", params={
            "id": list_id, "limit": limit, "offset": offset
        })
    
    def add_contacts(self, list_id: int, contacts: List[Union[Dict[str, str], Contact]]) -> Dict[str, Any]:
        """Add contacts to a list"""
        contact_list = []
        for c in contacts:
            if isinstance(c, Contact):
                contact_list.append({
                    "email": c.email,
                    "firstName": c.first_name,
                    "lastName": c.last_name,
                    "custom1": c.custom1,
                    "custom2": c.custom2,
                })
            else:
                contact_list.append(c)
        
        return self._request("POST", "/lists/contacts/add", params={"id": list_id}, json={"contacts": contact_list})
    
    def remove_contacts(self, list_id: int, emails: List[str]) -> Dict[str, Any]:
        """Remove contacts from a list"""
        return self._request("DELETE", "/lists/contacts/delete", params={"id": list_id}, json={"emails": emails})
    
    # ===== Schedules =====
    
    def get_schedules(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all schedules (status: queue, prep, sending, done, paused)"""
        params = {"status": status} if status else {}
        return self._request("GET", "/schedules", params=params)
    
    def create_schedule(
        self,
        campaign_id: int,
        list_id: int,
        server_id: int,
        sender_name: Optional[str] = None,
        schedule: Optional[str] = None,  # YYYY-MM-DD HH:MM:SS
    ) -> Dict[str, Any]:
        """Create a sending task"""
        body = {
            "campaign_id": campaign_id,
            "list_id": list_id,
            "server_id": server_id,
        }
        if sender_name: body["sender_name"] = sender_name
        if schedule: body["schedule"] = schedule
        return self._request("POST", "/schedules/create", json=body)
    
    def update_schedule(
        self,
        id: int,
        sender_name: Optional[str] = None,
        schedule: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update schedule sender name or datetime"""
        body = {}
        if sender_name: body["sender_name"] = sender_name
        if schedule: body["schedule"] = schedule
        return self._request("PUT", "/schedules/update", params={"id": id}, json=body)
    
    def pause_schedule(self, id: int) -> Dict[str, Any]:
        """Pause a schedule"""
        return self._request("POST", "/schedules/pause", params={"id": id})
    
    def resume_schedule(self, id: int) -> Dict[str, Any]:
        """Resume a schedule"""
        return self._request("POST", "/schedules/resume", params={"id": id})
    
    def stop_schedule(self, id: int) -> Dict[str, Any]:
        """Stop and delete a schedule"""
        return self._request("DELETE", "/schedules/stop", params={"id": id})
    
    # ===== Servers =====
    
    def get_servers(self) -> List[Dict[str, Any]]:
        """Get all servers"""
        return self._request("GET", "/servers")
    
    def get_server(self, id: int) -> Dict[str, Any]:
        """Get a specific server"""
        return self._request("GET", "/servers/get", params={"id": id})
    
    def verify_domain(self, server_id: int) -> Dict[str, Any]:
        """Verify domain DNS (SPF, DKIM, DMARC, etc)"""
        return self._request("GET", "/domains/verify", params={"server_id": server_id})
    
    # ===== Statistics =====
    
    def get_overview_stats(self) -> Dict[str, Any]:
        """Get overall statistics"""
        return self._request("GET", "/stats/overview")
    
    def get_campaign_stats(self, task_id: int) -> Dict[str, Any]:
        """Get campaign/task statistics"""
        return self._request("GET", "/stats/campaign", params={"id": task_id})
    
    def get_hourly_stats(self, task_id: int) -> Dict[str, Any]:
        """Get hourly breakdown"""
        return self._request("GET", "/stats/hourly", params={"id": task_id})
    
    def get_daily_stats(self, task_id: int) -> Dict[str, Any]:
        """Get daily breakdown"""
        return self._request("GET", "/stats/daily", params={"id": task_id})
    
    def get_country_stats(self, task_id: int) -> Dict[str, Any]:
        """Get geographic stats"""
        return self._request("GET", "/stats/countries", params={"id": task_id})
    
    def get_provider_stats(self, task_id: int) -> Dict[str, Any]:
        """Get provider breakdown (Gmail, Outlook, etc)"""
        return self._request("GET", "/stats/providers", params={"id": task_id})
    
    def get_bounce_details(self, task_id: int) -> List[Dict[str, Any]]:
        """Get bounce details"""
        return self._request("GET", "/stats/bounces", params={"id": task_id})
    
    def get_events(
        self,
        task_id: int,
        type: Optional[str] = None,  # open, click, bounce, unsubscribe, sent
        email: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Get events for a task"""
        params = {"id": task_id, "limit": limit, "offset": offset}
        if type: params["type"] = type
        if email: params["email"] = email
        return self._request("GET", "/stats/events", params=params)
    
    # ===== Suppression =====
    
    def check_suppression(self, email: str) -> Dict[str, Any]:
        """Check if email is suppressed"""
        return self._request("GET", "/suppressions/check", params={"email": email})
    
    # ===== Account =====
    
    def get_account(self) -> Dict[str, Any]:
        """Get account information"""
        return self._request("GET", "/account")
    
    def get_usage(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return self._request("GET", "/account/usage")

