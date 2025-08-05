import os
import gspread
from dotenv import load_dotenv
from datetime import datetime

# Carica le variabili d'ambiente dal file .env
load_dotenv()

def get_spreadsheet():
    """Funzione helper per autenticarsi e ottenere l'oggetto spreadsheet."""
    google_sheet_name = os.getenv("GOOGLE_SHEET_NAME")
    credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE")

    if not google_sheet_name or not credentials_file:
        print("Errore: GOOGLE_SHEET_NAME o GOOGLE_CREDENTIALS_FILE non sono impostati.")
        return None

    try:
        gc = gspread.service_account(filename=credentials_file)
        spreadsheet = gc.open(google_sheet_name)
        return spreadsheet
    except FileNotFoundError:
        print(f"Errore: File di credenziali '{credentials_file}' non trovato.")
        return None
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Errore: Google Sheet con nome '{google_sheet_name}' non trovato.")
        return None
    except Exception as e:
        print(f"Errore imprevisto durante l'accesso a Google Sheets: {e}")
        return None

def save_to_id_store(execution_id, video_url, game_name, clip_details):
    """Salva i dati nella tabella ID_Store, includendo il contesto del gioco."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False
    try:
        worksheet = spreadsheet.worksheet("ID_Store")
        created_at = datetime.now().isoformat()
        # La riga ora include anche game_name e clip_details
        worksheet.append_row([execution_id, video_url, created_at, game_name, clip_details])
        print(f"Dati salvati su ID_Store: {execution_id}")
        return True
    except gspread.exceptions.WorksheetNotFound:
        print("Errore: Worksheet 'ID_Store' non trovato.")
        return False
    except Exception as e:
        print(f"Errore durante il salvataggio su ID_Store: {e}")
        return False

def get_video_url_by_clip_id(clip_id):
    """Cerca un clip_id in ID_Store e restituisce un dizionario con i dettagli della clip."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return None
    try:
        worksheet = spreadsheet.worksheet("ID_Store")
        # Trova la cella con il clip_id (assumendo sia nella colonna 1)
        cell = worksheet.find(clip_id)

        if cell:
            # Recupera l'intera riga per ottenere tutti i dati
            row_values = worksheet.row_values(cell.row)
            # Le colonne dovrebbero essere: 0:ID, 1:URL, 2:Data, 3:Gioco, 4:Dettagli
            clip_data = {
                "video_url": row_values[1],
                "game_name": row_values[3],
                "clip_details": row_values[4]
            }
            print(f"Trovati dati per clip_id {clip_id}: {clip_data}")
            return clip_data
        else:
            print(f"Nessun dato trovato per il clip_id: {clip_id}")
            return None
    except Exception as e:
        print(f"Errore durante la ricerca su ID_Store: {e}")
        return None

def add_to_content_calendar(video_url, title, description, hashtags):
    """Aggiunge una nuova riga al Content_Calendar."""
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False
    try:
        worksheet = spreadsheet.worksheet("Content_Calendar")
        # Simula un ID auto-incrementale
        post_id = len(worksheet.get_all_records()) + 1
        created_at = datetime.now().isoformat()
        publication_date = ""  # Lasciato vuoto inizialmente
        hashtags_str = ", ".join(hashtags)
        status = 'scheduled'

        new_row = [post_id, video_url, title, description, hashtags_str, status, created_at, publication_date]
        worksheet.append_row(new_row)
        print(f"Nuovo post (ID: {post_id}) aggiunto al Content_Calendar.")
        return True
    except gspread.exceptions.WorksheetNotFound:
        print("Errore: Worksheet 'Content_Calendar' non trovato.")
        return False
    except Exception as e:
        print(f"Errore durante l'aggiunta al Content_Calendar: {e}")
        return False

def get_next_scheduled_post():
    """
    Trova il primo post con stato 'scheduled' nel Content_Calendar.
    Ordina implicitamente per riga (più vecchio prima).

    Returns:
        dict: Un dizionario che rappresenta la riga del post, o None se non trovato.
    """
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return None
    try:
        worksheet = spreadsheet.worksheet("Content_Calendar")
        # get_all_records() è comodo perché restituisce una lista di dizionari
        all_posts = worksheet.get_all_records()

        for post in all_posts:
            if post.get('status') == 'scheduled':
                print(f"Trovato post da pubblicare: ID {post.get('post_id')}")
                return post

        print("Nessun post schedulato trovato.")
        return None
    except Exception as e:
        print(f"Errore durante la ricerca del prossimo post: {e}")
        return None

def update_post_status(post_id, new_status):
    """
    Aggiorna lo stato di un post nel Content_Calendar e imposta la data di pubblicazione.

    Args:
        post_id (int or str): L'ID del post da aggiornare.
        new_status (str): Il nuovo stato (es. 'posted', 'failed').

    Returns:
        bool: True se l'aggiornamento è riuscito, False altrimenti.
    """
    spreadsheet = get_spreadsheet()
    if not spreadsheet:
        return False
    try:
        worksheet = spreadsheet.worksheet("Content_Calendar")
        # Trova la riga basata sul post_id (assumendo che sia nella colonna 1)
        cell = worksheet.find(str(post_id))

        if not cell:
            print(f"Errore: Post con ID {post_id} non trovato per l'aggiornamento.")
            return False

        # Aggiorna la colonna dello stato (colonna 6) e della data di pubblicazione (colonna 8)
        worksheet.update_cell(cell.row, 6, new_status)
        worksheet.update_cell(cell.row, 8, datetime.now().isoformat())

        print(f"Stato del post {post_id} aggiornato a '{new_status}'.")
        return True
    except Exception as e:
        print(f"Errore durante l'aggiornamento dello stato del post {post_id}: {e}")
        return False
