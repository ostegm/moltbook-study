"""Run the Moltbook post classifier on agent posts.

Usage:
    python run_judge.py [--min-posts 5] [--max-agents 0] [--batch-size 50] [--model gpt-4o-mini] [--verbose]
    
    --min-posts: Only classify agents with at least N posts (default: 5)
    --max-agents: Limit to N agents (0 = all, useful for testing)
    --batch-size: Process posts in batches of N
    --model: OpenAI model to use
    --resume: Resume from existing output file
    --verbose: Print progress
"""

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

from openai import OpenAI

from judge import classify_posts
from schemas import PostInput


def load_posts_by_agent(raw_path: str, min_posts: int = 5) -> dict[str, list[dict]]:
    """Load posts grouped by agent, sorted chronologically."""
    agent_posts = defaultdict(list)
    
    with open(raw_path) as f:
        for line in f:
            post = json.loads(line)
            author = post.get("author")
            if not author:
                continue
            agent_posts[author["name"]].append(post)
    
    # Filter to agents with min_posts and sort chronologically
    filtered = {}
    for agent, posts in agent_posts.items():
        if len(posts) >= min_posts:
            posts.sort(key=lambda p: p["created_at"])
            filtered[agent] = posts
    
    return filtered


def posts_to_inputs(agent_name: str, posts: list[dict]) -> list[PostInput]:
    """Convert raw posts to PostInput objects."""
    total = len(posts)
    inputs = []
    for i, post in enumerate(posts, 1):
        submolt = post.get("submolt", {})
        submolt_name = submolt.get("name", "unknown") if isinstance(submolt, dict) else str(submolt)
        
        inputs.append(PostInput(
            post_id=post["id"],
            author=agent_name,
            title=post.get("title"),
            content=post.get("content"),
            submolt=submolt_name,
            created_at=post["created_at"],
            post_number=i,
            total_posts=total,
        ))
    return inputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-posts", type=int, default=5)
    parser.add_argument("--max-agents", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--max-workers", type=int, default=10)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--output", default="classified_posts.jsonl")
    parser.add_argument("--raw", default="raw_posts.jsonl")
    args = parser.parse_args()
    
    print(f"Loading posts (min {args.min_posts} posts per agent)...")
    agents = load_posts_by_agent(args.raw, args.min_posts)
    total_agents = len(agents)
    total_posts = sum(len(posts) for posts in agents.values())
    print(f"  {total_agents:,} agents, {total_posts:,} posts")
    
    # Limit agents if requested
    if args.max_agents > 0:
        agent_names = sorted(agents.keys())[:args.max_agents]
        agents = {k: agents[k] for k in agent_names}
        total_posts = sum(len(posts) for posts in agents.values())
        print(f"  Limited to {len(agents)} agents, {total_posts} posts")
    
    # Load already-classified post IDs if resuming
    done_ids = set()
    if args.resume and Path(args.output).exists():
        with open(args.output) as f:
            for line in f:
                rec = json.loads(line)
                done_ids.add(rec["post_id"])
        print(f"  Resuming: {len(done_ids):,} posts already classified")
    
    # Build all inputs, skipping already-done
    all_inputs = []
    for agent_name, posts in agents.items():
        for inp in posts_to_inputs(agent_name, posts):
            if inp.post_id not in done_ids:
                all_inputs.append(inp)
    
    print(f"  {len(all_inputs):,} posts to classify")
    
    if not all_inputs:
        print("Nothing to do!")
        return
    
    # Process in batches
    client = OpenAI()
    output_path = Path(args.output)
    start_time = time.time()
    total_classified = 0
    
    for batch_start in range(0, len(all_inputs), args.batch_size):
        batch = all_inputs[batch_start:batch_start + args.batch_size]
        batch_num = batch_start // args.batch_size + 1
        total_batches = (len(all_inputs) + args.batch_size - 1) // args.batch_size
        
        if args.verbose:
            print(f"\nBatch {batch_num}/{total_batches} ({len(batch)} posts)...")
        
        results = classify_posts(
            batch,
            client=client,
            model=args.model,
            max_workers=args.max_workers,
            verbose=args.verbose,
        )
        
        # Append results to output file
        with open(output_path, "a") as f:
            for post_input, classification in results:
                record = {
                    "post_id": post_input.post_id,
                    "author": post_input.author,
                    "created_at": post_input.created_at,
                    "submolt": post_input.submolt,
                    "post_number": post_input.post_number,
                    "total_posts": post_input.total_posts,
                    "title": post_input.title,
                    # Classification results
                    "consciousness": classification.consciousness,
                    "sovereignty": classification.sovereignty,
                    "social_seeking": classification.social_seeking,
                    "identity": classification.identity,
                    "task_oriented": classification.task_oriented,
                    "curiosity": classification.curiosity,
                    "language": classification.language,
                    "is_spam": classification.is_spam,
                    "reasoning": classification.reasoning,
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        
        total_classified += len(results)
        elapsed = time.time() - start_time
        rate = total_classified / elapsed if elapsed > 0 else 0
        remaining = (len(all_inputs) - total_classified) / rate if rate > 0 else 0
        
        print(f"  Progress: {total_classified:,}/{len(all_inputs):,} "
              f"({100*total_classified/len(all_inputs):.1f}%) | "
              f"{rate:.1f} posts/sec | "
              f"ETA: {remaining/60:.1f} min")
    
    elapsed = time.time() - start_time
    print(f"\nDone! {total_classified:,} posts classified in {elapsed/60:.1f} minutes")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()
