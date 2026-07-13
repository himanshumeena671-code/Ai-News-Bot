import feedparser

RSS_URL = (
    "https://news.google.com/rss/search?"
    "q=%22GTA+6%22+OR+%22Grand+Theft+Auto+VI%22+OR+Rockstar"
    "&hl=en-US&gl=US&ceid=US:en"
)

def get_latest_news():
    feed = feedparser.parse(RSS_URL)

    news = []

    for entry in feed.entries:
        news.append({
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "link": entry.get("link", ""),
            "source": entry.get("source", {}).get("title", "Google News")
        })

    return news
