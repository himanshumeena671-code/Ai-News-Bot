from sources import get_latest_news

news = get_latest_news()

for item in news:
    print(item["title"])
