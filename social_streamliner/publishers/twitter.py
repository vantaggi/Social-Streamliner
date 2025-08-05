PLATFORM_NAME = "X (Twitter)"

def publish(video_path, title, description):
    """
    Simula la pubblicazione di un video su X (Twitter).

    Args:
        video_path (str): Il percorso locale del file video.
        title (str): Il testo del tweet.
        description (str): Non usato direttamente su Twitter, si usa solo il titolo.

    Returns:
        bool: True se la pubblicazione simulata è riuscita, False altrimenti.
    """
    print(f"--- Pubblicazione su {PLATFORM_NAME} ---")
    print(f"Video: {video_path}")
    print(f"Testo del Tweet: {title}")
    print(f"Successo: il video è stato 'pubblicato' su {PLATFORM_NAME}.")
    print("------------------------------------")
    # In una implementazione reale, qui ci sarebbe la chiamata all'API di X
    return True
