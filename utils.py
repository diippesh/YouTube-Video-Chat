import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url_or_id:str)->str:
    """
    Extract youtube video id from a full url
    """
    patterns = [
    r"(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})",
    r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
    ]
    
    for pattern in patterns:
        match = re.search(pattern,url_or_id)
        if match:
            return match.group(1)
        
        return url_or_id
    
def load_english_transcript(video_url_or_id:str)->str:
    """
    Load English transcript from youtube.
    raise error if english transcript is not available
    """
    video_id = extract_video_id(video_url_or_id)
    
    try:
        # Get the transcript using the API instance
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=['en'])
        print(len(transcript))
        text = " ".join(item.text for item in transcript)
        return re.sub(r'\s+'," ",text).strip()
    except Exception as e:
        raise Exception(f'English transcript not available for this video: {str(e)}')

if __name__ == "__main__":
    ans = load_english_transcript('https://youtu.be/dvx-DWWVTik?si=7nKU_2zo3EGe7HJZ')
    