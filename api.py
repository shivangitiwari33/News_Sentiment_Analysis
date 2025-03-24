from fastapi import FastAPI
from utils import (
    get_news_articles, 
    analyze_sentiment, 
    comparative_analysis, 
    generate_hindi_tts, 
    extract_topics
)

app = FastAPI()

@app.get("/news")
def fetch_news(company: str):
    print(f"[INFO] Fetching news for: {company}")
    
    articles = get_news_articles(company)

    if not articles:
        return {"Company": company, "Articles": [], "Message": "No articles found"}

    for article in articles:
        article["sentiment"] = analyze_sentiment(article["summary"])
        article["topics"] = extract_topics(article["summary"])

    comparison = comparative_analysis(articles)

    audio_file = generate_hindi_tts(articles)

    sentiment_count = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment_count[article["sentiment"]] += 1

    final_sentiment = (
        "Overall coverage is mostly positive."
        if sentiment_count["Positive"] > sentiment_count["Negative"]
        else "Overall coverage raises some concerns."
    )

    return {
        "Company": company,
        "Articles": [
            {
                "Title": a["title"],
                "Summary": a["summary"],
                "Sentiment": a["sentiment"],
                "Topics": a["topics"]
            }
            for a in articles
        ],
        "Comparative Sentiment Score": comparison,
        "Final Sentiment Analysis": final_sentiment,
        "Audio": audio_file
    }
