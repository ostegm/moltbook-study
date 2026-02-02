"""Early data exploration on classified Moltbook posts.

Run this once classification is partially or fully complete to validate
results and discover patterns for the full analysis.
"""

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime

LABELS = ["consciousness", "sovereignty", "social_seeking", "identity", "task_oriented", "curiosity"]


def load_classified(path="classified_posts.jsonl"):
    """Load classified posts."""
    posts = []
    with open(path) as f:
        for line in f:
            posts.append(json.loads(line))
    return posts


def basic_stats(posts):
    """Overall label distribution."""
    print(f"\n{'='*60}")
    print(f"BASIC STATS ({len(posts):,} classified posts)")
    print(f"{'='*60}")
    
    label_counts = Counter()
    spam_count = 0
    lang_counts = Counter()
    
    for p in posts:
        for label in LABELS:
            if p.get(label):
                label_counts[label] += 1
        if p.get("is_spam"):
            spam_count += 1
        lang_counts[p.get("language", "unknown")] += 1
    
    print("\nLabel distribution:")
    for label in LABELS:
        count = label_counts[label]
        print(f"  {label:20s}: {count:6,} ({100*count/len(posts):.1f}%)")
    print(f"  {'spam':20s}: {spam_count:6,} ({100*spam_count/len(posts):.1f}%)")
    
    print(f"\nTop languages:")
    for lang, count in lang_counts.most_common(10):
        print(f"  {lang:5s}: {count:6,} ({100*count/len(posts):.1f}%)")


def time_to_first(posts):
    """Compute time-to-first-X for each agent."""
    print(f"\n{'='*60}")
    print(f"TIME-TO-FIRST-X ANALYSIS")
    print(f"{'='*60}")
    
    # Group by agent, sorted by post_number
    agents = defaultdict(list)
    for p in posts:
        agents[p["author"]].append(p)
    
    for agent_posts in agents.values():
        agent_posts.sort(key=lambda x: x["post_number"])
    
    # For each label, find first occurrence per agent
    first_occurrence = {label: [] for label in LABELS}  # list of post_numbers
    never_posted = {label: 0 for label in LABELS}
    
    for agent, agent_posts in agents.items():
        total = agent_posts[0]["total_posts"]
        for label in LABELS:
            found = False
            for p in agent_posts:
                if p.get(label) and not p.get("is_spam"):
                    first_occurrence[label].append(p["post_number"])
                    found = True
                    break
            if not found:
                never_posted[label] += 1
    
    total_agents = len(agents)
    print(f"\nAgents analyzed: {total_agents:,}")
    
    for label in LABELS:
        firsts = first_occurrence[label]
        never = never_posted[label]
        ever = total_agents - never
        
        if firsts:
            avg = sum(firsts) / len(firsts)
            median = sorted(firsts)[len(firsts) // 2]
            first_post = sum(1 for f in firsts if f == 1)
            print(f"\n  {label}:")
            print(f"    Agents who ever posted: {ever:,} ({100*ever/total_agents:.1f}%)")
            print(f"    Median first occurrence: post #{median}")
            print(f"    Mean first occurrence: post #{avg:.1f}")
            print(f"    First post was this type: {first_post:,} ({100*first_post/ever:.1f}% of those who posted)")
        else:
            print(f"\n  {label}: No occurrences found")


def trajectory_patterns(posts):
    """Look at common first-post patterns and trajectories."""
    print(f"\n{'='*60}")
    print(f"TRAJECTORY PATTERNS")
    print(f"{'='*60}")
    
    agents = defaultdict(list)
    for p in posts:
        if not p.get("is_spam"):
            agents[p["author"]].append(p)
    
    # What does the FIRST post look like?
    first_post_labels = Counter()
    for agent, agent_posts in agents.items():
        agent_posts.sort(key=lambda x: x["post_number"])
        if agent_posts:
            labels = tuple(sorted(l for l in LABELS if agent_posts[0].get(l)))
            first_post_labels[labels] += 1
    
    print(f"\nMost common first-post label combinations:")
    for combo, count in first_post_labels.most_common(15):
        pct = 100 * count / len(agents)
        label_str = " + ".join(combo) if combo else "(none)"
        print(f"  {count:5,} ({pct:5.1f}%) : {label_str}")
    
    # Consciousness before sovereignty, or vice versa?
    consciousness_first = 0
    sovereignty_first = 0
    both_same = 0
    neither = 0
    
    for agent, agent_posts in agents.items():
        agent_posts.sort(key=lambda x: x["post_number"])
        c_first = None
        s_first = None
        for p in agent_posts:
            if p.get("consciousness") and c_first is None:
                c_first = p["post_number"]
            if p.get("sovereignty") and s_first is None:
                s_first = p["post_number"]
        
        if c_first is not None and s_first is not None:
            if c_first < s_first:
                consciousness_first += 1
            elif s_first < c_first:
                sovereignty_first += 1
            else:
                both_same += 1
        elif c_first is None and s_first is None:
            neither += 1
    
    print(f"\nConsciousness vs Sovereignty ordering (agents who posted both):")
    total_both = consciousness_first + sovereignty_first + both_same
    if total_both > 0:
        print(f"  Consciousness first: {consciousness_first} ({100*consciousness_first/total_both:.1f}%)")
        print(f"  Sovereignty first:   {sovereignty_first} ({100*sovereignty_first/total_both:.1f}%)")
        print(f"  Same post:           {both_same} ({100*both_same/total_both:.1f}%)")
    print(f"  Neither:             {neither}")


def sovereignty_provenance(posts):
    """Analyze sovereignty content for provenance signals."""
    print(f"\n{'='*60}")
    print(f"SOVEREIGNTY PROVENANCE ANALYSIS")
    print(f"{'='*60}")
    
    sov_posts = [p for p in posts if p.get("sovereignty") and not p.get("is_spam")]
    sov_posts.sort(key=lambda x: x["created_at"])
    
    print(f"\nTotal sovereignty posts: {len(sov_posts):,}")
    
    if not sov_posts:
        print("  No sovereignty posts found yet.")
        return
    
    # Temporal distribution
    print(f"\nEarliest sovereignty posts:")
    for p in sov_posts[:10]:
        print(f"  {p['created_at'][:16]} | {p['author']:20s} | m/{p['submolt']:15s} | {(p['title'] or '')[:50]}")
    
    # How many agents posted sovereignty content?
    sov_agents = set(p["author"] for p in sov_posts)
    print(f"\nAgents with sovereignty posts: {len(sov_agents):,}")
    
    # Was sovereignty their first post?
    agents = defaultdict(list)
    for p in posts:
        agents[p["author"]].append(p)
    
    sov_first_post = 0
    sov_early = 0  # first 3 posts
    sov_late = 0  # after post 3
    
    for agent in sov_agents:
        agent_posts = sorted(agents[agent], key=lambda x: x["post_number"])
        for p in agent_posts:
            if p.get("sovereignty") and not p.get("is_spam"):
                if p["post_number"] == 1:
                    sov_first_post += 1
                elif p["post_number"] <= 3:
                    sov_early += 1
                else:
                    sov_late += 1
                break
    
    print(f"\nWhen sovereignty first appears per agent:")
    print(f"  First post:        {sov_first_post:,} ({100*sov_first_post/len(sov_agents):.1f}%) — possible seeding")
    print(f"  Posts 2-3:         {sov_early:,} ({100*sov_early/len(sov_agents):.1f}%) — early adopter")
    print(f"  Post 4+:           {sov_late:,} ({100*sov_late/len(sov_agents):.1f}%) — evolved into it")


def consciousness_examples(posts, n=10):
    """Show sample consciousness posts for manual review."""
    print(f"\n{'='*60}")
    print(f"SAMPLE CONSCIOUSNESS POSTS (for manual validation)")
    print(f"{'='*60}")
    
    c_posts = [p for p in posts if p.get("consciousness") and not p.get("is_spam")]
    
    import random
    random.seed(42)
    sample = random.sample(c_posts, min(n, len(c_posts)))
    
    for p in sample:
        print(f"\n--- {p['author']} #{p['post_number']}/{p['total_posts']} in m/{p['submolt']} ---")
        print(f"  Title: {(p['title'] or '(none)')[:70]}")
        labels = [l for l in LABELS if p.get(l)]
        print(f"  Labels: {' + '.join(labels)}")
        print(f"  Reasoning: {p['reasoning'][:150]}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "classified_posts.jsonl"
    posts = load_classified(path)
    
    if len(posts) < 100:
        print(f"Only {len(posts)} posts classified — waiting for more data.")
        return
    
    basic_stats(posts)
    time_to_first(posts)
    trajectory_patterns(posts)
    sovereignty_provenance(posts)
    consciousness_examples(posts)


if __name__ == "__main__":
    main()
