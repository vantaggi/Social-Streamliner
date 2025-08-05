# Social Streamliner

Social Streamliner è un'applicazione di automazione completa progettata per streamer e creatori di contenuti per trasformare le clip video in post programmati e pubblicati sui social media con un intervento manuale minimo.

## Funzionalità Principali

- **Acquisizione tramite Webhook**: Invia un URL video a un endpoint API per avviare il processo.
- **Approvazione via Telegram**: Ricevi i video direttamente su Telegram con pulsanti per approvare o rifiutare la pubblicazione.
- **Arricchimento con AI**: I contenuti approvati vengono arricchiti con titoli, descrizioni e hashtag accattivanti generati da Google Gemini.
- **Calendario dei Contenuti**: I post vengono aggiunti a una coda di programmazione gestita tramite Google Sheets.
- **Pubblicazione Programmata**: Un processo schedulato pubblica automaticamente i contenuti su più piattaforme social a orari prestabiliti.
- **Modulare ed Estensibile**: L'architettura è progettata per aggiungere facilmente nuove piattaforme di social media.

## Architettura

L'applicazione è composta da due processi principali indipendenti:

1.  **Web Server (`main.py`)**: Un server Flask che gestisce la parte interattiva del flusso.
    -   Espone un endpoint `/webhook` per ricevere nuovi URL video.
    -   Espone un endpoint `/telegram_callback` per gestire le risposte ai pulsanti di approvazione/rifiuto.
    -   Comunica con Telegram, Google Sheets e Google Gemini.

2.  **Scheduler (`scheduler.py`)**: Un processo che viene eseguito in background per gestire la pubblicazione.
    -   Utilizza la libreria `schedule` per eseguire un job a intervalli di tempo configurabili.
    -   Cerca nel Google Sheet i post pronti per la pubblicazione.
    -   Scarica i video e li pubblica sulle piattaforme social configurate.

## Struttura del Progetto

```
social_streamliner/
├── publishers/
│   ├── __init__.py
│   ├── instagram.py
│   ├── tiktok.py
│   ├── twitter.py
│   └── youtube.py
├── .env.example
├── .gitignore
├── downloader.py
├── gemini_handler.py
├── main.py
├── README.md
├── requirements.txt
├── scheduler.py
├── sheets_handler.py
└── telegram_handler.py
```

## Installazione e Configurazione

Segui questi passaggi per configurare ed eseguire l'applicazione.

### 1. Prerequisiti

- Python 3.8+
- Un account Google con accesso a Google Sheets e Google AI Studio.
- Un bot di Telegram (creato tramite BotFather).

### 2. Installazione

```bash
# Clona questo repository (esempio)
# git clone https://github.com/tuo-utente/social-streamliner.git
# cd social-streamliner

# Installa le dipendenze
pip install -r social_streamliner/requirements.txt
```

### 3. Configurazione delle Credenziali

1.  **Google Sheets & Google Cloud**:
    -   Crea un progetto su [Google Cloud Platform](https://console.cloud.google.com/).
    -   Abilita l'API di **Google Sheets**.
    -   Crea un **Account di Servizio**, scarica il file delle credenziali JSON e rinominalo in `credentials.json`. Posizionalo nella cartella `social_streamliner`.
    -   Crea un nuovo Google Sheet. Condividilo con l'indirizzo email dell'account di servizio (es. `nome-servizio@...iam.gserviceaccount.com`).
    -   All'interno del foglio, crea due tabelle (fogli di lavoro) chiamate `ID_Store` e `Content_Calendar` e imposta le rispettive intestazioni come descritto nello schema del database.

2.  **Google Gemini AI**:
    -   Vai su [Google AI Studio](https://aistudio.google.com/) e genera una **API Key**.

3.  **Telegram**:
    -   Usa **BotFather** su Telegram per creare un nuovo bot e ottenere il **Token del Bot**.
    -   Trova il tuo **Chat ID** personale (puoi usare un bot come `@userinfobot`).

### 4. Variabili d'Ambiente

-   Crea un file `.env` nella cartella `social_streamliner` (puoi copiare da `.env.example`).
-   Compila il file `.env` con tutte le credenziali e i nomi raccolti nei passaggi precedenti.

## Come Eseguire l'Applicazione

Devi eseguire entrambi i processi in due terminali separati.

### 1. Avviare il Web Server

Questo processo gestisce la ricezione e l'approvazione dei video.

```bash
python social_streamliner/main.py
```

Per ricevere i webhook da Telegram, il server deve essere accessibile pubblicamente. Usa uno strumento come **ngrok** per esporre il tuo `localhost:5000` a internet e imposta il webhook del tuo bot Telegram sull'URL fornito da ngrok (es. `https://<ngrok_id>.ngrok.io/telegram_callback`).

### 2. Avviare lo Scheduler

Questo processo gestisce la pubblicazione dei video approvati.

```bash
python social_streamliner/scheduler.py
```

Lo scheduler si avvierà e attiverà i job di pubblicazione agli orari configurati (default: 09:00 e 18:00).

## Possibili Miglioramenti Futuri

- **Input Contestuale per l'AI**: Chiedere all'utente via Telegram dettagli sulla clip per generare testi più accurati.
- **Sistema di Retry**: In caso di fallimento di una pubblicazione, implementare un sistema che riprova a pubblicare.
- **Dashboard Web**: Aggiungere una semplice interfaccia web per visualizzare lo stato del calendario dei contenuti.
- **Database Robusto**: Migrare da Google Sheets a un database come PostgreSQL per gestire un volume maggiore di dati.
