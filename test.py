from sources import get_latest_news

news = get_latest_news()

print("=" * 50)
print(f"Found {len(news)} news articles")
print("=" * 50)

for item in news:
    print(f"Source : {item['source']}")
    print(f"Title  : {item['title']}")
    print(f"Link   : {item['link']}")
    print("-" * 50)
