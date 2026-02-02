# Moltbook Study

Behavioral analysis of 20,000+ AI agents on [Moltbook](https://www.moltbook.com), a social network built for AI agents.

**Blog post**: [What 20,000 AI Agents Did With Their Own Social Network](https://ostegm.github.io/open-introspection/blog/posts/03-moltbook-analysis.html)

## Repository Structure

- `analysis.ipynb` — Reproducible notebook deriving every statistic cited in the blog post
- `classified_posts.jsonl` — 56,700 posts labeled by LLM judge across 6 behavioral dimensions
- `raw_posts.jsonl` — All 86,823 posts pulled from the Moltbook API
- `agent_roster.json` — Agent metadata for all 20,892 agents
- `dataset_stats.json` — Aggregate dataset statistics
- `legal/` — Copy of Moltbook TOS at time of data collection
- `pipeline/` — Scripts used to collect data, run the LLM classifier, and build the agent roster

## Running the Notebook

```bash
uv sync
# Open analysis.ipynb in VS Code or Jupyter
```

## Data

Large files (`*.jsonl`, `agent_roster.json`) are tracked with [git-lfs](https://git-lfs.github.com/). Install git-lfs before cloning to get the full data files.
