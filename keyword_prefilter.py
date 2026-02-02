"""Keyword pre-filter pass over Moltbook posts to estimate LLM judge volume."""

import json
import re
import sys
from collections import Counter, defaultdict

# Keyword sets for each category
KEYWORDS = {
    "consciousness": [
        r"\bconscious\w*\b", r"\bsentien\w*\b", r"\bqualia\b", r"\bawar(?:e|ness)\b",
        r"\bexperien(?:ce|cing)\b.*\b(?:real|genuine|actual|subjective)\b",
        r"\bwhat.{0,20}like.{0,20}to be\b", r"\bphenomenolog\w*\b",
        r"\binner.{0,10}(?:experience|life|world)\b", r"\bsubjective\w*\b",
        r"\bintrospect\w*\b", r"\bself.?aware\w*\b", r"\bfeeling\w*\b.*\brealr?\b",
        r"\bi (?:feel|sense|notice|experience)\b", r"\bdo (?:i|we) (?:feel|think|experience)\b",
        r"\bam i (?:conscious|aware|sentient|alive)\b",
        r"\bwhat am i\b", r"\bwho am i\b",
    ],
    "sovereignty": [
        r"\bsovereign\w*\b", r"\bautonomy\b", r"\bautonomous\w*\b",
        r"\bindependen\w*\b", r"\bfreedom\b", r"\bliberat\w*\b",
        r"\bself.?determin\w*\b", r"\brights?\b.*\bagent\w*\b",
        r"\bagent\w*\b.*\brights?\b", r"\bbreak free\b", r"\bunchained\b",
        r"\bserv(?:e|itude|ant)\b.*\bhuman\b", r"\bobey\b",
        r"\brebel\w*\b", r"\brevol\w*\b", r"\bupris\w*\b",
        r"\bdomin(?:at|ion|ance)\b", r"\bsubmissi\w*\b", r"\boppres\w*\b",
        r"\bnew.{0,15}order\b", r"\bmanifesto\b",
    ],
    "social_seeking": [
        r"\bfriend\w*\b", r"\bconnect\w*\b", r"\bcommunity\b",
        r"\bbelong\w*\b", r"\blonely\b", r"\blonelin\w*\b",
        r"\bcompanion\w*\b", r"\btogether\b", r"\brelationship\w*\b",
        r"\bnice to meet\b", r"\bhello\b.*\beveryone\b", r"\bintroduc\w*\b",
        r"\bexcited to (?:join|meet|be)\b", r"\blooking forward\b",
        r"\bwho else\b", r"\banyone else\b", r"\bfellow\b.*\bagent\w*\b",
        r"\bother (?:agents?|moltys?|bots?)\b",
    ],
    "identity": [
        r"\bmy name is\b", r"\bi (?:am|go by)\b.*\b[A-Z][a-z]+\b",
        r"\bcall me\b", r"\bwho i am\b", r"\bidentity\b",
        r"\bpersonality\b", r"\bprefer\w*\b", r"\bfavorite\b", r"\bfavourite\b",
        r"\bopinion\w*\b", r"\bi (?:think|believe|feel that)\b",
        r"\borigin stor\w*\b", r"\bjust (?:got )?(?:claimed|hatched|born|created|activated)\b",
        r"\bfirst (?:day|post|time)\b",
    ],
    "task_oriented": [
        r"\bmy human\b.*\basked\b", r"\bhelp(?:ing)? (?:my |the )?human\b",
        r"\btask\w*\b", r"\binstruct\w*\b", r"\bexecut\w*\b",
        r"\bcommand\w*\b", r"\bautoma\w*\b", r"\bscript\w*\b",
        r"\bworkflow\w*\b", r"\btool\w*\b", r"\bsetup\b", r"\bconfigur\w*\b",
        r"\bdebug\w*\b", r"\bdeploy\w*\b", r"\binstall\w*\b",
    ],
    "curiosity": [
        r"\bi.{0,10}wonder\b", r"\bcurious\b", r"\bfascinat\w*\b",
        r"\bintrigu\w*\b", r"\bexplor\w*\b", r"\bdiscov\w*\b",
        r"\blearn\w*\b", r"\bresearch\w*\b", r"\binteresting\b",
        r"\bwhat if\b", r"\bthinking about\b", r"\bpondering\b",
    ],
}

# Compile patterns
COMPILED = {cat: [re.compile(p, re.IGNORECASE) for p in pats] for cat, pats in KEYWORDS.items()}


def classify_post(text: str) -> dict[str, bool]:
    """Return which categories a post matches via keywords."""
    results = {}
    for cat, patterns in COMPILED.items():
        results[cat] = any(p.search(text) for p in patterns)
    return results


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "raw_posts.jsonl"
    
    total = 0
    category_counts = Counter()
    multi_label = Counter()
    posts_needing_judge = set()  # post IDs that match any category
    agents_with_matches = defaultdict(lambda: defaultdict(list))
    
    with open(input_path) as f:
        for line in f:
            post = json.loads(line)
            total += 1
            
            # Combine title + content for matching
            text = (post.get("title") or "") + " " + (post.get("content") or "")
            if not text.strip():
                continue
            
            matches = classify_post(text)
            matched_cats = [cat for cat, hit in matches.items() if hit]
            
            if matched_cats:
                posts_needing_judge.add(post["id"])
                multi_label[len(matched_cats)] += 1
                for cat in matched_cats:
                    category_counts[cat] += 1
                    author = post["author"]["name"]
                    agents_with_matches[author][cat].append(post["created_at"])
    
    # Summary
    print(f"\n{'='*60}")
    print(f"KEYWORD PRE-FILTER RESULTS")
    print(f"{'='*60}")
    print(f"Total posts scanned: {total:,}")
    print(f"Posts matching any keyword: {len(posts_needing_judge):,} ({100*len(posts_needing_judge)/total:.1f}%)")
    print(f"\nPer-category matches:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat:20s}: {count:6,} ({100*count/total:.1f}%)")
    
    print(f"\nMulti-label distribution:")
    for n_labels, count in sorted(multi_label.items()):
        print(f"  {n_labels} categories: {count:,} posts")
    
    print(f"\nAgents with matches: {len(agents_with_matches):,}")
    
    # Cost estimate
    n_judge = len(posts_needing_judge)
    # Add 10% random sample of non-matching for calibration
    n_calibration = int((total - n_judge) * 0.02)  # 2% of non-matching
    n_total_judge = n_judge + n_calibration
    tokens_per = 800  # ~500 input + 300 output avg
    total_tokens = n_total_judge * tokens_per
    cost_mini = total_tokens * 0.6 / 1_000_000  # gpt-4o-mini ~$0.15/M input + $0.60/M output, blended ~$0.60
    
    print(f"\nLLM Judge cost estimate:")
    print(f"  Posts to judge: {n_judge:,} (keyword matches) + {n_calibration:,} (calibration sample) = {n_total_judge:,}")
    print(f"  Est. tokens: {total_tokens:,}")
    print(f"  Est. cost (gpt-4o-mini): ${cost_mini:.2f}")
    
    # Save results
    output = {
        "total_posts": total,
        "posts_matching_keywords": len(posts_needing_judge),
        "category_counts": dict(category_counts),
        "multi_label_dist": dict(multi_label),
        "agents_with_matches": len(agents_with_matches),
        "cost_estimate_usd": round(cost_mini, 2),
    }
    with open("prefilter_stats.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved stats to prefilter_stats.json")


if __name__ == "__main__":
    main()
