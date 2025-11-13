#!/usr/bin/env python3.11

"""
Google Drive MCP Server with Service Account Authentication
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
mcp = FastMCP("Google Drive Service Account Server")

class CreateSheetInput(BaseModel):
    title: str
    data: List[List[str]]
    make_public: bool = True

class SheetResult(BaseModel):
    success: bool
    sheet_id: Optional[str] = None
    sheet_url: Optional[str] = None
    error: Optional[str] = None

class UploadFileInput(BaseModel):
    file_path: str
    file_name: Optional[str] = None
    make_public: bool = True

class FileResult(BaseModel):
    success: bool
    file_id: Optional[str] = None
    file_url: Optional[str] = None
    error: Optional[str] = None

@mcp.tool()
def create_google_sheet(input_data: CreateSheetInput) -> SheetResult:
    """Create a Google Sheet with data using service account authentication"""
    try:
        from googleapiclient.discovery import build
        
        # Get service account credentials
        credentials = credential_manager.get_service_account_credentials()
        if not credentials:
            return SheetResult(
                success=False,
                error="Service account credentials not configured"
            )
        
        # Build Sheets service
        sheets_service = build('sheets', 'v4', credentials=credentials)
        drive_service = build('drive', 'v3', credentials=credentials)
        
        # Create spreadsheet
        spreadsheet_body = {
            'properties': {
                'title': input_data.title
            }
        }
        
        spreadsheet = sheets_service.spreadsheets().create(
            body=spreadsheet_body
        ).execute()
        
        sheet_id = spreadsheet['spreadsheetId']
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
        
        # Add data to sheet
        if input_data.data:
            range_name = f"Sheet1!A1:{chr(65 + len(input_data.data[0]) - 1)}{len(input_data.data)}"
            
            value_input_option = 'RAW'
            body = {
                'values': input_data.data
            }
            
            sheets_service.spreadsheets().values().update(
                spreadsheetId=sheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()
        
        # Make public if requested
        if input_data.make_public:
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            drive_service.permissions().create(
                fileId=sheet_id,
                body=permission
            ).execute()
        
        return SheetResult(
            success=True,
            sheet_id=sheet_id,
            sheet_url=sheet_url,
            error=None
        )
        
    except Exception as e:
        return SheetResult(
            success=False,
            error=f"Failed to create Google Sheet: {str(e)}"
        )

@mcp.tool()
def upload_file_to_drive(input_data: UploadFileInput) -> FileResult:
    """Upload file to Google Drive"""
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        credentials = credential_manager.get_service_account_credentials()
        if not credentials:
            return FileResult(
                success=False,
                error="Service account credentials not configured"
            )
        
        drive_service = build('drive', 'v3', credentials=credentials)
        
        file_path = Path(input_data.file_path)
        if not file_path.exists():
            return FileResult(
                success=False,
                error=f"File not found: {input_data.file_path}"
            )
        
        file_name = input_data.file_name or file_path.name
        
        file_metadata = {
            'name': file_name
        }
        
        media = MediaFileUpload(str(file_path), resumable=True)
        
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        file_id = file.get('id')
        file_url = f"https://drive.google.com/file/d/{file_id}/view"
        
        # Make public if requested
        if input_data.make_public:
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            drive_service.permissions().create(
                fileId=file_id,
                body=permission
            ).execute()
        
        return FileResult(
            success=True,
            file_id=file_id,
            file_url=file_url,
            error=None
        )
        
    except Exception as e:
        return FileResult(
            success=False,
            error=f"Failed to upload file: {str(e)}"
        )

@mcp.tool()
def list_drive_files(max_results: int = 10) -> Dict[str, Any]:
    """List files in Google Drive"""
    try:
        from googleapiclient.discovery import build
        
        credentials = credential_manager.get_service_account_credentials()
        if not credentials:
            return {"success": False, "error": "Service account not configured"}
        
        drive_service = build('drive', 'v3', credentials=credentials)
        
        results = drive_service.files().list(
            pageSize=max_results,
            fields="nextPageToken, files(id, name, mimeType, createdTime, webViewLink)"
        ).execute()
        
        files = results.get('files', [])
        
        return {
            "success": True,
            "files": files,
            "count": len(files)
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    mcp.run()
