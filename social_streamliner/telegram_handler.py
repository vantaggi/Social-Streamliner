import os
import telegram
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

async def send_to_telegram(clip_id, video_url):
    """
    Invia un video tramite URL a una chat di Telegram con una tastiera inline
    per l'approvazione o il rifiuto.

    Args:
        clip_id (str): L'ID univoco della clip, usato nel callback_data.
        video_url (str): L'URL del video da inviare.

    Returns:
        bool: True se l'invio è riuscito, False altrimenti.
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Errore: TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID non sono impostati nel file .env")
        return False

    try:
        bot = telegram.Bot(token=bot_token)

        # Creazione della tastiera inline
        keyboard = [
            [
                telegram.InlineKeyboardButton("✅ Approva", callback_data=f"approve:{clip_id}"),
                telegram.InlineKeyboardButton("❌ Rifiuta", callback_data=f"reject:{clip_id}"),
            ]
        ]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)

        # Invio del video
        # Usiamo un timeout più lungo perché il download e l'invio del video possono richiedere tempo
        await bot.send_video(
            chat_id=chat_id,
            video=video_url,
            reply_markup=reply_markup,
            connect_timeout=30,
            read_timeout=30
        )

        print(f"Video inviato a Telegram per approvazione. Clip ID: {clip_id}")
        return True

    except telegram.error.TelegramError as e:
        print(f"Errore durante l'invio del messaggio a Telegram: {e}")
        # Possibili cause: token non valido, chat_id non corretto, bot non autorizzato, URL del video non accessibile.
        return False
    except Exception as e:
        print(f"Si è verificato un errore imprevisto durante l'invio a Telegram: {e}")
        return False

async def send_confirmation_message(chat_id, text):
    """
    Invia un semplice messaggio di testo a una chat di Telegram.

    Args:
        chat_id (str or int): L'ID della chat a cui inviare il messaggio.
        text (str): Il testo del messaggio da inviare.

    Returns:
        bool: True se l'invio è riuscito, False altrimenti.
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("Errore: TELEGRAM_BOT_TOKEN non è impostato.")
        return False

    try:
        bot = telegram.Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=text)
        print(f"Messaggio di conferma inviato alla chat {chat_id}.")
        return True
    except Exception as e:
        print(f"Errore durante l'invio del messaggio di conferma: {e}")
        return False
