import os
from google_auth_oauthlib.flow import InstalledAppFlow
import config
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

PLATFORM_NAME = "YouTube"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    """
    Handles OAuth2 authentication and returns a YouTube API service object.
    Caches credentials in 'token.json' for future runs.
    """
    token_file = 'youtube_token.json'

    flow = InstalledAppFlow.from_client_secrets_file(config.YOUTUBE_CLIENT_SECRETS_FILE, SCOPES)

    # The 'token.json' file stores the user's access and refresh tokens.
    # It's created automatically when the authorization flow completes for the first time.
    if os.path.exists(token_file):
        from google.oauth2.credentials import Credentials
        credentials = Credentials.from_authorized_user_file(token_file, SCOPES)
    else:
        # Run the flow to get the new credentials.
        credentials = flow.run_local_server(port=0)
        with open(token_file, 'w') as f:
            f.write(credentials.to_json())

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def publish(video_path, title, description):
    """
    Publishes a video to YouTube.

    Args:
        video_path (str): The local path to the video file.
        title (str): The video's title.
        description (str): The video's description.

    Returns:
        bool: True if publishing was successful, False otherwise.
    """
    try:
        print(f"--- Publishing on {PLATFORM_NAME} ---")
        youtube = get_authenticated_service()

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': [], # Tags are less relevant for Shorts, but can be added here
                'categoryId': '20' # 20 is the category ID for "Gaming"
            },
            'status': {
                'privacyStatus': 'public', # or 'private' or 'unlisted'
                'selfDeclaredMadeForKids': False
            }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media
        )

        response = request.execute()
        print(f"Successfully uploaded video to YouTube. Video ID: {response['id']}")
        print("------------------------------------")
        return True

    except Exception as e:
        print(f"An error occurred while publishing to {PLATFORM_NAME}: {e}")
        return False
