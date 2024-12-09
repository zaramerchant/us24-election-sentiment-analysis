import googleapiclient.discovery
from config import API_KEY

def fetch_comments(video_id, max_results=100):
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY
    )

    try:
        comments = [] 
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        )

        while request:
            response = request.execute()
            for item in response.get("items", []):
                top_comment = item["snippet"]["topLevelComment"]["snippet"]
                comment = {
                    "id": item["id"],
                    "text": top_comment["textDisplay"], 
                    "author": top_comment.get("authorChannelId", {}).get("value", "Anonymous"), 
                    "publishedAt": top_comment["publishedAt"],  
                    "likeCount": top_comment.get("likeCount", 0), 
                }
                comments.append(comment)

            request = youtube.commentThreads().list_next(request, response)

        return comments

    except Exception as e:
        print(f"Error fetching comments for video ID {video_id}: {e}")
        return []

def fetch_comments_from_videos(video_ids, max_results=100):
    all_comments = {}
    for video_id in video_ids:
        print(f"Fetching comments for video ID: {video_id}")
        comments = fetch_comments(video_id, max_results)
        all_comments[video_id] = comments
    return all_comments
