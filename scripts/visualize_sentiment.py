import sqlite3
import pandas as pd
import plotly.express as px

DB_PATH = "data/election_comments.db"

def visualize_sentiment():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT sentiment_label, sentiment_score, analysis_timestamp FROM sentiment_analysis", conn)
    conn.close()

    sentiment_counts = df["sentiment_label"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    bar_figure = px.bar(sentiment_counts, x="Sentiment", y="Count", color="Sentiment",
                     title="Sentiment Analysis Counts",
                     labels={"Count": "Number of Comments", "Sentiment": "Sentiment Type"})
    bar_figure.show()

    pie_figure = px.pie(sentiment_counts, names="Sentiment", values="Count",
                     title="Sentiment Analysis Proportion")
    pie_figure.show()

    df["analysis_timestamp"] = pd.to_datetime(df["analysis_timestamp"])
    df["Date"] = df["analysis_timestamp"].dt.date
    sentiment_trends = df.groupby(["Date", "sentiment_label"]).size().reset_index(name="Count")

    line_chart = px.line(sentiment_trends, x="Date", y="Count", color="sentiment_label",
                        title="Sentiment Trends Over Time",
                        labels={"Count": "Number of Comments", "Date": "Date", "sentiment_label": "Sentiment"})
    line_chart.show()

if __name__ == "__main__":
    visualize_sentiment()
