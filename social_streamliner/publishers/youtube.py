PLATFORM_NAME = "YouTube Shorts"

def publish(video_path, title, description):
    """
    Simula la pubblicazione di un video su YouTube Shorts.

    Args:
        video_path (str): Il percorso locale del file video.
        title (str): Il titolo del video.
        description (str): La descrizione del video.

    Returns:
        bool: True se la pubblicazione simulata è riuscita, False altrimenti.
    """
    print(f"--- Pubblicazione su {PLATFORM_NAME} ---")
    print(f"Video: {video_path}")
    print(f"Titolo: {title}")
    print(f"Descrizione: {description}")
    print(f"Successo: il video è stato 'pubblicato' su {PLATFORM_NAME}.")
    print("------------------------------------")
    # In una implementazione reale, qui ci sarebbe la chiamata all'API di YouTube
    return True
