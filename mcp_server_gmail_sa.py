#!/usr/bin/env python3.11

"""
Gmail MCP Server with Service Account Authentication
Distinguished Engineer Implementation
"""

import sys
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import asyncio

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastmcp import FastMCP
from enhanced_credential_manager import credential_manager

# Initialize MCP server
mcp = FastMCP("Gmail Service Account Server")

class SendEmailInput(BaseModel):
    to: str
    subject: str
    body: str
    body_type: str = "plain"  # "plain" or "html"

class EmailResult(BaseModel):
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None

@mcp.tool()
def send_email(input_data: SendEmailInput) -> EmailResult:
    """Send email using Gmail API with service account authentication"""
    try:
        from googleapiclient.discovery import build
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        import base64
        
        # Get service account credentials
        credentials = credential_manager.get_service_account_credentials()
        if not credentials:
            return EmailResult(
                success=False,
                error="Service account credentials not configured"
            )
        
        # Build Gmail service
        service = build('gmail', 'v1', credentials=credentials)
        
        # Create message
        if input_data.body_type == "html":
            message = MIMEMultipart('alternative')
            message['to'] = input_data.to
            message['subject'] = input_data.subject
            
            html_part = MIMEText(input_data.body, 'html')
            message.attach(html_part)
        else:
            message = MIMEText(input_data.body)
            message['to'] = input_data.to
            message['subject'] = input_data.subject
        
        # Set from address to service account email
        with open(credential_manager.service_account_file, 'r') as f:
            import json
            sa_data = json.load(f)
            message['from'] = sa_data['client_email']
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        # Send email
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        return EmailResult(
            success=True,
            message_id=result.get('id'),
            error=None
        )
        
    except Exception as e:
        return EmailResult(
            success=False,
            error=f"Failed to send email: {str(e)}"
        )

@mcp.tool()
def get_recent_emails(count: int = 10) -> Dict[str, Any]:
    """Get recent emails from Gmail"""
    try:
        from googleapiclient.discovery import build
        
        credentials = credential_manager.get_service_account_credentials()
        if not credentials:
            return {"success": False, "error": "Service account not configured"}
        
        service = build('gmail', 'v1', credentials=credentials)
        
        # Get message list
        results = service.users().messages().list(
            userId='me', maxResults=count
        ).execute()
        
        messages = results.get('messages', [])
        
        email_list = []
        for msg in messages[:count]:
            # Get message details
            message = service.users().messages().get(
                userId='me', id=msg['id']
            ).execute()
            
            headers = message['payload'].get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
            
            email_list.append({
                'id': msg['id'],
                'subject': subject,
                'from': sender,
                'date': date
            })
        
        return {
            "success": True,
            "emails": email_list,
            "count": len(email_list)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    mcp.run()
