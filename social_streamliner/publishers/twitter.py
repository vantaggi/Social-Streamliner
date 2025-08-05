import tweepy
import config
import time

PLATFORM_NAME = "X (Twitter)"

def get_api_v1():
    """Autenticazione per l'API v1.1 (necessaria per l'upload media)"""
    auth = tweepy.OAuth1UserHandler(
        config.X_API_KEY, config.X_API_SECRET,
        config.X_ACCESS_TOKEN, config.X_ACCESS_TOKEN_SECRET
    )
    return tweepy.API(auth)

def get_client_v2():
    """Autenticazione per l'API v2 (necessaria per postare il tweet)"""
    return tweepy.Client(
        consumer_key=config.X_API_KEY,
        consumer_secret=config.X_API_SECRET,
        access_token=config.X_ACCESS_TOKEN,
        access_token_secret=config.X_ACCESS_TOKEN_SECRET
    )

def publish(video_path, title, description):
    """Pubblica un video su X."""
    try:
        print(f"--- Pubblicazione su {PLATFORM_NAME} ---")
        api_v1 = get_api_v1()
        client_v2 = get_client_v2()

        # Fase di upload del media
        media = api_v1.media_upload(filename=video_path, media_category='tweet_video', chunked=True)

        # Attendi che l'elaborazione del media sia completata
        while media.processing_info['state'] == 'pending':
            print("Attendendo l'elaborazione del video da parte di X...")
            time.sleep(media.processing_info['check_after_secs'])
            media = api_v1.get_media_status(media.media_id_string)

        if media.processing_info['state'] != 'succeeded':
            raise Exception(f"Elaborazione video fallita: {media.processing_info['error']['message']}")

        print("Video caricato con successo su X.")

        # Pubblica il tweet allegando il media
        # Unisce titolo e descrizione per il testo del tweet
        tweet_text = f"{title}\n\n{description}"
        client_v2.create_tweet(text=tweet_text, media_ids=[media.media_id_string])

        print(f"Tweet pubblicato con successo su {PLATFORM_NAME}.")
        print("------------------------------------")
        return True

    except Exception as e:
        print(f"Errore durante la pubblicazione su {PLATFORM_NAME}: {e}")
        return False
