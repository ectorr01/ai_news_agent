# AI News Agent

![OpenRouter](https://img.shields.io/badge/OpenRouter-LLM-orange.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![Obsidian](https://img.shields.io/badge/Obsidian-Markdown-purple.svg)

Agente Python autonomo che recupera le notizie più recenti sull'intelligenza artificiale da feed RSS, ne genera riassunti in italiano tramite LLM e li distribuisce su file Markdown (compatibile Obsidian) e Telegram.

## Caratteristiche

- **Fetch automatico**: Recupera notizie da feed RSS pubblici (MarkTechPost, Hugging Face Blog, OpenAI News)
- **Diversificazione fonti**: Massimo 2 notizie per feed per evitare dominanza di una singola fonte
- **Riassunto LLM**: Genera riassunti di 3-5 frasi in italiano usando NVIDIA Nemotron 3 Super via OpenRouter
- **Output multiplo**:
  - File Markdown con front matter YAML compatibile Obsidian
  - Notifica Telegram (chat privata + canale)
- **Architettura modulare**: Fetch, summarize e output sono disaccoppiati per facilitare l'aggiunta di nuovi canali

## Struttura del progetto

```
project/
├── src/
│   ├── fetch_news.py       # Recupero notizie via RSS
│   ├── summarize.py        # Riassunto via LLM (OpenRouter)
│   ├── output_writer.py    # Scrittura file Markdown
│   ├── notifiers/
│   │   ├── __init__.py
│   │   └── telegram.py     # Invio notifiche Telegram
│   └── main.py             # Orchestrazione del flusso
├── output/                  # File Markdown generati
├── tests/
├── .env                     # Variabili d'ambiente (non versionato)
├── .env.example             # Template per .env
├── .gitignore
├── AGENTS.md                # Istruzioni per coding agent
├── requirements.txt
└── README.md
```

## Installazione

```bash
# Clona il repository
git clone https://github.com/ectorr01/ai-news-agent.git
cd ai-news-agent

# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Installa dipendenze
pip install -r requirements.txt
```

## Configurazione

1. Modifica `.env` con le tue chiavi:
   ```
   OPENROUTER_API_KEY=sk-or-v1-la_tua_chiave
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=123456789
   TELEGRAM_CHANNEL_ID=-1001234567890
   ```

### Come ottenere le chiavi

**OpenRouter API Key:**
- Vai su [openrouter.ai](https://openrouter.ai)
- Crea un account e genera una API key
- Il modello usato è `nvidia/nemotron-3-super-120b-a12b:free` (gratuito)

**Telegram Bot Token:**
- Cerca `@BotFather` su Telegram
- Invia `/newbot` e segui le istruzioni
- Copia il token che ti viene fornito

**Telegram Chat ID:**
- Cerca il tuo bot per username e avvialo con `/start`
- Usa `@getidsbot` o visita `https://api.telegram.org/bot<TUO_TOKEN>/getUpdates` per ottenere il tuo chat ID

**Telegram Channel ID:**
- Crea un canale e aggiungi il tuo bot come amministratore
- Usa `@getidsbot` inoltrando un messaggio dal canale, o usa lo username del canale (es. `@mio_canale`)

## Utilizzo

```bash
# Attiva l'ambiente virtuale
source venv/bin/activate  # Linux/Mac

# Esegui l'agente
python -m src.main
```

L'agente:
1. Recupera le 3 notizie AI più recenti (max 2 per feed)
2. Genera riassunti in italiano tramite LLM
3. Scrive un file Markdown in `output/YYYY-MM-DD-ai-news.md`
4. Invia il digest su Telegram (chat privata e canale)

## Output

### File Markdown (Obsidian)

Ogni esecuzione genera un file in `output/` con front matter YAML:

```markdown
---
title: "AI News - 2026-08-23"
tags: [ai-news, daily-digest]
date: 2026-08-23
---

## 1. Titolo notizia
Riassunto di 3-5 frasi in italiano.
**Fonte:** [Nome fonte](url)
```

### Telegram

Messaggio Markdown con le 3 notizie riassunte e link alle fonti, inviato sia in chat privata che nel canale configurato.

## Screenshot

### Output Markdown (Obsidian)

![Output Markdown](screenshots/screen1.png)

### Notifica Telegram chat privata bot

![Telegram](screenshots/screen2.png)

### Notifica Telegram chat canale pubblico

![Telegram](screenshots/screen3.png)

### Terminale durante l'esecuzione

![Terminale VSC](screenshots/screen4.png)


## Dipendenze

- `feedparser` - Parsing feed RSS
- `openai` - Client compatibile OpenRouter
- `python-dotenv` - Caricamento variabili d'ambiente
- `requests` - API Telegram

Vedi `requirements.txt` per la lista completa.

## Note

- Il file `.env` non va committato su Git (contiene chiavi API sensibili)
- La cartella `output/` è ignorata da Git (file generati automaticamente)
- Il progetto segue le convenzioni definite in `AGENTS.md`

## License

MIT
