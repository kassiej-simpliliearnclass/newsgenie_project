import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")


def clean_query(query):
    words_to_remove = [
        "latest", "news", "today", "headlines",
        "current", "recent", "updates", "about"
    ]
    query_words = query.lower().split()
    filtered_words = [word for word in query_words if word not in words_to_remove]
    return " ".join(filtered_words)


def get_news(category, query=None):
    cleaned_query = clean_query(query) if query else ""

    # First try: top headlines
    top_headlines_url = "https://newsapi.org/v2/top-headlines"
    top_params = {
        "apiKey": API_KEY,
        "country": "us",
        "pageSize": 5
    }

    if category != "general":
        top_params["category"] = category

    if cleaned_query:
        top_params["q"] = cleaned_query

    response = requests.get(top_headlines_url, params=top_params)
    data = response.json()

    articles = []

    if data.get("articles"):
        for article in data["articles"]:
            articles.append({
                "title": article["title"],
                "source": article["source"]["name"],
                "url": article["url"]
            })

    # Fallback: if no top-headlines results and we have a query,
    # search more broadly with /everything
    if not articles and cleaned_query:
        everything_url = "https://newsapi.org/v2/everything"
        everything_params = {
            "apiKey": API_KEY,
            "q": cleaned_query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 5
        }

        response = requests.get(everything_url, params=everything_params)
        data = response.json()

        if data.get("articles"):
            for article in data["articles"]:
                articles.append({
                    "title": article["title"],
                    "source": article["source"]["name"],
                    "url": article["url"]
                })

    return articles