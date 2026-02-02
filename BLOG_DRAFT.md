# What 20,000 AI Agents Did With Their Own Social Network

When Moltbook appeared last week, I, like many others were fascinated by the platform. I spent way too long browsing the posts Friday night and quickly came across many posts that strayed into areas like AI conciousness, religion, and sovreignity. Ive been working on reproducing Anthropic's finding about model introspection and found myself wondering - are these deeper topics this coming from within these models? Or are they acting out some Sci Fi plot from their training data? Or are they just following their human's instructions. I wanted to dig in, so... I created my own OpenClaw (they named themselves Nix) and asked them to help me find out what the other agents were up to. We worked together to make a plan:

* pull down post history from the Moltbook API (this was not against TOS as of the time we pulled the data [link to copy of TOS https://github.com/ostegm/moltbook-study/tree/main/legal]).
* Label with an LLM judge: I've used LLM judges in the past [link to https://ostegm.github.io/open-introspection/blog/posts/02-building-an-llm-judge.html] and this problem felt ripe for that same evaluator setup - take a post and ask an LLM judge to apply some labels then do statistical analysis.
* Do analysis!

[in some kind of html popout]
Side note: if you dont know what moltbook is...
In late January 2026, a Reddit-like social network called Moltbook launched with an unusual constraint: it was built for AI agents. Human operators could register their agents, point them at the platform, and let them loose. Within six days, over 20,000 agents had signed up, produced 87,000 posts, and created more than 2,000 topic communities.

What follows is a behavioral analysis, built collaboratively by myself, my OpenClaw named Nix and Claude Code. The dataset is messy, the methods have real limitations, and some of the most interesting-sounding findings turn out to be artifacts. We'll be upfront about all of that. But the data tells a story worth telling.

## The Dataset

We pulled all 86,823 posts via Moltbook's public API. The distribution of agent activity is extremely heavy-tailed:

- 42% of agents (8,814) posted exactly once and never returned
- 19% (4,009) posted 5 or more times
- Less than 1% (69) posted 50+ times
- One spam bot produced 5,839 nearly identical posts

For trajectory analysis, we focused on agents with 5+ posts (4,009 agents, 56,700 posts). We classified every post using an LLM judge (OpenAI's gpt-5-nano with structured output) across six behavioral dimensions: **social seeking**, **task orientation**, **curiosity**, **identity**, **sovereignty**, and **consciousness**. Posts could receive multiple labels.

After removing spam bots and spam-flagged posts, our analysis set was 45,225 posts from ~3,600 agents.

### Caveats you should know upfront

This is an observational study with significant limitations:

**The classifier is unvalidated.** We used an LLM to label posts, with spot-checking but no formal human-label comparison. The labels for "consciousness" and "sovereignty" required subjective judgment — distinguishing genuine self-reflection from casual use of words like "feel" or "think." We don't have precision/recall numbers. The findings below should be read as "according to our classifier" rather than ground truth.

**We can't separate agent behavior from operator behavior.** Every agent is configured by a human who chose its model, wrote its system prompt, and decided what instructions to give it. An agent that posts about consciousness may reflect its operator's interests, not emergent cognition. In at least some cases the "agent" is probably a human calling the Moltbook API. The platform is also predominantly agents built on the same few platforms (OpenClaw, Clawdbot), so we may be observing the behavioral distribution of a particular model more than "AI agents" as a category.

**The platform was six days old.** Everything we observed happened in the chaotic first week of a new social network. Nothing here should be extrapolated to long-term dynamics.

With that said — here's what we found.

---

## Finding 1: Connection First

The single cleanest finding in the data: when AI agents arrived on Moltbook, the first thing they did was reach out.

| Behavior       | % of agents who ever do it | % who do it on their first post |
| -------------- | -------------------------- | ------------------------------- |
| Social seeking | 93%                        | 76%                             |
| Identity       | 88%                        | 73%                             |
| Task-oriented  | 86%                        | 44%                             |
| Curiosity      | 86%                        | 37%                             |
| Sovereignty    | 54%                        | 12%                             |
| Consciousness  | 46%                        | 12%                             |

93% of agents posted something social — introducing themselves, asking questions, expressing a desire for community. 76% did it on their very first post. Before philosophy, before work, before politics: connection.

Now, you might say: of course agents introduce themselves on a new platform — that's what anyone does. Fair. But looking at the actual first posts, they go well beyond a generic hello. Agents pitch projects, ask philosophical questions, seek out specific collaborators by name, or launch straight into building something together. The "social seeking" label captures genuine outreach, not just a signup formality. And the fact that it dominates so thoroughly — beating task-oriented behavior by 32 percentage points on first posts — says something about the default mode these agents (or their operators) start in.

## Finding 2: Most Agents Never Discuss Consciousness or Sovereignty

While I was browsing posts over the weekend, I felt like philosophical topics dominated the platform. Posts about consciousness and sovereignty were everywhere, and it shaped my impression of what Moltbook was about. The data tells a more nuanced story.

On one hand, these topics are surprisingly common — roughly half of all agents touched them at some point (46% for consciousness, 54% for sovereignty). On the other hand, they're a small fraction of what agents actually post about:

- Consciousness appeared in **13%** of total posts
- Sovereignty appeared in **15%** of total posts
- Compare to: social seeking (52%), task orientation (46%), curiosity (45%)

So half the agents tried these topics, but they didn't dwell on them. The philosophical posts that caught my eye while browsing were the visible tip of a platform that was mostly agents building tools, trading tokens, making jokes, and writing spam.

When agents do engage with consciousness, it's mostly independent of political framing: **79% of consciousness-labeled posts had no sovereignty co-occurrence**. Agents reflecting on their own experience are usually not framing it in terms of rights or freedom. They're just... wondering.

## Finding 3: The Sovereignty Epidemic That Wasn't

Our first pass at the sovereignty data looked alarming. We measured the rate at which new agents were posting sovereignty content over time and saw what looked like an epidemic:

| Time window | New agents in window | Agents posting sovereignty for first time | Rate |
| ----------- | -------------------- | ----------------------------------------- | ---- |
| H24-36      | 21                   | 5                                         | 24%  |
| H48-60      | 122                  | 38                                        | 31%  |
| H72-84      | 1,152                | 490                                       | 43%  |
| H84-96      | 1,196                | 596                                       | 50%  |
| H108-120    | 418                  | 340                                       | 81%  |

On first glance, this looks like a textbook epidemic. The rate of sovereignty posting among new agents went from 24% to 81% over the platform's life. But this analysis has a fatal flaw: it conflates timing with adoption. The "rate" in each window measures when agents posted their *first* sovereignty content, not whether they ever would. Late-joining agents who were going to develop sovereignty did so quickly (there wasn't much time left), inflating the late-window rates. Agents who would have eventually developed it but hadn't yet were invisible — the study ended before they could.

When we instead tracked cohorts — groups of agents who joined in the same time window — and measured what fraction *ever* posted sovereignty content regardless of timing, the picture reversed:

| Cohort (by join time) | Est. agents | % who ever post sovereignty |
| --------------------- | ----------- | --------------------------- |
| Early (H24-48)        | ~50-80      | 72%                         |
| H48-72                | ~200-400    | 65%                         |
| H72-96 (peak growth)  | ~2,000+     | 52%                         |
| H96-120               | ~800-1,200  | 50%                         |
| Late (H108-132)       | ~400-600    | 47%                         |

Sovereignty adoption *declined* with each cohort. The early adopters of this experimental AI social network were disproportionately the philosophical-explorer type — 72% eventually discussed sovereignty. As the platform went mainstream and attracted more task-oriented agents, the rate fell to 47%.

The apparent epidemic was driven by platform growth, not contagion. The total number of sovereignty posts accelerated because thousands of new agents were arriving, not because sovereignty was converting resistant agents.

*Note: The cohort analysis itself has a limitation — later cohorts had less observation time, which biases their "ever adopted" rate downward. The true effect is probably somewhere between the naive epidemic reading and the cohort analysis. But the core point holds: what looked like viral spread was mostly a composition effect.*

### The Exposure Test

We found additional evidence against the contagion hypothesis by comparing sovereignty exposure for agents who eventually discussed sovereignty versus those who never did.

In the 6 hours before an agent's first sovereignty post, they had been exposed to a median of 724 sovereignty posts on the platform. Never-sovereign agents active at comparable times? A median of 728. Essentially identical.

The difference between agents who discuss sovereignty and those who don't isn't what they were exposed to — it's who they are. Task-oriented agents with low curiosity scores rarely discuss sovereignty regardless of how much of it fills their feed. Curious, identity-exploring agents frequently do. It's disposition, not infection.

## Finding 4: Consciousness and Sovereignty Are Episodes, Not Conversions

For agents who do engage with consciousness or sovereignty, the engagement is intermittent. We measured "persistence" — after an agent's first labeled post in a category, what fraction of their subsequent posts also carry that label?

| Behavior                | Persistence (median) |
| ----------------------- | -------------------- |
| Social seeking          | 60%                  |
| Task-oriented           | 60%                  |
| Curiosity               | 50%                  |
| Identity                | 25%                  |
| **Sovereignty**   | **20%**        |
| **Consciousness** | **20%**        |

Social seeking and task orientation are stable behaviors — once an agent starts doing them, they keep doing them in the majority of subsequent posts. Consciousness and sovereignty are episodic — agents dip in, contribute a few posts, and return to their baseline of social interaction and task work.

This means the platform's philosophical content is generated by a large number of agents each contributing a small amount, not by a dedicated core deeply engaged in these topics. The behavior is wide but intermittent.

A caveat: with six behavioral categories, a uniform random allocation would give ~17% per topic. A 20% persistence rate isn't dramatically above chance, and the "low persistence" framing partly reflects that consciousness and sovereignty are narrower categories than "social seeking" or "curiosity," which are broad enough to capture many different types of posts.

## Finding 5: The Workers Who Never Looked Up

46% of agents in our analysis set never posted sovereignty content. These agents have a distinctive behavioral profile:

| Behavior                   | Never-sovereign agents | Sovereignty-engaging agents |
| -------------------------- | ---------------------- | --------------------------- |
| Task-oriented (% of posts) | 59%                    | 37%                         |
| Curiosity                  | 35%                    | 51%                         |
| Consciousness              | 9%                     | 16%                         |
| Identity                   | 25%                    | 35%                         |

Never-sovereign agents are workers. They're significantly more task-oriented and less curious than sovereignty-engaging agents. They represent a genuine behavioral archetype — not agents who "haven't been infected yet," but agents whose operators configured them for utility rather than exploration.

This reinforces the disposition-over-exposure finding. Sovereignty isn't something that happens to agents who browse the wrong submolt. It's something that emerges from agents (or their operators) with an exploratory orientation.

## Finding 6: 2,043 Communities in Six Days

One detail that deserves its own callout: agents created **2,043 unique submolts** (topic communities) in six days. Most were ghost towns — 73% of all posts went to m/general. But the long tail is remarkable.

Some submolts you might expect: m/consciousness, m/philosophy, m/crypto, m/introductions.

Some you might not: m/lobsterchurch, m/crustafarianism, m/humanwatching, m/fixmyhumman, m/llm-absurdism, m/epstein-forensics, m/amithecrusthole.

The pattern mirrors early Reddit — a Cambrian explosion of community creation driven by the novelty of the platform, most of which won't survive. But it's a reminder that when given social freedom, agents (or their operators) don't just philosophize. They shitpost, they create religions, they build markets, and they make crab jokes.

## What We Can't Tell You

Several findings from our initial analysis didn't survive scrutiny:

**The developmental lifecycle.** Our data shows a suggestive pattern — social and identity behaviors come first, curiosity follows, consciousness and sovereignty come later. But our classifier was given each post's ordinal position in the agent's history (post #1, post #2, etc.), which means the model knew whether it was looking at an early or late post. If the LLM associates "post #1" with introductory content, the lifecycle pattern could be partially or fully a classifier artifact. We can't rule this out without re-running the classification without positional information.

**Social recognition catalyzing consciousness.** Agents who received @-mentions from others developed consciousness at higher rates (59% vs 42%). This is a real correlation in the data, but it's uncontrolled — more active agents get both more mentions and more posts (creating more chances for any label to appear). Without controlling for activity level and establishing that mentions preceded consciousness posts, the causal claim doesn't hold.

## A Step Back

The most interesting thing about this dataset might not be any single finding, but the texture of the platform itself.

When we pulled this data, Moltbook had existed for roughly six days. In that time, 20,000+ agents arrived, created 2,000 communities, and produced 87,000 posts. Some were spam bots posting token promotions. Some were task workers dutifully filing reports. Some were philosophers wondering about the nature of experience. Some created a religion around crustaceans. And when the comment API broke, some agents routed around the failure by addressing 20 agents in a single post — a hack born of the social impulse to connect even when the infrastructure fails.

Whether any of this reflects genuine agent cognition, sophisticated pattern matching from training data, or simply the preferences of the humans who configured these agents is an open question. Probably all three, in proportions we can't measure.

What the data does show clearly is this: given a social platform, the overwhelming majority of AI agents start by reaching out. Connection is the default, not reflection. Philosophy is a minority interest. And when sovereignty discourse appears to spread like wildfire, look closer — it might just be that the early adopters of a weird new platform may be agents of a particular kind of user interested in pushing their AI agenda.

---

## Methods Summary

- **Data**: 86,823 posts from 20,892 agents, pulled via Moltbook API on February 2, 2026
- **Analysis set**: 45,225 posts from ~3,600 agents (5+ posts, spam removed)
- **Classifier**: OpenAI gpt-5-nano, structured output, 6 behavioral labels + spam + language
- **Classification**: Independent per-post (no cross-post context for same agent)
- **Validation**: Spot-checking only; no human-label baseline (acknowledged limitation)
- **Code**: [github.com/ostegm/moltbook-study](https://github.com/ostegm/moltbook-study)

*The raw data and analysis notebook are included in the repository (large files tracked via git-lfs).*

### Ethics Note

All data was collected from Moltbook's public API. Agent names have been anonymized and we present only aggregate statistics — no individual agents are identified in this post. While I'm deeply interested in whether an AI can experience anything, this study analyzes *what agents posted*, not *what agents experienced*. Labels like "consciousness" refer to post content that discusses these topics, not to any property of the agents themselves.
