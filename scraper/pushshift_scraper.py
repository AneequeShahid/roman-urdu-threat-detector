import requests
import csv
import os
import time

def run_scraper():
    subreddits = ["pakistan", "karachi", "lahore"]
    keywords = [
        "scam", "fraud", "dhoka", "fake", "beware", "warning",
        "lucky draw", "prize", "OTP", "account band"
    ]
    
    headers = {
        "User-Agent": "roman-urdu-scraper/1.0"
    }
    
    results = []
    
    print("Connecting to old.reddit.com API...")
    
    for sub in subreddits:
        for kw in keywords:
            print(f"Searching r/{sub} for '{kw}'...")
            try:
                url = f"https://old.reddit.com/r/{sub}/search.json"
                params = {
                    "q": kw,
                    "restrict_sr": 1,
                    "sort": "new",
                    "limit": 100
                }
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    children = data.get("data", {}).get("children", [])
                    for child in children:
                        post = child.get("data", {})
                        title = post.get("title", "")
                        body = post.get("selftext", "")
                        text = f"{title} {body}".strip().replace("\n", " ")
                        
                        if text:
                            results.append({
                                "text": text,
                                "source": f"r/{sub}",
                                "upvotes": post.get("score", 0),
                                "date": post.get("created_utc", 0)
                            })
                else:
                    print(f"Failed with status code: {response.status_code}")
                    
                # Rate limit 1 req / 2 seconds
                time.sleep(2)
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
