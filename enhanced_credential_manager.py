#!/usr/bin/env python3.11

"""
Enhanced Credential Manager - Distinguished Engineer Solution
Secure, scalable credential management for MCP servers
"""

import os
import json
import base64
from pathlib import Path
from typing import Dict, Optional, Any
from cryptography.fernet import Fernet
from google.oauth2 import service_account
from google.auth.transport.requests import Request

class SecureCredentialManager:
    """Enterprise-grade credential management"""
    
    def __init__(self):
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)
        self.env_file = self.config_dir / ".env"
        self.service_account_file = self.config_dir / "service_account.json"
        self._encryption_key = self._get_or_create_encryption_key()
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for sensitive data"""
        key_file = self.config_dir / ".encryption_key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            # Make key file read-only
            os.chmod(key_file, 0o600)
            return key
    
    def encrypt_credential(self, value: str) -> str:
        """Encrypt sensitive credential"""
        f = Fernet(self._encryption_key)
        encrypted = f.encrypt(value.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_credential(self, encrypted_value: str) -> str:
        """Decrypt sensitive credential"""
        f = Fernet(self._encryption_key)
        encrypted_bytes = base64.b64decode(encrypted_value.encode())
        return f.decrypt(encrypted_bytes).decode()
    
    def set_service_account_credentials(self, service_account_json_path: str) -> bool:
        """Set service account credentials"""
        try:
            import shutil
            source_path = Path(service_account_json_path)
            
            if not source_path.exists():
                print(f"❌ Service account file not found: {service_account_json_path}")
                return False
            
            # Copy and secure the service account file
            shutil.copy2(source_path, self.service_account_file)
            os.chmod(self.service_account_file, 0o600)
            
            # Validate the service account
            with open(self.service_account_file, 'r') as f:
                sa_data = json.load(f)
            
            required_fields = ['type', 'project_id', 'private_key', 'client_email']
            if not all(field in sa_data for field in required_fields):
                print(f"❌ Invalid service account file format")
                return False
            
            print(f"✅ Service account configured: {sa_data['client_email']}")
            
            # Update environment
            self._update_env_var('USE_SERVICE_ACCOUNT', 'true')
            self._update_env_var('SERVICE_ACCOUNT_FILE', str(self.service_account_file))
            
            return True
            
        except Exception as e:
            print(f"❌ Error setting service account: {e}")
            return False
    
    def get_service_account_credentials(self) -> Optional[service_account.Credentials]:
        """Get service account credentials"""
        try:
            if not self.service_account_file.exists():
                return None
            
            scopes = [
                'https://www.googleapis.com/auth/gmail.send',
                'https://www.googleapis.com/auth/gmail.readonly',
                'https://www.googleapis.com/auth/drive.file',
                'https://www.googleapis.com/auth/spreadsheets'
            ]
            
            credentials = service_account.Credentials.from_service_account_file(
                str(self.service_account_file), scopes=scopes
            )
            
            return credentials
            
        except Exception as e:
            print(f"❌ Error loading service account: {e}")
            return None
    
    def _update_env_var(self, key: str, value: str):
        """Update environment variable in .env file"""
        env_content = ""
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                env_content = f.read()
        
        # Update or add the variable
        lines = env_content.split('\n')
        updated = False
        
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}"
                updated = True
                break
        
        if not updated:
            lines.append(f"{key}={value}")
        
        with open(self.env_file, 'w') as f:
            f.write('\n'.join(lines))
    
    def get_telegram_credentials(self) -> Dict[str, str]:
        """Get Telegram credentials"""
        return {
            'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
            'chat_id': os.getenv('TELEGRAM_CHAT_ID', '')
        }
    
    def validate_all_credentials(self) -> Dict[str, bool]:
        """Validate all credential configurations"""
        validation = {}
        
        # Service Account
        sa_creds = self.get_service_account_credentials()
        validation['service_account'] = sa_creds is not None
        
        # Telegram
        tg_creds = self.get_telegram_credentials()
        validation['telegram'] = bool(tg_creds['bot_token'] and tg_creds['chat_id'])
        
        return validation

# Global instance
credential_manager = SecureCredentialManager()
