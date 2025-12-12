import feedparser

RSS_URL = "https://pypi.org/rss/project/ancientlinesoftheworld/releases.xml"

def get_releases():
    feed = feedparser.parse(RSS_URL)
    result = []

    for entry in feed.entries:
        block = (
            f"📌 Version:   {entry.title}\n"
            f"📅 Published: {entry.published}\n"
            f"🔗 URL:       {entry.link}\n"
            f"{'-' * 40}"
        )
        result.append(block)

    return "\n".join(result)
