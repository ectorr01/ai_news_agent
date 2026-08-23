"""Modulo per il riassunto delle notizie via LLM (OpenRouter)."""

import os
from typing import List, Dict, Any

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


SYSTEM_PROMPT = (
    "Sei un assistente che riassume notizie sull'intelligenza artificiale. "
    "Rispondi SEMPRE in italiano, anche se il testo originale è in inglese. "
    "Genera un riassunto di 3-5 frasi, tono neutro, che menzioni la fonte originale e il link. "
    "Non aggiungere commenti extra, solo il riassunto."
)


def _get_openrouter_client() -> "OpenAI | None":
    """Crea client OpenRouter se API key disponibile."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or not OPENAI_AVAILABLE:
        return None
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )


def _summarize_with_llm(client: "OpenAI", title: str, summary: str, source: str, link: str) -> str:
    """Genera riassunto usando LLM via OpenRouter."""
    user_prompt = (
        f"Titolo: {title}\n"
        f"Fonte: {source}\n"
        f"Link: {link}\n"
        f"Testo originale: {summary}\n\n"
        "Genera il riassunto in italiano (3-5 frasi) menzionando fonte e link."
    )
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()


def summarize_news(news_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Genera riassunti per le notizie via LLM o fallback a summary RSS.

    Args:
        news_items: Lista di notizie con title, link, summary, source.

    Returns:
        Lista di notizie arricchite con campo 'summary_llm'.
    """
    client = _get_openrouter_client()

    for item in news_items:
        if client:
            try:
                item["summary_llm"] = _summarize_with_llm(
                    client,
                    item["title"],
                    item.get("summary", ""),
                    item["source"],
                    item["link"],
                )
            except Exception as e:
                print(f"Errore LLM per '{item['title']}': {e}. Uso fallback RSS.")
                item["summary_llm"] = item.get("summary", "Nessun riassunto disponibile.")
        else:
            item["summary_llm"] = item.get("summary", "Nessun riassunto disponibile.")

    return news_items


if __name__ == "__main__":
    print("Modulo summarize.py - test con dati di esempio")
    test_news = [{
        "title": "Test AI News",
        "link": "https://example.com",
        "summary": "This is a test summary about AI advances.",
        "source": "Test Source",
    }]
    result = summarize_news(test_news)
    print(result[0].get("summary_llm", "N/A"))