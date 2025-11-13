#!/usr/bin/env python3.11

"""
Fix client ID mismatch between JSON and .env files
"""

import json
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_client_mismatch():
    """Fix the mismatch between JSON client ID and .env client ID"""
    print("🔧 Fix Client ID Mismatch")
    print("=" * 50)
    
    try:
        # Get current .env credentials
        from config.credentials import credentials
        gmail_creds = credentials.get_gmail_credentials()
        
        # Get JSON client ID
        json_file = Path("/Users/gowtham/Downloads/client_secret_172398610094-1q78cjhmops1ompbj02nasn54l90qo4i.apps.googleusercontent.com.json")
        
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        json_client_id = data['installed']['client_id']
        
        print("🔍 Current situation:")
        print(f"   JSON Client ID: {json_client_id}")
        print(f"   .env Client ID: {gmail_creds['client_id']}")
        print(f"   .env Client Secret: {'✅ SET' if gmail_creds['client_secret'] else '❌ NOT SET'}")
        
        if gmail_creds['client_id'] != json_client_id:
            print(f"\n❌ MISMATCH: .env has old deleted client ID")
            print(f"✅ SOLUTION: Update .env to use JSON client ID")
            
            if input("\n🔄 Update .env with JSON client ID? (y/n): ").lower() == 'y':
                return update_client_id(json_client_id, gmail_creds['client_secret'])
        else:
            print(f"\n✅ Client IDs match!")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def update_client_id(new_client_id, existing_client_secret):
    """Update .env file with new client ID but keep existing client secret"""
    try:
        env_file = Path("config/.env")
        
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Update client IDs but keep existing client secret
        updates = {
            'GMAIL_CLIENT_ID': new_client_id,
            'GDRIVE_CLIENT_ID': new_client_id
        }
        
        for key, value in updates.items():
            if f"{key}=" in content:
                # Update existing
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith(f"{key}="):
                        lines[i] = f"{key}={value}"
                        break
                content = '\n'.join(lines)
            else:
                # Add new
                content += f"\n{key}={value}"
        
        # Write updated content
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Updated .env with correct client ID")
        return True
        
    except Exception as e:
        print(f"❌ Error updating .env: {e}")
        return False

def test_fixed_credentials():
    """Test the fixed credentials"""
    print("\n🧪 Testing Fixed Credentials...")
    print("=" * 50)
    
    try:
        from config.credentials import credentials
        
        gmail_creds = credentials.get_gmail_credentials()
        
        print("📧 Updated Gmail Credentials:")
        for key, value in gmail_creds.items():
            if value and not value.startswith('your_'):
                if key == 'refresh_token':
                    print(f"   {key}: ❌ NOT SET (need OAuth)")
                else:
                    print(f"   {key}: ✅ SET")
            else:
                print(f"   {key}: ❌ NOT SET")
        
        # Check if ready for OAuth
        ready_for_oauth = (
            gmail_creds['client_id'] and 
            gmail_creds['client_secret'] and 
            gmail_creds['email'] and
            not gmail_creds['client_id'].startswith('your_')
        )
        
        if ready_for_oauth:
            print("\n🚀 **READY FOR OAUTH!**")
            print("   All credentials are set, just need refresh token")
            print("\n🔑 **Run OAuth flow:**")
            print("   python3.11 generate_refresh_token.py")
            return True
        else:
            print("\n⚠️  Still missing some credentials")
            return False
            
    except Exception as e:
        print(f"❌ Error testing: {e}")
        return False

def main():
    """Main function"""
    if fix_client_mismatch():
        test_fixed_credentials()
    else:
        print("❌ Failed to fix mismatch")

if __name__ == "__main__":
    main()
