# backend/app/services/sentiment_service.py

from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon', quiet=True)

def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    
    if sentiment_scores['compound'] >= 0.05:
        sentiment = 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    return {
        'sentiment': sentiment,
        'pos_score': sentiment_scores['pos'],
        'neg_score': sentiment_scores['neg'],
        'neu_score': sentiment_scores['neu'],
        'compound_score': sentiment_scores['compound']
    }
