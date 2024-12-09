import sqlite3
import pandas as pd
from scripts.fetch_comments import fetch_comments_from_videos
from scripts.search_videos import search_videos
from scripts.database_setup import create_database
from scripts.sentiment_analysis import SentimentAnalysis
from scripts.visualize_sentiment import visualize_sentiment

DB_PATH = "data/election_comments.db"

if __name__ == "__main__":
    create_database(DB_PATH) #creating database 

    conn = sqlite3.connect(DB_PATH) #connecting to database
    print(f"Connected to database: {DB_PATH}\n") #debugging

    query = "US 2024 presidential election debate" #query search for vids
    max_videos = 10

    video_data = search_videos(query, max_results=max_videos)
    video_ids = [video["video_id"] for video in video_data]

    print(f"Fetching comments for {len(video_ids)} videos...")
    all_comments = fetch_comments_from_videos(video_ids)

    total_comments = 0 
    cursor = conn.cursor()
    for video in video_data:
        video_id = video["video_id"]
        title = video["title"]
        description = video["description"]
        comments = all_comments.get(video_id, [])
        total_comments += len(comments)
        for comment in comments:
            comment_id = comment["id"]
            user_id = comment["author"] 
            text = comment["text"]
            timestamp = comment["publishedAt"] 
            like_count = comment["likeCount"]

            cursor.execute("""
            INSERT OR IGNORE INTO comments (video_id, comment_id, user_id, text, timestamp, like_count, reply_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (video_id, comment_id, user_id, text, timestamp, like_count, 0))

    conn.commit()
    print(f"Total comments fetched: {total_comments}\n")

    sentiment_analyzer = SentimentAnalysis(DB_PATH)
    sentiment_analyzer.process_comments()

    print("Visualizing sentiment analysis results...\n")
    visualize_sentiment()

    df = pd.read_sql_query("SELECT * FROM sentiment_analysis", conn)
    print("Sentiment analysis table:\n")
    print(df.head())

    conn.close()
    print("Database connection closed.\n")

   
