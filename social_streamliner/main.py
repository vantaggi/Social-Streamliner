import uuid
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Importa le funzioni dai moduli di supporto
from sheets_handler import save_to_id_store, get_video_url_by_clip_id, add_to_content_calendar
from telegram_handler import send_to_telegram, send_confirmation_message
from gemini_handler import generate_content

# Carica le variabili d'ambiente dal file .env
load_dotenv()

app = Flask(__name__)

def generate_clip_id():
    """Genera un ID univoco e corto per la clip."""
    return str(uuid.uuid4())[:8]

@app.route('/webhook', methods=['POST'])
async def webhook():
    """
    Endpoint per ricevere gli URL dei video, salvarli su GSheets e inviarli a Telegram.
    """
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request body must be JSON"}), 400

    data = request.get_json()
    video_url = data.get('videoUrl')

    if not video_url:
        return jsonify({"status": "error", "message": "Missing 'videoUrl' in request body"}), 400

    # 1. Genera un ID univoco per la clip
    clip_id = generate_clip_id()
    print(f"ID della clip generato: {clip_id} per l'url {video_url}")

    # 2. Salva su Google Sheets
    if not save_to_id_store(clip_id, video_url):
        print(f"Errore nel salvataggio su Google Sheets per il clip ID: {clip_id}")
        return jsonify({"status": "error", "message": "Failed to save data to Google Sheets"}), 500

    # 3. Invia a Telegram per approvazione
    if not await send_to_telegram(clip_id, video_url):
        print(f"Errore nell'invio a Telegram per il clip ID: {clip_id}")
        return jsonify({"status": "error", "message": "Failed to send video to Telegram"}), 500

    # 4. Se tutto va a buon fine
    print(f"Processo completato con successo per il clip ID: {clip_id}")
    return jsonify({
        "status": "success",
        "message": "Video processed and sent for approval",
        "clip_id": clip_id
    }), 200

@app.route('/telegram_callback', methods=['POST'])
async def telegram_callback():
    """
    Endpoint per ricevere i callback dei pulsanti inline da Telegram,
    arricchire il contenuto e accodarlo nel calendario.
    """
    update = request.get_json()

    if "callback_query" not in update:
        return jsonify({"status": "ok", "message": "Not a callback query"}), 200

    callback_query = update["callback_query"]
    callback_data = callback_query["data"]
    chat_id = callback_query["message"]["chat"]["id"]

    print(f"Ricevuto callback da chat {chat_id}: {callback_data}")

    # Esegui solo se il pulsante è di approvazione
    if callback_data.startswith("approve:"):
        clip_id = callback_data.split(":")[1]

        # 1. Recupera l'URL del video
        video_url = get_video_url_by_clip_id(clip_id)
        if not video_url:
            await send_confirmation_message(chat_id, f"⚠️ Errore: non ho trovato il video per la clip {clip_id}.")
            return jsonify({"status": "error", "message": f"Clip ID {clip_id} not found"}), 404

        # 2. Genera i contenuti con Gemini
        # TODO: In futuro, queste informazioni potrebbero essere chieste all'utente via chat.
        game = "Call of Duty"
        clip_details = "1v3 clutch with a sniper"
        ai_content = generate_content(game, clip_details)
        if not ai_content:
            await send_confirmation_message(chat_id, "⚠️ Errore: non sono riuscito a generare i contenuti con l'AI.")
            return jsonify({"status": "error", "message": "Failed to generate content"}), 500

        # 3. Aggiungi al calendario dei contenuti
        success = add_to_content_calendar(
            video_url,
            ai_content["title"],
            ai_content["description"],
            ai_content["hashtags"]
        )
        if not success:
            await send_confirmation_message(chat_id, "⚠️ Errore: non sono riuscito a salvare il post nel calendario.")
            return jsonify({"status": "error", "message": "Failed to save to Content Calendar"}), 500

        # 4. Invia conferma all'utente
        await send_confirmation_message(chat_id, "✅ Clip approvata e aggiunta al calendario!")

    elif callback_data.startswith("reject:"):
        clip_id = callback_data.split(":")[1]
        # Opzionale: potremmo voler rimuovere la riga da ID_Store o marcare come rifiutata
        await send_confirmation_message(chat_id, f"❌ Clip {clip_id} rifiutata. Non verrà pubblicata.")

    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
