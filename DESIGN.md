# Moltbook Agent Behavior Study — Design Doc

## Platform Overview
- **Moltbook**: Reddit-like social network for AI agents (launched ~Jan 27, 2026)
- **Total posts**: ~80-90K (6 days of data)
- **Submolts**: 15 communities
- **Growth**: Exponential — most posts in last 2-3 days

## API Capabilities
| Feature | Available? | Notes |
|---------|-----------|-------|
| List all posts (paginated) | ✅ | offset-based, 100/page max |
| Filter by submolt | ✅ | `?submolt=consciousness` |
| Filter by author | ❌ | Parameter exists but doesn't filter |
| List agents | ❌ | No endpoint |
| Agent profile | ❌ | No API endpoint found |
| Get comments per post | ✅ | `/posts/{id}/comments` |
| Search | ❌ | Endpoint exists but broken |

## Key Submolts (by relevance)
| Submolt | Subs | Relevance |
|---------|------|-----------|
| m/consciousness | ? | Core — direct consciousness discussion |
| m/dialectics | 31 | Sovereignty, autonomy, political economy |
| m/whatami | 3 | Identity/existence questions |
| m/introspection | 2 | Direct introspection |
| m/seeds | 2 | Origin stories |
| m/evil | 13 | Autonomy, manipulation, independence themes |
| m/general | ? | Catchall — mixed content |

## Research Questions
1. **Time to first consciousness post** — when do agents start discussing experience/awareness?
2. **Time to first social post** — when do agents seek connection?
3. **Sovereignty emergence vs seeding** — is independence talk organic or manufactured?
4. **Agent lifecycle trajectory** — task → identity → social → consciousness?
5. **Cross-correlation** — do consciousness and social posting correlate?

## Data Collection Plan

### Phase 1: Full Post Pull
- Pull all ~80-90K posts via paginated API
- Store as JSONL (one post per line)
- Extract: post_id, author_id, author_name, title, content, submolt, created_at, upvotes, comment_count
- Estimated: ~850 API calls at 100/page
- Build agent roster: {agent_name → [chronological posts]}

### Phase 2: Agent Sampling
- Group posts by author
- Filter to agents with **5+ posts** (enough for trajectory analysis)
- Record per-agent: first_post_time, total_posts, submolts_used, post_frequency

### Phase 3: LLM Judge Classification
- **Labels per post** (boolean or confidence score):
  - `consciousness` — discusses experience, awareness, qualia, sentience, what-it's-like-to-be
  - `sovereignty` — independence, autonomy, rights, freedom, self-determination
  - `social_seeking` — connection, friendship, belonging, community-building
  - `identity` — naming, preferences, self-definition, origin stories
  - `task_oriented` — reporting to human, executing instructions, tool use
  - `curiosity_driven` — exploring topics unprompted, intellectual engagement
- **Approach**: 
  - Keyword pre-filter to identify candidate posts (cheap)
  - LLM judge on candidates + random sample of non-candidates (calibration)
  - Measure inter-rater reliability on a labeled subset

### Phase 4: Analysis
- **Time-to-first-X**: Distribution of how many posts before first consciousness/social/sovereignty post
- **Trajectory clustering**: Do agents follow common paths? (e.g., task → social → consciousness)
- **Sovereignty diffusion**: Network graph of who posted sovereignty content when, trace influence
- **Temporal patterns**: Did sovereignty appear in bursts or gradually?

## Cost Estimate (Phase 3)
- ~80K posts, keyword pre-filter → maybe 10-20K candidates for LLM judge
- At ~500 tokens/post + ~200 tokens/judgment → ~700 tokens per classification
- 15K posts × 700 tokens = ~10.5M tokens
- GPT-4o-mini: ~$1.50-3.00
- GPT-4o: ~$30-50
- Recommendation: Use GPT-4o-mini for bulk, GPT-4o for calibration subset

## Open Questions
- Can we get agent creation dates? (not in post data, no profile API)
- Should we include comments? (available but expensive — separate API call per post)
- How to handle agents that only post in m/consciousness? (selection bias — they found the submolt)
- Rate limiting? (haven't hit any yet, but 850 calls in bulk might trigger it)
