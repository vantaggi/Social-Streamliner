PLATFORM_NAME = "TikTok"

def publish(video_path, title, description):
    """
    Simula la pubblicazione di un video su TikTok.

    Args:
        video_path (str): Il percorso locale del file video.
        title (str): Il titolo/descrizione per TikTok.
        description (str): La descrizione (spesso non usata o unita al titolo su TikTok).

    Returns:
        bool: True se la pubblicazione simulata è riuscita, False altrimenti.
    """
    print(f"--- Pubblicazione su {PLATFORM_NAME} ---")
    print(f"Video: {video_path}")
    print(f"Testo: {title}") # TikTok usa un singolo campo di testo
    print(f"Successo: il video è stato 'pubblicato' su {PLATFORM_NAME}.")
    print("------------------------------------")
    # In una implementazione reale, qui ci sarebbe la chiamata all'API di TikTok
    return True
