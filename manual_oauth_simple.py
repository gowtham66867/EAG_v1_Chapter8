#!/usr/bin/env python3.11

"""
Simple Manual OAuth - Bypass consent screen issues
"""

import webbrowser
import requests
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def manual_oauth_flow():
    """Manual OAuth flow using urn:ietf:wg:oauth:2.0:oob redirect"""
    print("🔑 Manual OAuth Flow - Bypass Consent Issues")
    print("=" * 60)
    
    try:
        from config.credentials import credentials
        
        gmail_creds = credentials.get_gmail_credentials()
        client_id = gmail_creds['client_id']
        client_secret = gmail_creds['client_secret']
        
        print(f"📋 Using Client ID: {client_id[:30]}...")
        
        # Create OAuth URL with special redirect that bypasses consent issues
        scopes = [
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        
        scope_string = '%20'.join(scopes)
        
        # Use urn:ietf:wg:oauth:2.0:oob which is less restrictive
        oauth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope={scope_string}&response_type=code&access_type=offline&prompt=consent"
        
        print("\n🌐 **Manual OAuth Steps:**")
        print("1. Browser will open with Google authorization")
        print("2. Sign in with your Google account")
        print("3. Grant all permissions when asked")
        print("4. You'll see a page with an authorization code")
        print("5. Copy the code and paste it here")
        
        print(f"\n🔗 **OAuth URL:**")
        print(f"{oauth_url}")
        
        # Open browser
        webbrowser.open(oauth_url)
        print("\n✅ Opened OAuth URL in browser")
        
        print("\n📋 **What you'll see:**")
        print("   • Google sign-in page")
        print("   • Permission request page")
        print("   • A page showing 'Please copy this code...'")
        print("   • Copy the authorization code from that page")
        
        # Get authorization code
        print("\n⏳ Complete authorization in browser, then:")
        auth_code = input("📋 Paste the authorization code here: ").strip()
        
        if not auth_code:
            print("❌ No authorization code provided")
            return False
        
        print(f"✅ Authorization code received: {auth_code[:20]}...")
        
        # Exchange for refresh token
        return exchange_for_refresh_token(client_id, client_secret, auth_code)
        
    except Exception as e:
        print(f"❌ Error in manual OAuth: {e}")
        return False

def exchange_for_refresh_token(client_id, client_secret, auth_code):
    """Exchange authorization code for refresh token"""
    print("\n🔄 Exchanging code for refresh token...")
    
    try:
        token_url = "https://oauth2.googleapis.com/token"
        
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'
        }
        
        print("📤 Sending token request...")
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            
            if 'refresh_token' in token_data:
                refresh_token = token_data['refresh_token']
                access_token = token_data.get('access_token', 'N/A')
                
                print(f"✅ Tokens received successfully!")
                print(f"   🔑 Refresh token: {refresh_token[:30]}...")
                print(f"   🎫 Access token: {access_token[:30]}...")
                
                # Update .env file
                if update_env_with_refresh_token(refresh_token):
                    print("✅ Refresh token saved to .env file")
                    return True
                else:
                    print("❌ Failed to save refresh token")
                    return False
            else:
                print("❌ No refresh token in response")
                print(f"📄 Response data: {token_data}")
                
                if 'access_token' in token_data:
                    print("💡 Got access token but no refresh token")
                    print("💡 This might happen if you've already authorized")
                    print("💡 Try revoking app access and trying again")
                
                return False
        else:
            print(f"❌ Token exchange failed: HTTP {response.status_code}")
            print(f"📄 Error response: {response.text}")
            
            if response.status_code == 400:
                print("\n💡 **Possible fixes:**")
                print("   • Make sure you copied the full authorization code")
                print("   • Try the OAuth flow again")
                print("   • Check if the authorization code expired")
            
            return False
            
    except Exception as e:
        print(f"❌ Error exchanging token: {e}")
        return False

def update_env_with_refresh_token(refresh_token):
    """Update .env file with refresh token"""
    try:
        env_file = Path("config/.env")
        
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Update refresh tokens
        updates = {
            'GMAIL_REFRESH_TOKEN': refresh_token,
            'GDRIVE_REFRESH_TOKEN': refresh_token
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
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating .env: {e}")
        return False

def test_complete_setup():
    """Test the complete setup"""
    print("\n🧪 Testing Complete Setup...")
    print("=" * 50)
    
    try:
        from config.credentials import credentials
        
        gmail_creds = credentials.get_gmail_credentials()
        
        print("📧 Final Gmail Credentials:")
        all_set = True
        for key, value in gmail_creds.items():
            if value and not value.startswith('your_'):
                print(f"   {key}: ✅ SET")
            else:
                print(f"   {key}: ❌ NOT SET")
                all_set = False
        
        if all_set:
            print("\n🎉 **OAUTH SETUP COMPLETE!**")
            print("\n🚀 **Ready to run:**")
            print("   • Full F1 workflow: python3.11 manual_f1_trigger.py")
            print("   • Test Gmail: python3.11 -c \"from mcp_server_gmail import send_email, SendEmailInput; print('Testing...'); result = send_email(SendEmailInput(to='gowtham66866@gmail.com', subject='MCP Test', body='Hello from MCP!')); print(f'Success: {result.success}')\"")
            print("   • Test Google Drive: python3.11 -c \"from mcp_server_gdrive import create_google_sheet, CreateSheetInput; print('Testing...'); result = create_google_sheet(CreateSheetInput(title='Test Sheet', data=[['A', 'B'], ['1', '2']])); print(f'Success: {result.success}')\"")
            return True
        else:
            print("\n⚠️  Some credentials still missing")
            return False
            
    except Exception as e:
        print(f"❌ Error testing setup: {e}")
        return False

def main():
    """Main function"""
    if manual_oauth_flow():
        test_complete_setup()
    else:
        print("\n❌ Manual OAuth failed")
        print("\n💡 **Alternative options:**")
        print("   1. Try publishing your OAuth app (not just testing)")
        print("   2. Use a different Google account for testing")
        print("   3. Create a new OAuth client from scratch")

if __name__ == "__main__":
    main()
