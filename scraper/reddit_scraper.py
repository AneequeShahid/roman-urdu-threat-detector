import praw
import os
import csv
from dotenv import load_dotenv

load_dotenv()

def run_scraper():
    print("Connecting to Reddit...")
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT", "roman-urdu-scraper")
    )
    
    subreddits = ["pakistan", "karachi", "lahore"]
    scam_keywords = [
        "fraud", "scam", "beware", "warning", "fake", "dhoka",
        "bewakoof mat bano", "lucky draw", "prize", "OTP",
        "account band", "urgent", "verify karein"
    ]
    
    scam_data = []
    legit_data = []
    
    os.makedirs("data/raw", exist_ok=True)
    
    print("Scraping for scam posts...")
    for sub in subreddits:
        try:
            subreddit = reddit.subreddit(sub)
            # Search for scam posts using keywords
            for keyword in scam_keywords:
                for post in subreddit.search(keyword, limit=50):
                    scam_data.append({
                        "text": f"{post.title} {post.selftext}".strip().replace("\n", " "),
                        "source": f"r/{sub}",
                        "upvotes": post.score,
                        "date": post.created_utc
                    })
                    # Get top comments
                    post.comments.replace_more(limit=0)
                    for comment in post.comments[:5]:
                        scam_data.append({
                            "text": comment.body.strip().replace("\n", " "),
                            "source": f"r/{sub}_comment",
                            "upvotes": comment.score,
                            "date": comment.created_utc
                        })
        except Exception as e:
            print(f"Error scraping scam posts from r/{sub}: {e}")
            
    print("Scraping for legitimate posts...")
    for sub in subreddits:
        try:
            subreddit = reddit.subreddit(sub)
            for post in subreddit.hot(limit=200):
                # Ensure it doesn't contain scam keywords
                text_lower = f"{post.title} {post.selftext}".lower()
                if not any(kw.lower() in text_lower for kw in scam_keywords):
                    legit_data.append({
                        "text": f"{post.title} {post.selftext}".strip().replace("\n", " "),
                        "source": f"r/{sub}",
                        "upvotes": post.score,
                        "date": post.created_utc
                    })
                    if len(legit_data) >= 500:
                        break
        except Exception as e:
            print(f"Error scraping legit posts from r/{sub}: {e}")
            
        if len(legit_data) >= 500:
            break
            
    # Combine and save
    print("Saving to data/raw/reddit_scam_raw.csv...")
    with open("data/raw/reddit_scam_raw.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "source", "upvotes", "date"])
        writer.writeheader()
        writer.writerows(scam_data)
        writer.writerows(legit_data)
        
    print(f"\n--- Scraping Summary ---")
    print(f"Scam examples collected: {len(scam_data)}")
    print(f"Legitimate examples collected: {len(legit_data)}")

if __name__ == "__main__":
    run_scraper()
