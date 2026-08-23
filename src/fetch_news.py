"""Modulo per il recupero delle notizie AI via RSS usando feedparser."""

import feedparser
from datetime import datetime
from typing import List, Dict, Any


RSS_FEEDS = [
    "https://www.marktechpost.com/feed/",
    "https://huggingface.co/blog/feed.xml",
    "https://openai.com/news/rss.xml",
]


def fetch_latest_ai_news(max_items: int = 3) -> List[Dict[str, Any]]:
    """Recupera le ultime notizie AI dai feed RSS.

    Args:
        max_items: Numero massimo di notizie da restituire (default 3).

    Returns:
        Lista di dizionari con chiavi: title, link, published, summary, source.
    """
    all_entries = []

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            if feed.bozo and feed.bozo_exception:
                print(f"Warning: Errore parsing feed {feed_url}: {feed.bozo_exception}")

            for entry in feed.entries:
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])

                all_entries.append({
                    "title": entry.get("title", "").strip(),
                    "link": entry.get("link", "").strip(),
                    "published": published,
                    "summary": entry.get("summary", "").strip(),
                    "source": feed.feed.get("title", feed_url),
                })
        except Exception as e:
            print(f"Errore recupero feed {feed_url}: {e}")
            continue

    all_entries.sort(key=lambda x: x["published"] or datetime.min, reverse=True)

    seen_titles = set()
    deduplicated = []
    for entry in all_entries:
        title_lower = entry["title"].lower()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            deduplicated.append(entry)

    return deduplicated[:max_items]


if __name__ == "__main__":
    news = fetch_latest_ai_news()
    for i, item in enumerate(news, 1):
        print(f"{i}. {item['title']} ({item['source']})")
        print(f"   {item['link']}")
        print(f"   {item['published']}")
        print()