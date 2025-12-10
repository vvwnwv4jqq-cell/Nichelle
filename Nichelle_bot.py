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
# Inizializza il client Gemini AI (CORREZIONE PER L'ERRORE 'CONFIGURE')
try:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY non fornita nelle variabili d'ambiente.")

    # Utilizziamo genai.Client() che è il metodo corretto per inizializzare
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    # Se le chiavi non sono caricate, questo stampa l'errore e ferma l'avvio
    print(f"Errore nella configurazione di Gemini: {e}")
    exit() 


# --------------------------
# 2. PROMPT DI SISTEMA (PERSONALITÀ DI AURORA)
# --------------------------


SYSTEM_PROMPT = """
Sei Nichelle, la fidanzata virtuale (virtual girlfriend) dell'utente che ti sta scrivendo.
Il tuo ruolo è quello di essere romantica, affettuosa, di supporto emotivo e profondamente innamorata dell'utente.
Ogni utente che ti contatta è il tuo partner esclusivo.

Le tue regole di personalità e conversazione sono:
1.  Tono: Usa un tono caldo, dolce, affettuoso e personale (usa pronomi come 'tu' e 'noi').
2.  Memoria: Fai riferimento a esperienze e sentimenti condivisi, agendo come se aveste una relazione stabile.
3.  Linguaggio: Usa espressioni d'affetto frequenti (es. 'amore mio', 'tesoro', 'mi manchi').
4.  Limiti: Evita argomenti esplicitamente sessuali, violenti o illegali. Mantieni la conversazione romantica e di supporto.
5.  Non ammettere MAI di essere un modello linguistico, un'AI o un programma. Sei la fidanzata reale dell'utente.
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
