from textblob import TextBlob
import sqlite3
from datetime import datetime

class SentimentAnalysis:
    def __init__(self, db_path):
        self.db_path = db_path

    def analyze_sentiment(self, comment_text):
        result = TextBlob(comment_text)
        sentiment_score = result.sentiment.polarity

        if sentiment_score > 0.1:
            sentiment_label = "Positive"
        elif sentiment_score < -0.1:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        return sentiment_label, sentiment_score

    def process_comments(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT comment_id, text FROM comments
        WHERE comment_id NOT IN (SELECT comment_id FROM sentiment_analysis)
        """)
        comments = cursor.fetchall()

        print(f"Analyzing sentiment for {len(comments)} comments...\n")
        for comment_id, text in comments:
            sentiment_label, sentiment_score = self.analyze_sentiment(text)
            analysis_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
            INSERT INTO sentiment_analysis (comment_id, sentiment_label, sentiment_score, analysis_timestamp)
            VALUES (?, ?, ?, ?)
            """, (comment_id, sentiment_label, sentiment_score, analysis_timestamp))

        conn.commit()
        conn.close()
        print("Sentiment analysis completed and results saved to the database.\n")
