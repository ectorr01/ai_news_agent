"""Orchestrazione del flusso: fetch -> summarize -> write."""

from dotenv import load_dotenv
load_dotenv()

import sys
from .fetch_news import fetch_latest_ai_news
from .summarize import summarize_news
from .output_writer import write_to_markdown


def main() -> None:
    """Esegue il flusso completo."""
    print("Recupero notizie AI...")
    news = fetch_latest_ai_news()

    if not news:
        print("Nessuna notizia trovata. Interruzione.")
        sys.exit(1)

    print(f"Trovate {len(news)} notizie")
    for i, item in enumerate(news, 1):
        print(f"  {i}. {item['title']}")

    print("\nGenerazione riassunti...")
    news = summarize_news(news)

    if len(news) != 3:
        print(f"Warning: summarize_news ha restituito {len(news)} elementi, ne servono esattamente 3")

    print("\nScrittura file output...")
    output_path = write_to_markdown(news)
    print(f"File creato: {output_path}")

    print("\nFlusso completato")


if __name__ == "__main__":
    main()