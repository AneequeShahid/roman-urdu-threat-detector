import csv
import os
import itertools
from youtubesearchpython import VideosSearch
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR

def is_roman_urdu(text):
    # Simple heuristic to identify Roman Urdu
    urdu_words = ['hai', 'kya', 'aur', 'main', 'bhi', 'se', 'ko', 'ye', 'hain', 'ki', 'ka', 'nahi']
    text_lower = text.lower()
    for w in urdu_words:
        if f" {w} " in f" {text_lower} ":
            return True
    return False

def run_scraper():
    queries = [
        "pakistan online scam",
        "pakistan fraud whatsapp",
        "OTP scam pakistan"
    ]
    
    downloader = YoutubeCommentDownloader()
    results = []
    
    print("Starting YouTube Scraper...")
    
    for query in queries:
        print(f"Searching YouTube for: '{query}'")
        try:
            videosSearch = VideosSearch(query, limit=5)
            search_results = videosSearch.result()['result']
            
            for video in search_results:
                video_url = video['link']
                print(f"Fetching comments for {video_url}...")
                
                try:
                    comments = downloader.get_comments_from_url(video_url, sort_by=SORT_BY_POPULAR)
                    
                    count = 0
                    for comment in itertools.islice(comments, 100):  # limit to top 100 comments per video
                        text = comment['text'].replace('\n', ' ').strip()
                        if text and is_roman_urdu(text):
                            results.append({
                                "text": text,
                                "source": "YouTube Comments",
                                "url": video_url
                            })
                        count += 1
                except Exception as e:
                    print(f"Failed to fetch comments for {video_url}: {e}")
                    
        except Exception as e:
            print(f"Error processing query '{query}': {e}")
            
    os.makedirs("data/raw", exist_ok=True)
    out_file = "data/raw/youtube_comments_raw.csv"
    
    print(f"\nSaving {len(results)} Roman Urdu comments to {out_file}...")
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "source", "url"])
        writer.writeheader()
        writer.writerows(results)
        
    print("YouTube scraping complete.")

if __name__ == "__main__":
    run_scraper()
