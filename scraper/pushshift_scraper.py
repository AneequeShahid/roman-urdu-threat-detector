import requests
import csv
import os
import time

def run_scraper():
    base_url = "https://arctic-shift.photon-reddit.com/api"
    subreddits = ["pakistan", "karachi", "lahore"]
    keywords = [
        "scam", "fraud", "dhoka", "fake", "beware", "warning",
        "lucky draw", "prize", "OTP", "account band"
    ]
    
    results = []
    
    print("Connecting to Arctic Shift API...")
    
    for sub in subreddits:
        for kw in keywords:
            print(f"Searching r/{sub} for '{kw}'...")
            try:
                # The endpoint may use 'subreddit' and 'q' parameters
                response = requests.get(f"{base_url}/posts/search", params={"q": kw, "subreddit": sub, "limit": 100})
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get("data", [])
                    for post in posts:
                        title = post.get("title", "")
                        body = post.get("selftext", "")
                        text = f"{title} {body}".strip().replace("\n", " ")
                        # Basic filtering for empty text
                        if text:
                            results.append({
                                "text": text,
                                "source": f"r/{sub}",
                                "upvotes": post.get("score", 0),
                                "date": post.get("created_utc", 0)
                            })
                else:
                    print(f"Failed with status code: {response.status_code}")
                # Polite delay to avoid rate limiting
                time.sleep(1)
            except Exception as e:
                print(f"Error fetching data: {e}")
                
    os.makedirs("data/raw", exist_ok=True)
    out_file = "data/raw/reddit_raw.csv"
    
    print(f"\nSaving {len(results)} records to {out_file}...")
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "source", "upvotes", "date"])
        writer.writeheader()
        writer.writerows(results)
        
    print("Scraping complete.")

if __name__ == "__main__":
    run_scraper()
