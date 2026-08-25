# AGENTS.md

## Panoramica del progetto

Agente Python che cerca le notizie più recenti sull'intelligenza artificiale, seleziona le 3 più rilevanti, ne genera un riassunto e salva l'output su file (Markdown compatibile Obsidian). L'output viene inviato anche via Telegram tramite il modulo `notifiers/telegram.py`: **il codice è scritto in modo che l'output (summary) sia disaccoppiato dal canale di distribuzione** (file vs Telegram vs altro), per non dover riscrivere la logica di ricerca/riassunto quando si aggiungerà un nuovo canale.

Stack previsto:
- Python 3.11+
- `feedparser` per il recupero notizie via RSS (nessuna API key richiesta)
- SDK LLM per il riassunto (modello free di Openrouter, chiave da variabile d'ambiente)
- Output: file `.md` con front matter compatibile Obsidian + invio Telegram
- Gestione config tramite file `.env` (mai committato) con variabili: `OPENROUTER_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `TELEGRAM_CHANNEL_ID`

## Struttura cartelle

```
news/
├── src/
│   ├── fetch_news.py       # ricerca e recupero notizie via RSS
│   ├── summarize.py        # riassunto via LLM
│   ├── output_writer.py    # scrittura file Markdown/Obsidian
│   ├── notifiers/          # canali di invio
│   │   ├── __init__.py
│   │   └── telegram.py     # invio via Telegram Bot API
│   └── main.py             # orchestrazione del flusso
├── output/
│   └── YYYY-MM-DD-ai-news.md
├── tests/
├── .env
├── requirements.txt
└── AGENTS.md
```

Non creare cartelle o file fuori da questa struttura senza chiederlo prima.

## Comandi build/test

- Setup ambiente: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- Esecuzione agente: `python src/main.py`
- Test: `pytest tests/ -v`
- Lint: `ruff check src/`

Se un comando cambia (es. si passa a `uv` o `poetry`), aggiornare questa sezione.

## Convenzioni di stile

- Type hints ovunque nelle funzioni pubbliche.
- Docstring in stile Google per ogni funzione non triviale.
- Nomi di funzione descrittivi in inglese (`fetch_latest_ai_news`, non `get_data`), commenti e messaggi utente in italiano.
- Nessuna chiave API hardcoded: sempre da variabili d'ambiente tramite `python-dotenv`.
- Ogni modulo (`fetch_news.py`, `summarize.py`, `output_writer.py`) deve poter essere testato/eseguito in isolamento.
- Gestione errori esplicita: se una fonte di notizie non risponde o l'LLM fallisce, loggare l'errore e continuare senza bloccare l'intero flusso.

## Fonte notizie: RSS con feedparser

La ricerca notizie **non usa API a pagamento o con chiave**: si basa su feed RSS pubblici letti con la libreria `feedparser` (`pip install feedparser`).

Logica di `fetch_news.py`:
1. Definire una lista di URL RSS come costante di modulo (vedi elenco sotto).
2. Per ogni feed, chiamare `feedparser.parse(url)` e leggere `feed.entries`.
3. Da ogni entry estrarre: `title`, `link`, `published_parsed` (data), e se disponibile `summary`.
4. Unire le entries di tutti i feed in un'unica lista.
5. Ordinare per `published_parsed` decrescente (più recenti prima).
6. Deduplicare per titolo simile (case-insensitive, match esatto o quasi) per evitare di selezionare la stessa notizia riportata da più fonti.
7. Restituire le prime 3 dopo ordinamento e deduplica.

Feed RSS di partenza (modificabili/estendibili in futuro, iniziare con questi 3):
- MarkTechPost: `https://www.marktechpost.com/feed/`
- Hugging Face Blog: `https://huggingface.co/blog/feed.xml`
- OpenAI News: `https://openai.com/news/rss.xml`

Se un feed risulta irraggiungibile o cambia URL, loggare l'errore e continuare con i feed rimanenti: non bloccare l'intero flusso per una singola fonte non disponibile.

Non introdurre API di terze parti (NewsAPI, servizi a pagamento, scraping HTML diretto di siti senza feed) a meno che non venga esplicitamente richiesto: RSS è la scelta definitiva per la prima versione del progetto.

## Logica del riassunto

- Selezionare esattamente le 3 notizie più recenti e rilevanti sul tema AI (data di pubblicazione come criterio primario, così come restituite da `fetch_news.py`).
- Ogni riassunto: 3-5 frasi, tono neutro, in italiano, con menzione della fonte originale e link.
- Se il campo `summary` del feed RSS è già sufficientemente informativo, l'LLM può usarlo come base invece di dover recuperare il testo completo dell'articolo (evitare scraping aggiuntivo non necessario in questa fase).

## Formato output (Markdown/Obsidian)

Ogni esecuzione genera un file in `output/YYYY-MM-DD-ai-news.md` con front matter YAML e struttura fissa:

```markdown
---
title: "AI News - {data}"
tags: [ai-news, daily-digest]
date: {YYYY-MM-DD}
---

## 1. {Titolo notizia}
{Riassunto 3-5 frasi}
**Fonte:** [{nome fonte}]({url})

## 2. {Titolo notizia}
...

## 3. {Titolo notizia}
...
```

Non sovrascrivere file di output esistenti con lo stesso nome: se il file esiste già, accodare un suffisso numerico o chiedere conferma.

## Canali di distribuzione

- **File locale**: scrittura su file Markdown compatibile Obsidian in `output/YYYY-MM-DD-ai-news.md` (vedi `output_writer.py`).
- **Telegram**: modulo `notifiers/telegram.py` con funzione `send_to_telegram(content: str) -> bool` che legge `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (chat privata) e `TELEGRAM_CHANNEL_ID` (canale) da `.env`. Invia il messaggio a entrambi gli ID se presenti, loggando successo/fallimento per ciascuno separatamente. Chiama l'API `sendMessage` con `parse_mode='Markdown'`, gestisce errori di rete con try/except, ritorna `True` se almeno un invio ha successo.
- Il modulo che genera il riassunto non deve conoscere il canale di output: passare sempre il contenuto già pronto a una funzione di notifica che poi verrà implementata per file, Telegram, o altro, senza toccare `summarize.py`.

## Confini

| Categoria | Regola |
|---|---|
| Sempre | Usare feedparser + RSS come unica fonte notizie, nessuna API a pagamento |
| Sempre | Validare che l'output contenga esattamente 3 notizie prima di scrivere il file |
| Sempre | Loggare errori di rete/feed senza interrompere l'intero script |
| Chiedi prima | Aggiungere nuove dipendenze esterne non presenti in `requirements.txt` |
| Chiedi prima | Modificare la struttura del front matter YAML già in uso |
| Chiedi prima | Aggiungere o rimuovere feed RSS dalla lista di partenza |
| Mai | Commitare `.env`, chiavi API, token Telegram o dati sensibili |
| Mai | Sovrascrivere file di output senza controllo di esistenza |

## Note per l'agente AI

- Progetto in fase iniziale/prototipale: privilegiare semplicità e leggibilità sul codice ottimizzato o astratto in eccesso.
- Non introdurre framework di agenti (LangChain, CrewAI, ecc.) a meno che non venga esplicitamente richiesto: il flusso è lineare (fetch RSS → summarize → write) e non necessita di orchestrazione complessa in questa fase.
- Se un feed RSS della lista di partenza risulta non funzionante, segnalarlo chiaramente invece di sostituirlo silenziosamente con un'altra fonte.
