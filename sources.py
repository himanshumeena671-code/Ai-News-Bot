import feedparser

RSS_FEEDS = {
    "Rockstar": "https://www.rockstargames.com/newswire/rss",
    "IGN GTA": "https://feeds.ign.com/ign/all",
    "GameRant": "https://gamerant.com/feed/",
    "Dexerto": "https://www.dexerto.com/feed/"
}


KEYWORDS = [
    "gta",
    "gta 6",
    "gta vi",
    "grand theft auto",
    "rockstar"
]


def get_latest_news():
    news = []

    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", "")

                text = f"{title} {summary}".lower()

                if any(keyword in text for keyword in KEYWORDS):
                    news.append({
                        "source": source,
                        "title": title,
                        "summary": summary,
                        "link": entry.get("link", "")
                    })

        except Exception as e:
            print(f"{source}: {e}")

    return news
