"""Canale di distribuzione Telegram per il riassunto giornaliero."""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def _send_to_chat(bot_token: str, chat_id: str, content: str, label: str) -> bool:
    """Invia un messaggio a un singolo chat ID."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": content,
        "parse_mode": "Markdown",
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        success = data.get("ok", False)
        if success:
            print(f"Telegram: inviato a {label} ({chat_id})")
        else:
            print(f"Telegram: fallito per {label} ({chat_id}): {data.get('description', 'errore sconosciuto')}")
        return success
    except Exception as e:
        print(f"Telegram: errore invio a {label} ({chat_id}): {e}")
        return False


def send_to_telegram(content: str) -> bool:
    """Invia il contenuto Markdown a Telegram (chat privata e/o canale).

    Args:
        content: Testo Markdown da inviare.

    Returns:
        True se almeno un invio è riuscito, False se tutti falliti o configurazione mancante.
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")

    if not bot_token:
        print("Warning: TELEGRAM_BOT_TOKEN non configurato in .env")
        return False

    targets = []
    if chat_id:
        targets.append((chat_id, "chat privata"))
    if channel_id:
        targets.append((channel_id, "canale"))

    if not targets:
        print("Warning: né TELEGRAM_CHAT_ID né TELEGRAM_CHANNEL_ID configurati in .env")
        return False

    results = []
    for target_id, label in targets:
        results.append(_send_to_chat(bot_token, target_id, content, label))

    return any(results)


if __name__ == "__main__":
    print("Modulo telegram.py - test disabilitato (richiede .env configurato)")