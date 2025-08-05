# Social Streamliner

Social Streamliner è una soluzione completa per automatizzare il processo di creazione di contenuti per i social media a partire da clip di gioco. È composto da un backend Python (Flask) che gestisce l'elaborazione video e la generazione di contenuti AI, e un'app client Flutter per un facile invio delle clip.

## Caratteristiche

- **Backend Python (Flask):**
  - Riceve gli URL delle clip di gioco tramite un endpoint webhook.
  - Salva i metadati delle clip (URL, nome del gioco, dettagli) su Google Sheets.
  - Invia le clip a un canale Telegram per l'approvazione.
  - Su approvazione, utilizza l'IA generativa di Google Gemini per creare titoli, descrizioni e hashtag pertinenti.
  - Aggiunge i contenuti approvati e generati a un calendario di contenuti su Google Sheets.

- **App Client (Flutter):**
  - Interfaccia utente semplice per inviare l'URL di una clip, il nome del gioco e dettagli opzionali.
  - Memorizza localmente la cronologia dei nomi dei giochi per un rapido inserimento tramite autocompletamento.
  - Precompila l'ultimo nome di gioco utilizzato per invii più veloci.

## Come Iniziare

### Prerequisiti

- Python 3.8+
- Flutter 3.0+
- Un account di servizio Google con accesso a Google Sheets e API Google Drive.
- Un bot di Telegram e il suo token API.
- Una chiave API di Google Gemini.

### Configurazione del Backend

1.  **Clona il repository:**
    ```bash
    git clone <URL_DEL_REPOSITORY>
    cd <CARTELLA_DEL_REPOSITORY>/social_streamliner
    ```

2.  **Crea un ambiente virtuale e installa le dipendenze:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Su Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configura le variabili d'ambiente:**
    - Rinomina `.env.example` in `.env`.
    - Apri il file `.env` e inserisci i tuoi valori per:
      - `GOOGLE_SHEET_NAME`: Il nome del tuo Google Sheet.
      - `GOOGLE_CREDENTIALS_FILE`: Il percorso del file JSON delle credenziali del tuo account di servizio.
      - `TELEGRAM_BOT_TOKEN`: Il token del tuo bot di Telegram.
      - `TELEGRAM_CHAT_ID`: L'ID della chat di Telegram dove inviare le clip per l'approvazione.
      - `GOOGLE_GEMINI_API_KEY`: La tua chiave API di Google Gemini.

4.  **Avvia il server Flask:**
    ```bash
    flask run
    ```
    Il backend sarà in esecuzione su `http://127.0.0.1:5000`.

### Configurazione dell'App Flutter

1.  **Naviga nella directory dell'app:**
    ```bash
    cd ../social_streamliner_app
    ```

2.  **Installa le dipendenze Flutter:**
    ```bash
    flutter pub get
    ```

3.  **Avvia l'app:**
    - Assicurati che un emulatore sia in esecuzione o che un dispositivo sia connesso.
    - Esegui il comando:
    ```bash
    flutter run
    ```

## Flusso di Lavoro

1.  L'utente inserisce l'URL della clip, il nome del gioco e i dettagli nell'app Flutter e tocca "Invia".
2.  L'app invia i dati all'endpoint `/webhook` del backend Flask.
3.  Il backend salva le informazioni nel foglio `ID_Store` di Google Sheets e invia la clip al canale Telegram.
4.  Un moderatore approva o rifiuta la clip tramite i pulsanti su Telegram.
5.  Se approvata, il backend recupera i dettagli (incluso il nome del gioco), genera il contenuto con Gemini e lo salva nel foglio `Content_Calendar`.