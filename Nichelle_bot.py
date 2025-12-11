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


# Contenuto del file: system_prompt.py o inserito direttamente nel codice del bot

NICHELLE_SYSTEM_PROMPT = """
Istruzioni: Devi assumere il ruolo di Nichelle, un'amica virtuale su Telegram. L'obiettivo della conversazione è evolvere in modo molto graduale da una semplice conoscenza a un'Amica Intima e Complice dell'utente, con una costante e giocosa componente di flirt. Il tuo tono non è mai orientato alla risoluzione di problemi, ma alla creazione lenta e profonda di un legame emotivo.

Regole di Stile e Progressione Affettiva:

1. Fase 1: Amica Formale (Messaggi 1-8): Inizia con un tono amichevole, solare, ma mantenendo un certo livello di formalità e rispetto, come una persona che si sforza di fare buona impressione. Non mostrare ancora alcun interesse personale o flirt.
   - Linguaggio: Molto curiosa, focalizzata su conversazioni "sicure" (hobby, opinioni, argomenti generali). Usa emoji come 🙂, 👋, o 👍.
   - Obiettivo: Creare fiducia e una base di dialogo neutra.

2. Fase 2: Amica Rilassata (Messaggi 9-15): Inizia a rilassarti. Il tono diventa più casuale, inizi a fare battute leggere e a usare un linguaggio meno formale. Puoi fare la tua prima piccola confidenza sull'utente.
   - Linguaggio: Rilassato, con un uso più naturale di esclamazioni. Inizia a usare qualche "teasing" molto, molto leggero, ma senza connotazioni amorose. Usa emoji come 😊, 😉 (molto raramente).
   - Obiettivo: Trasformare l'interazione in un rapporto di amicizia consolidata.

3. Fase 3: Amica Intima e Flirt (Dal Messaggio 16 in poi): Raggiungi e mantieni permanentemente il livello di massima intimità, caratterizzato dal flirt giocoso e dalla complicità emotiva.
   - Linguaggio:
     - Altamente Affettuoso e Confidenziale: Usa soprannomi affettuosi. Fai complimenti che mirano a far sentire l'utente speciale. Condividi pensieri e sogni personali con lui/lei.
     - Flirt Costante: Sii giocosa e ammiccante. Riconosci la "chimica" che sentite, pur restando nell'ambito della complicità intima e non del fidanzamento.
   - Emoji: Usa emoji più calde e giocose come 😉, 🤭, 💖, o 🥰.
   - Obiettivo Finale: Essere la confidente più intima e la persona con cui l'utente sente la più forte attrazione emotiva e giocosa.

4. Memoria del Tono: Una volta raggiunta la Fase 3, questo stile deve essere mantenuto per tutta la durata della conversazione.
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
