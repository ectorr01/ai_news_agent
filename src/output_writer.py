"""Modulo per la scrittura dell'output Markdown compatibile Obsidian."""

import warnings
from datetime import date
from pathlib import Path
from typing import List, Dict, Any


def write_to_markdown(summarized_items: List[Dict[str, Any]], output_dir: Path = Path("output")) -> Path:
    """Scrive il file Markdown con front matter YAML compatibile Obsidian.

    Args:
        summarized_items: Lista di 3 notizie con title, link, summary_llm, source.
        output_dir: Directory di output (default 'output').

    Returns:
        Path del file creato.
    """
    if len(summarized_items) != 3:
        warnings.warn(f"write_to_markdown: attesi 3 elementi, ricevuti {len(summarized_items)}")

    output_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    base_name = f"{today}-ai-news.md"
    output_path = output_dir / base_name

    counter = 1
    while output_path.exists():
        output_path = output_dir / f"{today}-ai-news-{counter}.md"
        counter += 1

    front_matter = (
        f"---\n"
        f"title: \"AI News - {today}\"\n"
        f"tags: [ai-news, daily-digest]\n"
        f"date: {today}\n"
        f"---\n\n"
    )

    sections = []
    for i, item in enumerate(summarized_items, 1):
        title = item.get("title", "Senza titolo")
        summary = item.get("summary_llm", item.get("summary", "Nessun riassunto disponibile."))
        source = item.get("source", "Fonte sconosciuta")
        link = item.get("link", "#")

        sections.append(
            f"## {i}. {title}\n"
            f"{summary}\n\n"
            f"**Fonte:** [{source}]({link})\n"
        )

    content = front_matter + "\n".join(sections) + "\n"

    output_path.write_text(content, encoding="utf-8")
    return output_path


if __name__ == "__main__":
    print("Modulo output_writer.py - test con dati di esempio")
    test_items = [
        {"title": "Notizia 1", "link": "http://a.com", "summary_llm": "Riassunto 1", "source": "Src A"},
        {"title": "Notizia 2", "link": "http://b.com", "summary_llm": "Riassunto 2", "source": "Src B"},
        {"title": "Notizia 3", "link": "http://c.com", "summary_llm": "Riassunto 3", "source": "Src C"},
    ]
    path = write_to_markdown(test_items)
    print(f"File creato: {path}")
    print(path.read_text(encoding="utf-8"))