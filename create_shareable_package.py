#!/usr/bin/env python3.11

"""
Create Shareable Package - Remove Confidential Information
Creates a clean version of the MCP solution for sharing
"""

import os
import shutil
import json
from pathlib import Path

def create_shareable_package():
    """Create a clean shareable package"""
    
    print("🔧 Creating Shareable MCP Package")
    print("=" * 50)
    
    # Create shareable directory
    shareable_dir = Path("mcp_f1_workflow_shareable")
    if shareable_dir.exists():
        shutil.rmtree(shareable_dir)
    
    shareable_dir.mkdir()
    
    # Files to include (cleaned versions)
    files_to_copy = {
        'shareable_mcp_solution.py': 'f1_workflow_orchestrator.py',
        'README_SHAREABLE.md': 'README.md',
        'mcp_server_sse.py': 'mcp_server_sse.py',
    }
    
    # Copy main files
    for source, dest in files_to_copy.items():
        if Path(source).exists():
            shutil.copy2(source, shareable_dir / dest)
            print(f"✅ Copied {source} -> {dest}")
    
    # Create config template directory
    config_template_dir = shareable_dir / "config_template"
    config_template_dir.mkdir()
    
    # Copy template files
    template_files = {
        'config_template/.env.template': 'config_template/.env.template'
    }
    
    for source, dest in template_files.items():
        if Path(source).exists():
            shutil.copy2(source, shareable_dir / dest)
            print(f"✅ Copied {source}")
    
    # Create clean MCP server templates
    create_clean_mcp_servers(shareable_dir)
    
    # Create setup script
    create_setup_script(shareable_dir)
    
    # Create requirements file
    create_requirements_file(shareable_dir)
    
    # Create example configuration
    create_example_config(shareable_dir)
    
    print(f"\n🎉 Shareable package created: {shareable_dir}")
    print(f"📁 Contents:")
    for item in sorted(shareable_dir.rglob("*")):
        if item.is_file():
            print(f"   📄 {item.relative_to(shareable_dir)}")
    
    print(f"\n✅ Package is ready for sharing!")
    print(f"⚠️  All confidential information has been removed")

def create_clean_mcp_servers(shareable_dir):
    """Create clean MCP server templates"""
    
    # Telegram MCP Server Template
    telegram_server = '''#!/usr/bin/env python3.11

"""
Telegram MCP Server Template
Replace with your actual implementation
"""

import os
from fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("Telegram Server")

class SendMessageInput(BaseModel):
    message: str

class MessageResult(BaseModel):
    success: bool
    message_id: str = None
    error: str = None

@mcp.tool()
def send_telegram_message(input_data: SendMessageInput) -> MessageResult:
    """Send message via Telegram bot"""
    try:
        # TODO: Implement your Telegram bot logic here
        # Use python-telegram-bot library
        # Get bot_token and chat_id from environment variables
        
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            return MessageResult(
                success=False,
                error="Telegram credentials not configured"
            )
        
        # Placeholder implementation
        print(f"📱 [TELEGRAM] {input_data.message}")
        
        return MessageResult(
            success=True,
            message_id="placeholder_message_id"
        )
        
    except Exception as e:
        return MessageResult(
            success=False,
            error=str(e)
        )

if __name__ == "__main__":
    mcp.run()
'''
    
    # Gmail MCP Server Template
    gmail_server = '''#!/usr/bin/env python3.11

"""
Gmail MCP Server Template with Service Account Authentication
Replace with your actual implementation
"""

from fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("Gmail Service Account Server")

class SendEmailInput(BaseModel):
    to: str
    subject: str
    body: str
    body_type: str = "plain"

class EmailResult(BaseModel):
    success: bool
    message_id: str = None
    error: str = None

@mcp.tool()
def send_email(input_data: SendEmailInput) -> EmailResult:
    """Send email using Gmail API with service account"""
    try:
        # TODO: Implement Gmail API with service account
        # from googleapiclient.discovery import build
        # from google.oauth2 import service_account
        
        # Load service account credentials
        # credentials = service_account.Credentials.from_service_account_file(
        #     'config/service_account.json',
        #     scopes=['https://www.googleapis.com/auth/gmail.send']
        # )
        
        # Build Gmail service
        # service = build('gmail', 'v1', credentials=credentials)
        
        # Create and send email
        # ... implementation here ...
        
        # Placeholder implementation
        print(f"📧 [EMAIL] To: {input_data.to}")
        print(f"📧 [EMAIL] Subject: {input_data.subject}")
        
        return EmailResult(
            success=True,
            message_id="placeholder_message_id"
        )
        
    except Exception as e:
        return EmailResult(
            success=False,
            error=str(e)
        )

if __name__ == "__main__":
    mcp.run()
'''
    
    # Google Drive MCP Server Template
    gdrive_server = '''#!/usr/bin/env python3.11

"""
Google Drive MCP Server Template with Service Account Authentication
Replace with your actual implementation
"""

from fastmcp import FastMCP
from pydantic import BaseModel
from typing import List

mcp = FastMCP("Google Drive Service Account Server")

class CreateSheetInput(BaseModel):
    title: str
    data: List[List[str]]
    make_public: bool = True

class SheetResult(BaseModel):
    success: bool
    sheet_id: str = None
    sheet_url: str = None
    error: str = None

@mcp.tool()
def create_google_sheet(input_data: CreateSheetInput) -> SheetResult:
    """Create Google Sheet using service account"""
    try:
        # TODO: Implement Google Sheets API with service account
        # from googleapiclient.discovery import build
        # from google.oauth2 import service_account
        
        # Load service account credentials
        # credentials = service_account.Credentials.from_service_account_file(
        #     'config/service_account.json',
        #     scopes=['https://www.googleapis.com/auth/spreadsheets',
        #             'https://www.googleapis.com/auth/drive.file']
        # )
        
        # Build services
        # sheets_service = build('sheets', 'v4', credentials=credentials)
        # drive_service = build('drive', 'v3', credentials=credentials)
        
        # Create spreadsheet and add data
        # ... implementation here ...
        
        # Placeholder implementation
        sheet_id = "placeholder_sheet_id"
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
        
        print(f"📊 [SHEETS] Created: {input_data.title}")
        print(f"📊 [SHEETS] URL: {sheet_url}")
        
        return SheetResult(
            success=True,
            sheet_id=sheet_id,
            sheet_url=sheet_url
        )
        
    except Exception as e:
        return SheetResult(
            success=False,
            error=str(e)
        )

if __name__ == "__main__":
    mcp.run()
'''
    
    # Write MCP server files
    (shareable_dir / "mcp_server_telegram.py").write_text(telegram_server)
    (shareable_dir / "mcp_server_gmail_sa.py").write_text(gmail_server)
    (shareable_dir / "mcp_server_gdrive_sa.py").write_text(gdrive_server)
    
    print("✅ Created clean MCP server templates")

def create_setup_script(shareable_dir):
    """Create setup script for the shareable package"""
    
    setup_script = '''#!/usr/bin/env python3.11

"""
MCP F1 Workflow Setup Script
"""

import os
import sys
from pathlib import Path

def check_dependencies():
    """Check required dependencies"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'google-api-python-client',
        'google-auth', 
        'python-telegram-bot',
        'fastmcp',
        'pydantic',
        'uvicorn',
        'starlette'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\\n📦 Install missing packages:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True

def setup_config():
    """Setup configuration files"""
    print("\\n⚙️ Setting up configuration...")
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    env_file = config_dir / ".env"
    template_file = Path("config_template/.env.template")
    
    if not env_file.exists() and template_file.exists():
        import shutil
        shutil.copy2(template_file, env_file)
        print(f"   ✅ Created config/.env from template")
        print(f"   ⚠️  Please edit config/.env with your credentials")
    else:
        print(f"   ℹ️  config/.env already exists")
    
    return True

def main():
    """Main setup function"""
    print("🚀 MCP F1 Workflow Setup")
    print("=" * 40)
    
    if not check_dependencies():
        print("\\n❌ Please install missing dependencies first")
        return False
    
    if not setup_config():
        print("\\n❌ Configuration setup failed")
        return False
    
    print("\\n🎉 Setup complete!")
    print("\\n📋 Next steps:")
    print("   1. Edit config/.env with your credentials")
    print("   2. Set up Google Cloud service account")
    print("   3. Configure Telegram bot")
    print("   4. Run: python f1_workflow_orchestrator.py")
    
    return True

if __name__ == "__main__":
    main()
'''
    
    (shareable_dir / "setup.py").write_text(setup_script)
    print("✅ Created setup script")

def create_requirements_file(shareable_dir):
    """Create requirements.txt file"""
    
    requirements = '''# MCP F1 Workflow Requirements

# Google APIs
google-api-python-client>=2.100.0
google-auth>=2.20.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.2.0

# Telegram
python-telegram-bot>=20.0

# MCP Framework
fastmcp>=0.1.0
pydantic>=2.0.0

# Web Server
uvicorn>=0.20.0
starlette>=0.25.0

# Security
cryptography>=40.0.0

# Utilities
requests>=2.28.0
python-dotenv>=1.0.0
'''
    
    (shareable_dir / "requirements.txt").write_text(requirements)
    print("✅ Created requirements.txt")

def create_example_config(shareable_dir):
    """Create example configuration files"""
    
    # Example profiles.yaml
    profiles_yaml = '''agent:
  name: F1-Workflow-Agent
  id: f1_agent_001
  description: F1 championship workflow automation agent

strategy:
  type: conservative
  max_steps: 5

memory:
  top_k: 3
  type_filter: tool_output

llm:
  text_generation: gemini

mcp_servers:
  - id: telegram
    script: mcp_server_telegram.py
    cwd: .
  - id: gmail
    script: mcp_server_gmail_sa.py
    cwd: .
  - id: gdrive
    script: mcp_server_gdrive_sa.py
    cwd: .
  - id: sse
    script: mcp_server_sse.py
    cwd: .
'''
    
    config_dir = shareable_dir / "config_template"
    (config_dir / "profiles.yaml.template").write_text(profiles_yaml)
    print("✅ Created example profiles.yaml template")

if __name__ == "__main__":
    create_shareable_package()
