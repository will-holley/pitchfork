"""
Scrapes all Pitchfork reviews from the API and caches them to the fs.
"""
import requests
import pandas as pd

# ============================================================
# Constants
# ============================================================

# 200 is the maximum page size allowed by the API.
PAGE_SIZE = 200
CACHE_FILE_PATH = "cache/reviews.pkl"

# ============================================================
# Utilities
# ============================================================

def fetch_page(offset: int):
    """
    Fetches a page of reviews from the Pitchfork API using limit/offset
    pagination.
    """
    res = requests.get(
        "https://pitchfork.com/api/v2/search",
        params={
            "types": "reviews",
            "sort": "publishdate+desc,position+asc",
            "size": PAGE_SIZE,
            "start": offset,
        },
    )
    return res.json()    

# ============================================================
# Main
# ============================================================

pages = []
index = 0

while True:
    print(f"Fetching page {index}")

    page = fetch_page(index * PAGE_SIZE)
    results = page["results"]["list"]

    if len(results) == 0:
        break
    
    pages.append(pd.DataFrame(results))
    
    index += 1

df = pd.concat(pages)
print(f"Fetched {len(df)} reviews. Caching...")
df.to_pickle("cache/reviews.pkl")