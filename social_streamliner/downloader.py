import os
import requests
import uuid

def download_video(video_url, destination_folder="temp_videos"):
    """
    Scarica un video da un URL in una cartella di destinazione.

    Args:
        video_url (str): L'URL del video da scaricare.
        destination_folder (str): La cartella dove salvare il video.

    Returns:
        str: Il percorso del file scaricato, o None se il download fallisce.
    """
    try:
        # Assicura che la cartella di destinazione esista
        os.makedirs(destination_folder, exist_ok=True)

        # Esegui la richiesta per scaricare il video
        response = requests.get(video_url, stream=True, timeout=60)
        response.raise_for_status()  # Solleva un'eccezione per status code di errore

        # Genera un nome di file unico per evitare sovrascritture
        # Estrae l'estensione del file dall'URL se possibile, altrimenti usa .mp4
        file_extension = os.path.splitext(video_url)[1]
        if not file_extension:
            file_extension = ".mp4"

        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(destination_folder, file_name)

        # Salva il file in chunk per gestire file di grandi dimensioni
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Video scaricato con successo in: {file_path}")
        return file_path

    except requests.exceptions.RequestException as e:
        print(f"Errore durante il download del video da {video_url}: {e}")
        return None
    except Exception as e:
        print(f"Errore imprevisto durante il download del video: {e}")
        return None
