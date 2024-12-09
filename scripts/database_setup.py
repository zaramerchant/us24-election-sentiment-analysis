import sqlite3
import os

def create_database(db_path="youtube_comments.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #comments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incremented ID for each record
        video_id TEXT,                         -- YouTube video ID
        comment_id TEXT UNIQUE,                -- Unique ID for each comment
        user_id TEXT,                          -- YouTube user ID (if available)
        text TEXT,                             -- The comment text
        timestamp DATETIME,                    -- When the comment was posted
        like_count INTEGER,                    -- Number of likes for the comment
        reply_count INTEGER                    -- Number of replies to the comment
    )
    """)

    #sentiment table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sentiment_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incremented ID for each record
        comment_id TEXT,                       -- References the `comment_id` in the `comments` table
        sentiment_label TEXT,                  -- Sentiment label: positive, negative, or neutral
        sentiment_score REAL,                  -- Sentiment score (e.g., polarity)
        analysis_timestamp DATETIME,           -- When the sentiment analysis was performed
        FOREIGN KEY (comment_id) REFERENCES comments (comment_id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized at: {db_path}\n")

if __name__ == "__main__":
    create_database()
