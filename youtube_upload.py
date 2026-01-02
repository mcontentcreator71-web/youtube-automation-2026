"""
YouTube Upload Script for The AI Ledger
Handles OAuth2.0 authentication and video upload to YouTube
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    import pickle
except ImportError as e:
    print(f"Missing required library: {e}")
    print("Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)


class YouTubeUploader:
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    CLIENT_SECRETS_FILE = "client_secrets.json"  # Download from Google Cloud Console
    CREDENTIALS_FILE = "youtube_credentials.pickle"
    
    def __init__(self):
        self.youtube = None
        self.credentials = None
        
    def authenticate(self):
        """Authenticate with YouTube API using OAuth2.0"""
        creds = None
        
        # Load existing credentials
        if os.path.exists(self.CREDENTIALS_FILE):
            with open(self.CREDENTIALS_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.CLIENT_SECRETS_FILE):
                    raise FileNotFoundError(
                        f"Please download OAuth2.0 credentials from Google Cloud Console "
                        f"and save as {self.CLIENT_SECRETS_FILE}"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CLIENT_SECRETS_FILE, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.CREDENTIALS_FILE, 'wb') as token:
                pickle.dump(creds, token)
        
        self.credentials = creds
        self.youtube = build('youtube', 'v3', credentials=creds)
        return True
    
    def upload_video(self, video_file, title, description, tags=None, category_id="28", 
                     privacy_status="private", schedule_time=None):
        """
        Upload video to YouTube
        
        Args:
            video_file: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID (28 = Science & Technology)
            privacy_status: 'private', 'unlisted', or 'public'
            schedule_time: datetime object for scheduled publish (optional)
        """
        if not self.youtube:
            self.authenticate()
        
        # Prepare metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status
            }
        }
        
        # Add scheduled publish time if provided
        if schedule_time:
            body['status']['publishAt'] = schedule_time.isoformat() + 'Z'
        
        # Upload video
        media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
        
        insert_request = self.youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        return {
                            'status': 'success',
                            'videoId': response['id'],
                            'videoUrl': f"https://www.youtube.com/watch?v={response['id']}"
                        }
                    else:
                        return {
                            'status': 'error',
                            'error': 'Upload failed - no video ID returned'
                        }
            except Exception as e:
                if retry > 3:
                    return {
                        'status': 'error',
                        'error': str(e)
                    }
                retry += 1
                error = e
        
        return {
            'status': 'error',
            'error': str(error) if error else 'Unknown error'
        }
    
    def schedule_upload(self, video_file, title, description, upload_times, tags=None):
        """
        Schedule multiple uploads at specific times
        
        Args:
            upload_times: List of datetime objects for scheduled uploads
        """
        results = []
        for schedule_time in upload_times:
            result = self.upload_video(
                video_file=video_file,
                title=title,
                description=description,
                tags=tags,
                privacy_status='private',  # Will be made public at schedule time
                schedule_time=schedule_time
            )
            results.append({
                'scheduleTime': schedule_time.isoformat(),
                **result
            })
        return results


def get_usa_peak_times():
    """Get USA peak times for today: 8 AM, 12 PM, 6 PM EST"""
    from datetime import datetime, timezone, timedelta
    
    # EST timezone
    est = timezone(timedelta(hours=-5))
    today = datetime.now(est).date()
    
    times = [
        datetime.combine(today, datetime.strptime("08:00", "%H:%M").time()).replace(tzinfo=est),
        datetime.combine(today, datetime.strptime("12:00", "%H:%M").time()).replace(tzinfo=est),
        datetime.combine(today, datetime.strptime("18:00", "%H:%M").time()).replace(tzinfo=est),
    ]
    
    return times


if __name__ == "__main__":
    # Example usage
    try:
        input_data = json.load(sys.stdin) if not sys.stdin.isatty() else {}
        
        uploader = YouTubeUploader()
        uploader.authenticate()
        
        video_file = input_data.get('videoFilePath')
        title = input_data.get('title', 'AI News Update')
        description = input_data.get('description', '')
        tags = input_data.get('tags', ['AI', 'Artificial Intelligence', 'Technology', 'The AI Ledger'])
        
        # Schedule uploads for USA peak times
        schedule_times = get_usa_peak_times()
        
        result = uploader.schedule_upload(
            video_file=video_file,
            title=title,
            description=description,
            upload_times=schedule_times,
            tags=tags
        )
        
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({'error': str(e), 'status': 'failed'}))







