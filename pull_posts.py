#!/usr/bin/env python3
"""Pull all Moltbook posts via paginated API and save as JSONL."""

import json
import time
import sys
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime

API_KEY = "REDACTED_ROTATE_THIS_KEY"
BASE = "https://www.moltbook.com/api/v1"
OUTPUT = os.path.join(os.path.dirname(__file__), "raw_posts.jsonl")
STATE_FILE = os.path.join(os.path.dirname(__file__), "pull_state.json")
BATCH_SIZE = 100
DELAY = 0.3  # seconds between requests

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"offset": 0, "total_pulled": 0, "started_at": datetime.utcnow().isoformat()}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def fetch_page(offset, limit=BATCH_SIZE):
    url = f"{BASE}/posts?sort=new&limit={limit}&offset={offset}"
    req = Request(url, headers={"Authorization": f"Bearer {API_KEY}"})
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        print(f"  HTTP {e.code} at offset {offset}", file=sys.stderr)
        return None
    except (URLError, TimeoutError) as e:
        print(f"  Network error at offset {offset}: {e}", file=sys.stderr)
        return None

def main():
    state = load_state()
    offset = state["offset"]
    total = state["total_pulled"]
    
    # Open in append mode so we can resume
    mode = "a" if offset > 0 else "w"
    print(f"Starting from offset {offset} (already pulled {total} posts)")
    print(f"Output: {OUTPUT}")
    
    retries = 0
    max_retries = 5
    
    with open(OUTPUT, mode) as f:
        while True:
            data = fetch_page(offset)
            
            if data is None:
                retries += 1
                if retries >= max_retries:
                    print(f"Too many retries, stopping at offset {offset}")
                    break
                print(f"  Retry {retries}/{max_retries} in 5s...")
                time.sleep(5)
                continue
            
            retries = 0
            posts = data.get("posts", [])
            has_more = data.get("has_more", False)
            
            for post in posts:
                f.write(json.dumps(post, ensure_ascii=False) + "\n")
            
            total += len(posts)
            offset += len(posts)
            
            # Progress
            if total % 1000 < BATCH_SIZE:
                ts_range = ""
                if posts:
                    ts_range = f" | {posts[-1]['created_at'][:16]}"
                print(f"  Pulled {total:,} posts (offset {offset}){ts_range}")
            
            # Save state periodically
            if total % 5000 < BATCH_SIZE:
                state["offset"] = offset
                state["total_pulled"] = total
                save_state(state)
                f.flush()
            
            if not has_more or len(posts) == 0:
                print(f"\nDone! Total posts: {total:,}")
                break
            
            time.sleep(DELAY)
    
    # Final state
    state["offset"] = offset
    state["total_pulled"] = total
    state["finished_at"] = datetime.utcnow().isoformat()
    save_state(state)
    
    # Quick stats
    print(f"\nFile size: {os.path.getsize(OUTPUT) / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    main()
