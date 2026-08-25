"""Canale di distribuzione Telegram per il riassunto giornaliero."""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def send_to_telegram(content: str) -> bool:
    """Invia il contenuto Markdown a Telegram.

    Args:
        content: Testo Markdown da inviare.

    Returns:
        True se invio riuscito, False altrimenti.
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Warning: TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID non configurati in .env")
        return False

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
        return data.get("ok", False)
    except Exception as e:
        print(f"Errore invio Telegram: {e}")
        return False


if __name__ == "__main__":
    print("Modulo telegram.py - test disabilitato (richiede .env configurato)")