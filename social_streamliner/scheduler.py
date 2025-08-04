import os
import time
import schedule
from sheets_handler import get_next_scheduled_post, update_post_status
from downloader import download_video
from publishers import all_publishers

def job():
    """
    Il compito che verrà eseguito dallo scheduler.
    Contiene la logica principale del Modulo di Pubblicazione.
    """
    print("\n" + "="*50)
    print(f"Esecuzione del job di pubblicazione: {time.ctime()}")
    print("="*50)

    # 1. Trova il prossimo post da pubblicare
    post = get_next_scheduled_post()
    if not post:
        print("Nessun post da pubblicare. Il job termina qui.")
        return

    post_id = post.get('post_id')
    video_url = post.get('video_url')
    title = post.get('title')
    description = post.get('description')

    # 2. Scarica il video
    print(f"\n--- Download del video per il post {post_id} ---")
    video_path = download_video(video_url)
    if not video_path:
        print(f"Download fallito. Marco il post {post_id} come 'failed'.")
        update_post_status(post_id, 'failed')
        return

    # 3. Pubblica su tutte le piattaforme
    print(f"\n--- Inizio pubblicazione su tutte le piattaforme per il post {post_id} ---")
    success_count = 0
    for publisher in all_publishers:
        try:
            if publisher.publish(video_path, title, description):
                success_count += 1
            else:
                print(f"Pubblicazione fallita su {publisher.PLATFORM_NAME}")
        except Exception as e:
            print(f"Errore imprevisto durante la pubblicazione su {publisher.PLATFORM_NAME}: {e}")

    # 4. Aggiorna lo stato finale e pulisci
    final_status = 'posted' if success_count > 0 else 'failed'
    print(f"\n--- Aggiornamento stato finale per il post {post_id} ---")
    update_post_status(post_id, final_status)

    print(f"\n--- Pulizia dei file temporanei ---")
    try:
        os.remove(video_path)
        print(f"File video {video_path} rimosso.")
    except OSError as e:
        print(f"Errore durante la rimozione del file {video_path}: {e}")

    print("\n" + "="*50)
    print("Job di pubblicazione completato.")
    print("="*50)

def main():
    """
    Funzione principale per avviare lo scheduler.
    """
    print("Avvio dello scheduler di pubblicazione...")

    # Imposta la schedulazione. Esempio: ogni giorno alle 09:00 e alle 18:00
    # Per testing, possiamo eseguirlo più frequentemente, es. ogni minuto.
    schedule.every().day.at("09:00").do(job)
    schedule.every().day.at("18:00").do(job)

    # Loop infinito per mantenere lo script in esecuzione
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
