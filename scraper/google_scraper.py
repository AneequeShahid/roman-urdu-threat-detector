import csv
import time
import os
import requests
from bs4 import BeautifulSoup
from googlesearch import search

def run_scraper():
    queries = [
        "site:reddit.com/r/pakistan scam",
        "site:reddit.com/r/pakistan fraud",
        "site:reddit.com/r/pakistan dhoka"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    results = []
    
    print("Starting Google Search Scraper...")
    
    for query in queries:
        print(f"Searching Google for: '{query}'")
        try:
            # googlesearch-python returns an iterator of URLs
            urls = search(query, num_results=20, lang="en")
            for url in urls:
                print(f"Fetching: {url}")
                try:
                    resp = requests.get(url, headers=headers, timeout=10)
                    if resp.status_code == 200:
                        soup = BeautifulSoup(resp.text, "html.parser")
                        # Basic extraction: Reddit's DOM changes often, but we can grab paragraph text
                        paragraphs = soup.find_all("p")
                        text_content = " ".join([p.get_text() for p in paragraphs]).strip()
                        
                        if text_content:
                            results.append({
                                "text": text_content,
                                "source": "Google Search - Reddit",
                                "url": url
                            })
                    else:
                        print(f"Failed with status code: {resp.status_code}")
                except Exception as e:
                    print(f"Failed to fetch {url}: {e}")
                
                # Polite delay
                time.sleep(2)
        except Exception as e:
            print(f"Error during Google search: {e}")
            
    os.makedirs("data/raw", exist_ok=True)
    out_file = "data/raw/google_reddit_raw.csv"
    
    print(f"\nSaving {len(results)} records to {out_file}...")
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "source", "url"])
        writer.writeheader()
        writer.writerows(results)
        
    print("Google scraping complete.")

if __name__ == "__main__":
    run_scraper()
