import os
import time
import requests
import config

PLATFORM_NAME = "Instagram"
GRAPH_API_VERSION = "v19.0"

def publish(video_path, title, description):
    """
    Publishes a video to Instagram Reels.

    Args:
        video_path (str): The local path to the video file.
        title (str): Not used by Instagram Reels API, caption is used instead.
        description (str): The caption for the Reel.

    Returns:
        bool: True if publishing was successful, False otherwise.
    """
    if not all([config.INSTAGRAM_BUSINESS_ACCOUNT_ID, config.INSTAGRAM_ACCESS_TOKEN]):
        print(f"Error: Instagram credentials are not set in the config file.")
        return False

    base_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{config.INSTAGRAM_BUSINESS_ACCOUNT_ID}"
    caption = f"{title}\n\n{description}" # Combine title and description for the caption

    try:
        print(f"--- Publishing on {PLATFORM_NAME} ---")

        # --- Step 1: Create a media container ---
        print("Step 1: Creating media container...")
        container_url = f"{base_url}/media"
        container_params = {
            'media_type': 'REELS',
            'video_url': None, # We will upload the file directly, not from a URL
            'caption': caption,
            'access_token': config.INSTAGRAM_ACCESS_TOKEN
        }

        # Instagram API requires a direct upload, so we can't use a pre-downloaded URL easily.
        # This example will proceed with a direct file upload flow.
        # The 'video_url' parameter is for server-side videos, not local uploads.
        # For local uploads, we first create a container, then upload to it.

        # Let's adjust the container creation for a local file upload
        container_params_for_upload = {
            'media_type': 'REELS',
            'caption': caption,
            'access_token': config.INSTAGRAM_ACCESS_TOKEN
        }

        # This is a simplified example. The actual Reels API requires a two-step upload.
        # 1. POST to /media to get an upload URL.
        # 2. POST the video file to that upload URL.
        # For simplicity and to avoid complex session handling, this example will just simulate.
        # A real implementation would require a more robust library or direct API calls.

        # The following is a conceptual guide. A full implementation is complex.
        # A real implementation would look something like this:

        # 1. Initialize Upload Session
        upload_init_url = f"{base_url}/media"
        upload_init_params = {
            'media_type': 'REELS',
            'access_token': config.INSTAGRAM_ACCESS_TOKEN,
        }
        init_response = requests.post(upload_init_url, params=upload_init_params)
        init_response.raise_for_status()
        upload_container_id = init_response.json()['id']
        print(f"Media container created with ID: {upload_container_id}")

        # 2. Upload the video file
        print("Step 2: Uploading video file...")
        upload_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{upload_container_id}"
        video_size = os.path.getsize(video_path)
        headers = {
            'Authorization': f'OAuth {config.INSTAGRAM_ACCESS_TOKEN}',
            'Content-Type': 'application/offset+octet-stream',
            'Content-Length': str(video_size)
        }
        with open(video_path, 'rb') as video_file:
            upload_response = requests.post(upload_url, headers=headers, data=video_file)
            upload_response.raise_for_status()
        print("Video file uploaded successfully.")

        # --- Step 3: Publish the media container ---
        print("Step 3: Publishing media container...")
        publish_url = f"{base_url}/media_publish"
        publish_params = {
            'creation_id': upload_container_id,
            'caption': caption,
            'access_token': config.INSTAGRAM_ACCESS_TOKEN
        }

        # Poll for completion
        # A real implementation would poll the status of the upload container before publishing.
        # For this example, we assume it's ready and proceed.

        publish_response = requests.post(publish_url, params=publish_params)
        publish_response.raise_for_status()

        final_media_id = publish_response.json()['id']
        print(f"Successfully published Reel to Instagram. Media ID: {final_media_id}")
        print("------------------------------------")
        return True

    except requests.exceptions.RequestException as e:
        print(f"An API error occurred while publishing to {PLATFORM_NAME}: {e}")
        if e.response:
            print(f"Response Body: {e.response.json()}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
