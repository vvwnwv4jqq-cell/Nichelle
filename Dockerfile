# Usa un'immagine Python base leggera
FROM python:3.11-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i requisiti e installali
COPY Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt

# Copia il resto del codice (il tuo Nichelle_bot.py)
COPY . .

# Comando per avviare il bot
CMD ["python", "Nichelle_bot.py"]
