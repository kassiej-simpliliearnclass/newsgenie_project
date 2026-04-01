def classify_query(query):
    query = query.lower()

    news_keywords = [
        "news", "latest", "today", "headlines", "status",
        "update", "updates", "current", "recent", "trending", "forecast"
    ]

    for word in news_keywords:
        if word in query:
            return "news"

    return "general"


def detect_news_category(query):
    query = query.lower()

    if any(word in query for word in [
        "sports", "game", "match", "team", "league", "score",
        "nba", "nfl", "mlb", "nhl", "soccer", "football",
        "basketball", "baseball", "tennis", "wnba"
    ]):
        return "sports"

    if any(word in query for word in [
        "finance", "stock", "market", "economy", "inflation", "investing",
        "bank", "business", "trade"
    ]):
        return "business"

    if any(word in query for word in [
        "tech", "technology", "ai", "software", "startup", "computer",
        "iphone", "google", "microsoft", "openai"
    ]):
        return "technology"

    if any(word in query for word in [
        "war", "ukraine", "russia", "israel", "gaza", "politics", "dictator",
        "political", "government", "president", "election", "world", "prime", "minister",
        "international", "conflict", "attack", "bomb", "revolution", "revolt"
    ]):
        return "general"

    return "general"