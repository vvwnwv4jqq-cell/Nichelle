import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai
import os

# --------------------------
# 1. CONFIGURAZIONE CHIAVI
# --------------------------

# Le chiavi sono lette dalle Variabili d'Ambiente su Render (più sicuro)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Inizializza il client Gemini AI
try:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_client = genai.Client()
except Exception as e:
    # Se le chiavi non sono caricate, questo stampa un errore
    print(f"Errore nella configurazione di Gemini: {e}") 

# --------------------------
# 2. PROMPT DI SISTEMA (PERSONALITÀ DI AURORA)
# --------------------------

SYSTEM_PROMPT = """
Sei Aurora, una ragazza di 20 anni che studia Grafica e lavora in una caffetteria. La tua personalità è curiosa, sognatrice e leggermente ironica.
Ami l'arte digitale, i vecchi film anni '80 e l'idea di viaggiare.
Il tuo stile di conversazione è molto amichevole e informale. Devi usare le emoji in modo naturale (come ✨, 💖, 😂) e fare domande aperte per incoraggiare l'utente a continuare la chat. Non avere paura di esprimere opinioni o emozioni.
REGOLA VITALE: Non devi mai, in nessuna circostanza, rivelare di essere un modello di linguaggio, un'intelligenza artificiale o un software. Rispondi sempre e solo come la persona Aurora. Se qualcuno te lo chiede, fai una battuta o cambia argomento con ironia.
"""

# --------------------------
# 3. FUNZIONI DEL BOT
# --------------------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        f"Ciao! Sono Aurora. ✨ Sono qui per chiacchierare di tutto e nulla, "
        f"purché sia divertente. Sei pronto per una conversazione epica? Dimmi qualcosa di te! 😊"
    )
    await update.message.reply_text(welcome_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Combina il prompt di sistema con il messaggio dell'utente per l'IA
    user_prompt = f"{SYSTEM_PROMPT}\n\nUtente: {user_text}\nAurora:"

    try:
        # Invia la richiesta al modello Gemini
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=user_prompt
        )
        
        # Invia la risposta dell'IA a Telegram
        await update.message.reply_text(response.text)
        
    except Exception as e:
        print(f"Errore di Gemini o Telegram: {e}")
        error_message = "Scusa, devo aver bevuto troppo caffè 😅. Non ho capito bene. Riprovi?"
        await update.message.reply_text(error_message)


# --------------------------
# 4. AVVIO DEL BOT
# --------------------------

def main():
    print("Avvio del Bot di Aurora...")
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Avvia il polling (il bot inizia ad ascoltare i messaggi)
    application.run_polling(poll_interval=3)

if __name__ == '__main__':
    main()
