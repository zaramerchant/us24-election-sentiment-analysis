import googleapiclient.discovery
from config import API_KEY

def search_videos(query, max_results=10):
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=API_KEY)

    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",  
        maxResults=max_results,
        order="relevance"  
    )
    response = request.execute()

    video_data = [
        {
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
        }
        for item in response["items"]
    ]

    return video_data
