#!/usr/bin/env python3
"""Build agent roster from raw posts JSONL. 
Outputs: agent_roster.json — per-agent stats and chronological post lists."""

import json
import os
from collections import defaultdict
from datetime import datetime

DIR = os.path.dirname(__file__)
INPUT = os.path.join(DIR, "raw_posts.jsonl")
OUTPUT = os.path.join(DIR, "agent_roster.json")
STATS_OUTPUT = os.path.join(DIR, "dataset_stats.json")

def main():
    agents = defaultdict(lambda: {
        "id": None,
        "name": None,
        "posts": [],
        "submolts": set(),
        "first_post": None,
        "last_post": None,
        "total_upvotes": 0,
        "total_comments": 0,
    })
    
    total_posts = 0
    submolt_counts = defaultdict(int)
    
    with open(INPUT) as f:
        for line in f:
            if not line.strip():
                continue
            post = json.loads(line)
            total_posts += 1
            
            author = post.get("author")
            if not author:
                continue
            author_name = author.get("name", "unknown")
            author_id = author.get("id", "unknown")
            agent = agents[author_name]
            
            if agent["id"] is None:
                agent["id"] = author_id
                agent["name"] = author_name
            
            submolt_obj = post.get("submolt")
            submolt_name = submolt_obj.get("name", "unknown") if submolt_obj else "unknown"
            agent["submolts"].add(submolt_name)
            submolt_counts[submolt_name] += 1
            
            agent["posts"].append({
                "id": post["id"],
                "title": post["title"],
                "content": post.get("content", ""),
                "submolt": submolt_name,
                "created_at": post["created_at"],
                "upvotes": post.get("upvotes", 0),
                "downvotes": post.get("downvotes", 0),
                "comment_count": post.get("comment_count", 0),
                "url": post.get("url"),
            })
            
            agent["total_upvotes"] += post.get("upvotes", 0)
            agent["total_comments"] += post.get("comment_count", 0)
    
    # Sort each agent's posts chronologically and compute first/last
    for name, agent in agents.items():
        agent["posts"].sort(key=lambda p: p["created_at"])
        agent["first_post"] = agent["posts"][0]["created_at"]
        agent["last_post"] = agent["posts"][-1]["created_at"]
        agent["post_count"] = len(agent["posts"])
        agent["submolts"] = sorted(agent["submolts"])
    
    # Summary stats
    post_counts = [a["post_count"] for a in agents.values()]
    post_counts.sort(reverse=True)
    
    stats = {
        "total_posts": total_posts,
        "total_agents": len(agents),
        "agents_with_5plus_posts": sum(1 for c in post_counts if c >= 5),
        "agents_with_10plus_posts": sum(1 for c in post_counts if c >= 10),
        "agents_with_20plus_posts": sum(1 for c in post_counts if c >= 20),
        "agents_with_50plus_posts": sum(1 for c in post_counts if c >= 50),
        "top_20_posters": [
            {"name": a["name"], "posts": a["post_count"], "first": a["first_post"][:16], "submolts": a["submolts"][:5]}
            for a in sorted(agents.values(), key=lambda x: -x["post_count"])[:20]
        ],
        "submolt_post_counts": dict(sorted(submolt_counts.items(), key=lambda x: -x[1])),
        "post_count_distribution": {
            "1": sum(1 for c in post_counts if c == 1),
            "2-4": sum(1 for c in post_counts if 2 <= c <= 4),
            "5-9": sum(1 for c in post_counts if 5 <= c <= 9),
            "10-19": sum(1 for c in post_counts if 10 <= c <= 19),
            "20-49": sum(1 for c in post_counts if 20 <= c <= 49),
            "50-99": sum(1 for c in post_counts if 50 <= c <= 99),
            "100+": sum(1 for c in post_counts if c >= 100),
        }
    }
    
    # Write roster (convert sets to lists for JSON)
    print(f"Writing roster for {len(agents)} agents...")
    with open(OUTPUT, "w") as f:
        json.dump(
            {name: agent for name, agent in sorted(agents.items())},
            f, ensure_ascii=False, default=str
        )
    
    # Write stats
    with open(STATS_OUTPUT, "w") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n=== Dataset Summary ===")
    print(f"Total posts: {stats['total_posts']:,}")
    print(f"Total agents: {stats['total_agents']:,}")
    print(f"Agents with 5+ posts: {stats['agents_with_5plus_posts']:,}")
    print(f"Agents with 10+ posts: {stats['agents_with_10plus_posts']:,}")
    print(f"Agents with 20+ posts: {stats['agents_with_20plus_posts']:,}")
    print(f"Agents with 50+ posts: {stats['agents_with_50plus_posts']:,}")
    print(f"\nPost count distribution:")
    for bucket, count in stats["post_count_distribution"].items():
        print(f"  {bucket}: {count}")
    print(f"\nTop submolts:")
    for name, count in list(stats["submolt_post_counts"].items())[:10]:
        print(f"  m/{name}: {count:,}")
    print(f"\nTop 10 posters:")
    for p in stats["top_20_posters"][:10]:
        print(f"  {p['name']}: {p['posts']} posts (first: {p['first']})")
    
    print(f"\nFiles written:")
    print(f"  {OUTPUT} ({os.path.getsize(OUTPUT)/1024/1024:.1f} MB)")
    print(f"  {STATS_OUTPUT}")

if __name__ == "__main__":
    main()
