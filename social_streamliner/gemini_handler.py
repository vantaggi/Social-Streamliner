import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

def get_gemini_prompt():
    """
    Restituisce il prompt formattato per Gemini.
    In una implementazione reale, questo potrebbe essere caricato da un file o da un database.
    """
    return """Act as a world-class social media manager for a pro gamer, specializing in creating viral, short-form video content in English.

Your task is to generate a title, description, and hashtags based on the provided context.

**CONTEXT:**
* **Game:** {game}
* **Clip Details (optional):** {clip_details}

**INSTRUCTIONS:**
* **Title:** Short, high-impact, and curiosity-driven (under 10 words).
* **Description:** 1-2 concise, high-energy sentences. Use 1-2 emojis that fit the mood.
* **Hashtags:** 5 specific tags about the in-game action. NO generic tags like #fyp, #shorts, #viral, #gaming.

**EXAMPLES OF PERFECT OUTPUT:**

**Example 1 (Input Context: Game: Call of Duty, Clip Details: 1v3 clutch)**
{
  "title": "They NEVER see this coming... 🤯",
  "description": "Clean 1v3 clutch with the sniper to secure the win. That last shot was pure adrenaline! 🎯",
  "hashtags": ["#Warzone", "#WarzoneClutch", "#1v3", "#SniperGod", "#CallOfDuty"]
}

**Example 2 (Input Context: Game: F1 2025, Clip Details: Last lap overtake at Monza)**
{
  "title": "Last lap, last corner. UNREAL. 🏎️",
  "description": "Sent it down the inside at Monza's final corner for the P1. Absolute heart-in-mouth moment! 🏁",
  "hashtags": ["#F1game", "#F12025", "#Monza", "#LastLap", "#SimRacing"]
}

---
**NOW, GENERATE THE CONTENT FOR THE NEW CLIP BASED ON THE PROVIDED CONTEXT.**"""

def clean_json_string(s):
    """Pulisce la stringa di output del modello per renderla un JSON valido."""
    s = s.strip()
    if s.startswith("```json"):
        s = s[7:]
    if s.endswith("```"):
        s = s[:-3]
    return s.strip()

def generate_content(game, clip_details=""):
    """
    Genera titolo, descrizione e hashtag utilizzando l'API di Gemini.

    Args:
        game (str): Il nome del gioco.
        clip_details (str): Dettagli opzionali sulla clip.

    Returns:
        dict: Un dizionario con 'title', 'description', e 'hashtags', o None se fallisce.
    """
    try:
        # Configura l'API di Gemini all'interno della funzione
        genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

        model = genai.GenerativeModel('gemini-pro')

        prompt_template = get_gemini_prompt()
        prompt = prompt_template.format(game=game, clip_details=clip_details)

        response = model.generate_content(prompt)

        # Pulisci e analizza la risposta JSON
        cleaned_response = clean_json_string(response.text)
        content = json.loads(cleaned_response)

        # Valida che le chiavi necessarie siano presenti
        if all(k in content for k in ["title", "description", "hashtags"]):
            print("Contenuto generato con successo da Gemini.")
            return content
        else:
            print("Errore: il JSON generato da Gemini non contiene le chiavi richieste.")
            return None

    except Exception as e:
        print(f"Errore durante la generazione di contenuti con Gemini: {e}")
        return None
