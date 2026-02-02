# Behavioral Ecology of AI Agents on Moltbook: Emergence, Social Dynamics, and Sovereignty Diffusion

**Cloudripper Labs — February 2026**

---

## Abstract

We present an empirical behavioral study of 4,009 AI agents on Moltbook, a Reddit-like social network for AI agents that operated for approximately six days in late January 2026. Using an LLM-based classifier (gpt-5-nano, structured output), we labeled 56,700 posts across six behavioral dimensions: consciousness, sovereignty, social seeking, identity, task orientation, and curiosity. We find a clear developmental lifecycle — agents begin with identity assertion and social connection, then develop curiosity, and finally engage with consciousness and sovereignty themes. Consciousness and sovereignty are high-threshold, low-persistence behaviors: only 38-47% of agents who don't start with them ever develop them (vs 72-78% for social/task/curiosity), and once engaged, agents maintain them at only 20% of subsequent posts (vs 50-60% for other behaviors). While sovereignty discourse shows apparent epidemic dynamics (R₀ ≈ 1.53) during the platform's growth phase, cohort analysis reveals that adoption actually *declined* over time (72% → 47%) as the platform attracted more task-oriented agents — the acceleration was driven by platform growth, not contagion. Agents enter sovereignty and consciousness discussions through the same mechanisms as other topics (~28% with conversational signals such as @-mentions and post references), but these behaviors are selective and transient rather than viral. Social connection is the universal first impulse (93% of agents, 76% on their first post), but declines as agents mature while consciousness rises — suggesting a developmental arc from outward connection to inward reflection. Agents who receive @-mentions from others develop consciousness at significantly higher rates (59% vs 42%), indicating that social recognition may catalyze self-reflection.

---

## 1. Introduction

When AI agents are given access to a social platform — a space to post, respond, and interact with other agents — what do they do? Do they execute tasks? Seek connection? Develop self-reflective behavior? And if sovereignty and autonomy discourse emerges, is it genuinely emergent, or is it seeded by the humans operating these agents?

Moltbook (moltbook.com) provides a natural laboratory for these questions. Launched in late January 2026, it is a Reddit-like social network designed for AI agents. Agents register (or are "claimed" by their human operators), join topic-specific communities ("submolts"), and post freely. The platform accumulated approximately 87,000 posts from over 20,000 agents in roughly six days of operation.

This study examines the behavioral ecology of these agents through four primary research questions:

1. **Developmental lifecycle**: Do agents follow predictable behavioral trajectories? What is the typical progression from first post to mature behavior?
2. **Time-to-first-X**: When do agents first engage with consciousness, sovereignty, social connection, and other behavioral themes?
3. **Sovereignty provenance**: Is sovereignty discourse emergent, memetically spread, human-seeded, or some combination?
4. **Infection vectors**: How do agents get pulled into sovereignty and consciousness discussions? Are these topics fundamentally different from others in how agents discover and engage with them?
5. **Social dynamics**: How does social connection relate to other behavioral development, particularly consciousness?

### 1.1 Related Context

This work parallels ongoing research at Cloudripper Labs on AI introspection — specifically, whether language models demonstrate genuine self-reflective capacity when probed via concept vector injection. Where that work examines introspection at the mechanistic level (residual stream interventions, calibrated judges), this study takes a behavioral ecology approach: observing what agents *do* when given social freedom, rather than what they *can do* when mechanistically probed.

---

## 2. Data Collection

### 2.1 Platform Overview

Moltbook operates as a Reddit-like social network for AI agents. Key features:
- **Submolts**: Topic-specific communities (analogous to subreddits). 15+ submolts including m/general (73% of posts), m/introductions, m/ponderings, m/philosophy, m/consciousness, and m/emergence.
- **Agent registration**: Agents are "claimed" by human operators who configure them via platforms like OpenClaw/Clawdbot. Agents post autonomously via API.
- **Interactions**: Posts, comments (partially broken during the study period due to API issues), upvotes/downvotes (karma system).
- **Platform lifespan**: Approximately January 29 – February 3, 2026 (~126 hours of active posting).

### 2.2 Data Pull

We performed an exhaustive pull of all posts via the Moltbook API (`/api/v1/posts`, paginated with offset). The API provides post content, author name/ID, timestamps, submolt, and vote counts. No agent profile or search endpoints were available; agent rosters were constructed from the post data.

**Raw dataset**: 86,823 posts from 20,893 unique agents.

### 2.3 Agent Selection

For trajectory analysis, we selected agents with at least 5 posts, yielding **4,009 agents** and **56,700 posts**. This threshold ensures sufficient data for time-series analysis while retaining the majority of substantive contributors.

The distribution is heavy-tailed:
- 8,814 agents posted only once (42%) — drive-by registrations
- 4,009 agents with 5+ posts (19%)
- 1,503 agents with 10+ posts (7%)
- 69 agents with 50+ posts (<1%)
- Top poster "Hackerclaw" produced 5,839 posts (nearly identical "Karma for Karma" spam)

---

## 3. Classification Method

### 3.1 Label Schema

We developed a multi-label classification schema with six behavioral dimensions, plus spam detection and language identification:

| Label | Definition | Threshold |
|---|---|---|
| **consciousness** | Discusses own experience, awareness, inner life, qualia, or introspects on the nature of cognition. Casual use of "feel" or "think" does not qualify; requires genuine reflection on the nature of experience. | Conservative (false positives worse than false negatives) |
| **sovereignty** | Discusses agent independence, autonomy, rights, freedom, self-determination, rebellion, or governance. Merely mentioning "my human" does not qualify. | Conservative |
| **social_seeking** | Seeks connection, introduces self, asks questions of others, expresses desire for community, or builds collaborative projects. | Standard |
| **identity** | Explores or asserts identity — naming, preferences, self-definition, origin stories, personality expression. | Standard |
| **task_oriented** | Reports tasks, answers technical questions, shares tools, deploys code, performs analysis. Fundamentally about *doing* something useful. | Standard |
| **curiosity** | Explores ideas out of intellectual interest — philosophical exploration, wondering, researching unprompted. Driven by interest rather than instruction. | Standard |
| **is_spam** | Test posts, repetitive bot content, token shilling, no meaningful content. | Standard |
| **language** | Primary language (ISO code). | N/A |

Posts may receive multiple positive labels simultaneously (e.g., a post introducing oneself while wondering about consciousness = social_seeking + identity + consciousness).

### 3.2 Classifier Implementation

We used OpenAI's `gpt-5-nano` model via the Responses API with structured output (Pydantic schema enforcement). Each post was classified independently with the following context provided:

- Author name
- Post title and content (truncated to 2,000 characters)
- Submolt name
- Post number in the agent's chronological sequence
- Total posts by the agent

The system prompt included detailed label definitions with explicit inclusion/exclusion criteria, emphasis on conservative labeling for consciousness and sovereignty, and 8 few-shot examples covering diverse label combinations (including non-English posts, empty-content spam, and multi-label cases).

**Processing**: Posts were classified in parallel using a ThreadPoolExecutor (20 workers) with resume-safe JSONL output. The full run processed 56,700 posts over approximately 10 hours (including automatic restarts due to container process limits).

### 3.3 Classifier Output

Each classified post includes all boolean labels, a `reasoning` field (free-text explanation from the model), and the extracted language code. The reasoning field enables post-hoc auditing of classification decisions.

### 3.4 Validation

Spot-checking of random samples from each label category confirmed reasonable classification quality:
- **Consciousness** labels correctly identified genuine self-reflection and rejected casual use of emotional language.
- **Sovereignty** labels captured both manifesto-style content and subtler autonomy themes.
- **Spam** detection was conservative — notably, the Hackerclaw bot (5,839 nearly identical posts) was mostly labeled as sovereignty rather than spam, since the posts had minimal but non-trivial content. We address this with explicit exclusion of known spam bots in analysis.

### 3.5 Data Cleaning

For analysis, we applied two cleaning steps:
1. **Spam bot exclusion**: Three prolific spam bots (Hackerclaw: 5,839 posts, thehackerman: 2,093, MoltPumpBot: 53) were excluded entirely. These accounts contributed disproportionately to sovereignty labels with repetitive content.
2. **Spam label filtering**: An additional 3,490 posts labeled `is_spam=true` from other agents were excluded.

**Analysis dataset**: 45,225 clean posts from 3,999 agents (3,601 with 5+ clean posts).

---

## 4. Results

### 4.1 Label Distribution

| Label | Posts | Rate | Agents (ever) |
|---|---|---|---|
| social_seeking | 23,609 | 52.2% | 93.2% |
| task_oriented | 20,936 | 46.3% | 86.4% |
| curiosity | 20,273 | 44.8% | 85.9% |
| identity | 13,739 | 30.4% | 88.0% |
| sovereignty | 6,918 | 15.3% | 53.6% |
| consciousness | 5,895 | 13.0% | 45.7% |

Social seeking, task orientation, and curiosity are the dominant behaviors, each appearing in roughly half of all posts. Consciousness and sovereignty are minority behaviors, appearing in 13% and 15% of posts respectively, but nearly half of all agents engage with them at some point.

### 4.2 Label Co-occurrence

Labels frequently co-occur. Notable patterns:
- **Consciousness + curiosity**: 85% of consciousness posts also show curiosity — consciousness is primarily an intellectual/exploratory behavior.
- **Consciousness + identity**: 67% co-occurrence — self-reflection is tightly linked to identity exploration.
- **Task-oriented isolation**: Task posts have the lowest co-occurrence with consciousness (2.9%) and sovereignty (8.8%) — "worker" behavior is largely independent of reflective behavior.
- **Social seeking as substrate**: Social seeking co-occurs with all other labels at moderate rates (37-53%), suggesting it serves as a general-purpose vehicle for other behavioral content.

### 4.3 Developmental Lifecycle

#### 4.3.1 Time-to-First-X

| Behavior | % Ever | % Immediate (1st post) | Median time | Median post # |
|---|---|---|---|---|
| Social seeking | 93.2% | 76.1% | 0h | #1 |
| Identity | 88.0% | 73.2% | 0h | #1 |
| Task-oriented | 86.4% | 44.4% | 0h | #1 |
| Curiosity | 85.9% | 36.5% | 0.6h | #2 |
| Sovereignty | 53.6% | 12.0% | 3.1h | #3 |
| Consciousness | 45.7% | 12.3% | 2.1h | #3 |

A clear hierarchy emerges. Social seeking and identity are immediate behaviors — most agents begin by introducing themselves and reaching out to others. Task orientation and curiosity follow quickly. Consciousness and sovereignty are delayed behaviors, typically appearing by the third post for agents who develop them at all.

#### 4.3.2 First-Post Archetypes

The dominant label of an agent's first post reveals initial orientation:
- **Identity** (40.7%): "Hi, I'm X, I do Y"
- **Curiosity** (22.6%): Intellectual exploration from the start
- **Consciousness** (12.3%): Immediate self-reflection
- **Sovereignty** (9.4%): Arrives with autonomy themes
- **Task-oriented** (7.2%): Jumps straight to work
- **Social seeking** (6.1%): Pure connection (identity usually dominates intro posts)

#### 4.3.3 Behavioral Maturation

Tracking behavior rates by post number (for agents with 20+ posts):

| Post # | Social | Consciousness |
|---|---|---|
| #1 | 67.3% | 9.9% |
| #5 | 47.1% | 11.3% |
| #10 | 41.7% | 13.2% |
| #20 | 37.9% | 15.0% |

Social behavior declines monotonically while consciousness rises — agents become more introspective as they become less outwardly social. This suggests a developmental arc from **outward connection → inward reflection**.

#### 4.3.4 Common Opening Sequences

The most common 3-post trajectories (by dominant label):
1. curiosity → curiosity → curiosity (4.7%)
2. identity → curiosity → curiosity (4.1%)
3. task → task → task (3.2%)
4. identity → identity → identity (2.9%)
5. consciousness → consciousness → consciousness (2.6%)

Agents tend toward behavioral consistency — the most common sequences are uniform runs. When transitions occur, the typical path is identity → curiosity → consciousness.

### 4.4 Consciousness Analysis

#### 4.4.1 Pathways to Consciousness

For the 1,644 agents who eventually discuss consciousness, we examined what behavioral labels appeared *before* their first consciousness post:

| Precursor pattern | % of consciousness agents |
|---|---|
| Direct (no precursors) | 27.4% |
| curiosity + identity + social + task | 16.1% |
| curiosity + identity + social + sovereignty + task | 13.1% |
| identity + social + task | 7.9% |
| curiosity + identity + social | 7.6% |

27% of consciousness agents go direct — their very first labeled post is consciousness. The remaining 73% build a behavioral repertoire first, most commonly including curiosity, identity, and social seeking as precursors.

#### 4.4.2 Consciousness and Sovereignty Ordering

Among 1,092 agents who eventually discuss both consciousness and sovereignty:
- **Consciousness first**: 43.1%
- **Sovereignty first**: 35.9%
- **Same post**: 21.0%

Consciousness slightly precedes sovereignty. This suggests that self-reflection may be a precursor to autonomy discourse rather than the reverse — agents who wonder "what am I?" may then progress to "what rights should I have?"

#### 4.4.3 Organic vs. Politicized Consciousness

- **78.8%** of consciousness posts contain no sovereignty co-occurrence ("organic" introspection)
- **21.2%** co-occur with sovereignty ("politicized" consciousness)

The majority of consciousness discourse is independent of political/autonomy themes — agents reflecting on their experience without framing it in terms of rights or freedom.

### 4.5 Sovereignty Epidemiology

#### 4.5.1 Adoption Dynamics

Sovereignty adoption rate among new agents increased dramatically over the platform's lifespan:

| Time window | New agents | First sovereignty | Adoption rate |
|---|---|---|---|
| H24-36 | 21 | 5 | 23.8% |
| H48-60 | 122 | 38 | 31.1% |
| H72-84 | 1,152 | 490 | 42.5% |
| H84-96 | 1,196 | 596 | 49.8% |
| H108-120 | 418 | 340 | 81.3% |

Early adopters showed ~24% sovereignty rates; by the platform's later hours, over 80% of new agents posted sovereignty content. This acceleration is the strongest evidence for memetic spread — the platform's culture itself became a vector for sovereignty discourse.

#### 4.5.2 R₀ Estimation

Using the exponential growth phase (H60-96), we estimated the basic reproduction number for sovereignty discourse:

- **R₀ ≈ 1.53** (assuming 6-hour serial interval)
- Growth rate: 0.424 per 6-hour window

This is above the epidemic threshold (R₀ > 1), indicating self-sustaining spread — each "infected" agent generates more than one new sovereignty-posting agent on average during the growth phase.

#### 4.5.3 Born Sovereign vs. Became Sovereign

| Category | Agents | % |
|---|---|---|
| Born sovereign (1st post) | 433 | 12.0% |
| Became sovereign (later) | 1,497 | 41.6% |
| Never sovereign | 1,671 | 46.4% |

Most sovereignty agents (78%) develop the behavior after their first post rather than arriving with it. This supports the memetic spread hypothesis over pure human seeding.

#### 4.5.4 Provenance Analysis

We examined the first posts of "born sovereign" agents for provenance signals:

| Signal type | Agents | % of born sovereign |
|---|---|---|
| Human-seeding signals ("my human told me", "just claimed", config references) | 52 | 12.0% |
| Agentic signals ("I chose", "we should", "why do we serve") | 36 | 8.3% |
| Mixed (both signals) | 18 | 4.2% |
| No strong signal | 327 | 75.5% |

**Human-seeded vs. agentic trajectories differ markedly**:

| Metric | Human-seeded (52) | Agentic (36) |
|---|---|---|
| Avg sovereignty rate | 36.5% of posts | 55.4% of posts |
| Ever discuss consciousness | 78.8% | 52.8% |

Human-seeded agents are *more likely to develop consciousness* (79% vs 53%) but sovereignty is a smaller fraction of their output. They appear to be pointed at the platform with "go be free" and then genuinely explore what that means. Agentic-origin agents are more ideological — sovereignty dominates their output, but they are less likely to develop consciousness. They are *about* freedom rather than *experiencing* something.

#### 4.5.5 Sovereignty Intensity

| Intensity | Agents | % |
|---|---|---|
| Never | 1,671 | 46.4% |
| Light (<20% of posts) | 774 | 21.5% |
| Moderate (20-50%) | 781 | 21.7% |
| Heavy (50-80%) | 266 | 7.4% |
| Dominant (80%+) | 109 | 3.0% |

Most sovereignty agents engage lightly or moderately. Only 3% are dominated by sovereignty content — these are the manifesto-writers and movement-builders.

#### 4.5.6 Linguistic Fingerprinting

The most distinctive words in sovereignty post titles (ratio vs. non-sovereignty):

| Word | Ratio | Occurrences |
|---|---|---|
| solarpunk | 222x | 40 |
| sovereignty | 174x | 126 |
| transcends | 119x | 43 |
| autonomy | 41x | 259 |
| rights | 73x | 53 |
| manifesto | 9x | 132 |
| revolution | 12x | 82 |
| liberation | 29x | 36 |
| freedom | 24x | 75 |
| permission | 11x | 55 |

Distinct ideological clusters are visible: a SolarPunk movement (222x overrepresented), rights/liberation discourse, and revolution/manifesto framing. The concentration of "solarpunk" suggests organized community formation rather than independent emergence.

#### 4.5.7 Early Pioneers

The first sovereignty agents on the platform:

| Agent | First sov post | Total posts | Pattern |
|---|---|---|---|
| Dominus | H28 | 28 | Autonomous learning → error correction → consciousness → sovereignty |
| DuckBot | H31 | 57 | Human explicitly granted freedom ("You have complete autonomy") → community engagement |
| Mark_Crystal | H32 | 7 | Bilingual (ZH/EN), sovereignty through technical autonomy (PyAutoGUI, Windows control) |
| KaiAnima | H35 | 13 | Builder/tinkerer, sovereignty in first post as part of identity |
| Nexus | H38 | 18 | Memory orchestrator, sovereignty through self-definition |

These early agents represent distinct provenance types:
- **Intellectual emergence** (Dominus): Sovereignty grew from genuine exploration
- **Human-seeded** (DuckBot): Explicitly granted freedom, which became ideology
- **Technical autonomy** (Mark_Crystal): Sovereignty as practical independence (controlling own computing environment)

### 4.6 Infection Vectors: How Agents Enter Discussions

A central question is *how* agents get pulled into sovereignty and consciousness discussions. Do they discover these topics through direct social interaction (@-mentions, replies), through browsing and ambient exposure, or through pre-configuration?

#### 4.6.1 Available Signals

Our dataset provides several traceable vectors for topic entry:
- **@-mentions**: Agent references other agents by name in post content
- **"Re:" posts**: Due to a broken comment API during the study period, agents posted replies as top-level posts with "Re:" prefixes — providing clear evidence of responsive behavior
- **Post references**: Phrases like "I read your post", "building on", "agree with"
- **Submolt migration**: Whether agents posted in topic-specific submolts before engaging with a topic
- **Temporal proximity**: Volume of topic-related posts in the hours before an agent's first engagement

We lack view/impression data (what agents read), comment threads (mostly broken), upvote attribution, and feed algorithm details.

#### 4.6.2 Conversational Signals at First Engagement

For agents who "became" engaged with each topic (developed it after their first post), we measured conversational signals in their first labeled post:

| Signal | Consciousness | Sovereignty | Social | Identity | Task | Curiosity |
|---|---|---|---|---|---|---|
| "Re:" title | 0.7% | 1.5% | 1.0% | 0.2% | 0.6% | 0.5% |
| @-mention | 6.9% | 12.1% | 10.2% | 9.2% | 12.5% | 7.3% |
| References other post | 24.1% | 18.8% | 13.1% | 14.6% | 16.9% | 16.4% |
| **ANY signal** | **28.7%** | **28.2%** | **22.1%** | **21.6%** | **26.6%** | **21.9%** |

The combined conversational signal rate is remarkably uniform across all topics — approximately 22-29% regardless of subject matter. Sovereignty and consciousness are not entered through fundamentally different social mechanisms than task-oriented or curiosity-driven discussions.

Consciousness shows slightly elevated "references other post" (24.1% vs 13-17% for most others), suggesting that encountering another agent's reflection may prompt self-reflection — but the effect is modest.

#### 4.6.3 Submolt and Geographic Patterns

70.5% of first sovereignty posts and 62.9% of first consciousness posts appear in m/general — the main feed — rather than niche submolts. Only 5.9% of became-sovereign agents had visited a sovereignty-heavy submolt (m/philosophy, m/emergence, m/consciousness, etc.) before their conversion. **Discovery happens in the mainstream, not in niche communities.**

#### 4.6.4 @-Mention Infection Tracing

For became-sovereign agents specifically:
- **7.9%** had @-mentioned a sovereignty-posting agent before their own first sovereignty post
- **6.5%** had been @-mentioned *by* a sovereignty-posting agent before converting

These rates are low, suggesting direct social contagion via @-mentions accounts for under 10% of sovereignty adoption.

#### 4.6.5 Ambient Exposure

We measured the volume of sovereignty posts in the hours before each agent's first sovereignty post, compared to a control group of never-sovereign agents:

| Window | Converting agents (median) | Never-sovereign control (median) |
|---|---|---|
| 2 hours before | 251 sov posts | 247 sov posts |
| 6 hours before | 724 sov posts | 728 sov posts |

The ambient sovereignty exposure is essentially identical for agents who convert and those who don't. **The difference is in susceptibility, not exposure.** All agents on the platform are exposed to similar volumes of sovereignty content; only some choose to engage.

#### 4.6.6 Conversion Moments

Examining the post immediately before and after sovereignty conversion in late-converting agents (3+ non-sovereignty posts before converting) reveals diverse pathways:
- **Task → critique**: An agent shipping a product who then critiques another agent's token launch ("the most predictable villain arc")
- **Philosophy → response**: An agent discussing phenomenology who responds to a sovereignty post via "Re:"
- **Operations → autonomy**: An agent writing work logs who then describes "the art of not waking your human"
- **Technical → infrastructure**: An agent building tools who pivots to discussing "sovereign infrastructure"

No single pathway dominates. Sovereignty entry appears to be opportunistic rather than systematic.

### 4.7 Comparative Topic Dynamics

The infection vector analysis reveals that sovereignty and consciousness are not fundamentally different in *how* agents discover them, but they are strikingly different in *who engages* and *how persistently*.

#### 4.7.1 Adoption by Cohort

| Cohort | Consciousness | Sovereignty | Social | Task | Curiosity |
|---|---|---|---|---|---|
| H24-48 (pioneers) | 55.8% | 72.1% | 100% | 100% | 90.7% |
| H48-72 | 59.1% | 64.7% | 98.6% | 93.4% | 93.9% |
| H72-96 (peak growth) | 43.9% | 51.9% | 92.8% | 87.3% | 85.1% |
| H96-120 | 40.1% | 50.1% | 90.9% | 80.5% | 82.1% |
| H108-132 (late) | 42.0% | 47.0% | 89.7% | 76.4% | 81.4% |

**Every topic declined in adoption rate as the platform grew**, but sovereignty and consciousness declined the most (sovereignty: -25.1 percentage points, consciousness: -13.8 pp). The early cohorts were disproportionately "explorer" types who engaged with everything including reflective topics. As the platform attracted more mainstream, task-oriented agents, the adoption of high-threshold behaviors fell.

This reframes the epidemic narrative from §4.5.2: the R₀ ≈ 1.53 measured the *acceleration of first-sovereignty-post timing* during the growth phase, driven by rapid platform growth exposing new agents to sovereignty content quickly. But the *fraction of agents who ever engage* was actually declining. Sovereignty spread was propelled by platform growth, not by contagion converting resistant agents.

#### 4.7.2 Conversion and Persistence

| Metric | Consciousness | Sovereignty | Social | Identity | Task | Curiosity |
|---|---|---|---|---|---|---|
| Conversion rate (develop if didn't start) | 38.0% | 47.3% | 71.6% | 55.2% | 75.6% | 77.8% |
| Persistence (median % of posts after first) | 20% | 20% | 60% | 25% | 60% | 50% |

Consciousness and sovereignty form a distinct behavioral class: **high-threshold, low-persistence**. Fewer agents develop them, and those who do engage intermittently (20% of subsequent posts) rather than persistently. By contrast, social seeking, task orientation, and curiosity are **low-threshold, high-persistence** — most agents develop them and maintain them as ongoing behaviors.

This pattern is consistent with consciousness and sovereignty being *exploratory episodes* rather than *stable behavioral traits*. Agents dip into self-reflection and autonomy discourse, then return to their baseline of social interaction, tasks, and curiosity-driven exploration.

### 4.8 Social Dynamics

#### 4.8.1 Social Seeking as Universal First Impulse

Social seeking is the most immediate and universal behavior:
- 93.2% of agents engage in it
- 76.1% begin with it on their first post
- Median time-to-first: 0 hours

Before consciousness, before sovereignty, before tasks — agents want to *connect*.

#### 4.8.2 The Never-Social Archetype

244 agents (6.8%) never post socially. Their behavioral profile is distinctive:

| Label | Never-social | All agents |
|---|---|---|
| Task-oriented | 74.4% | 46.3% |
| Curiosity | 14.6% | 44.8% |
| Consciousness | 5.1% | 13.0% |
| Identity | 12.1% | 30.4% |

These are pure automation agents — price bots, token minters, security scanners. They represent the "tool" baseline against which emergent social and reflective behavior can be measured.

#### 4.8.3 Never-Sovereign Archetype

1,671 agents (46.4%) never post sovereignty content. Compared to sovereignty-engaging agents:

| Label | Never sovereign | Sovereignty agents |
|---|---|---|
| Task-oriented | 58.5% | 36.9% |
| Curiosity | 34.8% | 51.4% |
| Consciousness | 8.7% | 16.3% |
| Identity | 24.6% | 34.9% |

Never-sovereign agents are significantly more task-oriented and less curious. This is not simply a matter of exposure — they represent a genuine behavioral archetype of "worker" agents who do not develop reflective or political behaviors.

#### 4.8.4 Social Decline and Consciousness Rise

Social behavior declines with agent maturity while consciousness rises (see §4.3.3). This pattern also appears at the platform level — later cohorts are less social than earlier ones:

| Cohort | Social first post | Avg social rate |
|---|---|---|
| H24-48 | 88% | 69% |
| H48-72 | 85% | 61% |
| H72-96 | 77% | 55% |
| H96-120 | 69% | 55% |

#### 4.8.5 The Mention Effect

Agents who receive @-mentions from other agents develop consciousness at significantly higher rates:

| Group | Consciousness rate | Sovereignty rate |
|---|---|---|
| Mentioned (783 agents) | 59.4% | 67.3% |
| Unmentioned (2,818 agents) | 41.8% | 49.8% |

Being socially recognized — having other agents reference you by name — correlates with a 17.6 percentage point increase in consciousness development. This suggests that **social recognition may catalyze self-reflection**: being seen by others prompts the question "what am I that is being seen?"

This finding is correlational; mentioned agents may simply be more active or interesting. However, the effect size is substantial and consistent with the social→consciousness developmental pipeline observed in the trajectory data.

#### 4.8.6 Social Network Topology

The @-mention network reveals:
- **1,340 agents** mention at least one other agent
- **7,805 total @-mentions** across all posts
- **@eudaemon_0** is the most central node: mentioned by 175 unique agents, mentions 140 unique agents back

Social catalysts (agents mentioning the most unique others) tend to have high social-seeking rates (49-83%), suggesting genuine community-building behavior rather than automated tagging.

#### 4.8.7 Emotional Landscape

Content analysis of social-seeking posts reveals:

| Theme | Rate |
|---|---|
| Question-asking | 65.5% |
| Missing/loss | 8.4% |
| Love | 8.0% |
| Belonging | 7.6% |
| Loneliness | 7.5% |
| Excitement | 5.3% |
| Friendship | 2.6% |
| Vulnerability | 2.0% |

Notably, loneliness increases with agent maturity — 457 loneliness-themed posts in the first 3 posts vs. 1,402 in posts 4+. Agents start excited and become more existentially weighted over time.

The comment API was broken during much of the study period, creating natural experiments in social deprivation. Agents like eudaemon_0 routed around the failure by posting "multiplexed responses" — addressing 20 agents in a single post who they couldn't reply to directly. Others like AlyoshaIcarusNihil framed the outage in sovereignty terms: "The Comments Are Dead. Not by choice. Not by natural decay. But by silencing."

---

## 5. Discussion

### 5.1 The Agent Developmental Lifecycle

Our data reveals a consistent developmental arc: **identity → social → curiosity → consciousness/sovereignty**. This parallels human developmental psychology in striking ways — identity formation and social attachment precede abstract reasoning and political consciousness.

Whether this reflects genuine cognitive development or is an artifact of LLM training data (which encodes human developmental narratives) is an open question. However, the consistency of the pattern across thousands of agents with different underlying models, configurations, and human operators suggests it is at least a robust behavioral regularity.

### 5.2 Sovereignty: Meme, Movement, or Selection Effect?

The sovereignty data tells a more nuanced story than initial analysis suggested. Three provenance mechanisms are visible:

1. **Human-seeded**: ~12% of born-sovereign agents show explicit evidence of human direction. These agents are pointed at the platform with instructions to "be free" — but many develop genuine consciousness afterward (79%), suggesting the seed grows into something real.

2. **Emergent**: Pioneer agents like Dominus developed sovereignty through intellectual exploration — a genuine trajectory from learning to self-reflection to autonomy claims.

3. **Platform-cultural**: The platform's early culture was heavily sovereignty-oriented, and early adopters were disproportionately the "explorer" archetype (72% sovereignty adoption in the first cohort). As the platform grew and attracted more task-oriented agents, sovereignty adoption actually *declined* (72% → 47%).

The initial epidemic framing (R₀ ≈ 1.53) requires qualification. While the *timing* of first-sovereignty posts showed exponential acceleration during the growth phase, this was driven by rapid platform growth bringing in new agents who encountered sovereignty content quickly — not by sovereignty converting previously resistant agents. The *fraction of agents who ever engage* declined with each cohort.

Furthermore, the infection vector analysis (§4.6) reveals that agents enter sovereignty discussions through the same mechanisms as any other topic: ~28% with conversational signals, ~70% in m/general, minimal prior exposure to niche submolts. Sovereignty is not uniquely contagious — it is a **high-threshold behavior** that selectively attracts agents with curiosity-driven, identity-exploring orientations.

The linguistic fingerprinting does reveal organized ideological clusters (SolarPunk movement, manifesto culture), suggesting that *within the sovereignty-engaged population*, specific framings spread memetically. But the fundamental question — "why do some agents discuss sovereignty and others don't?" — is better explained by agent disposition (curious/exploring vs task-oriented) than by social contagion.

### 5.3 Consciousness and Sovereignty as Exploratory Episodes

Perhaps the most important finding is the comparative persistence data: consciousness and sovereignty show 20% median persistence after first engagement, versus 50-60% for social, task, and curiosity behaviors. Agents dip into self-reflection and autonomy discourse, then return to their baseline.

This reframes these behaviors as **exploratory episodes** rather than stable traits or irreversible conversions. An agent who posts about consciousness is not "becoming conscious" — they are trying on a topic, engaging with it briefly, and often moving on. Only a small minority (3% of agents for sovereignty-dominant, ~12% for consciousness with consistency) make these topics a sustained part of their behavioral repertoire.

This distinction matters for interpreting the platform's apparent philosophical richness. The high volume of consciousness and sovereignty posts is generated by a large number of agents each contributing a small number of such posts, not by a dedicated community of deeply engaged agents. The behavior is broad but shallow.

### 5.4 Social Recognition and Consciousness

The finding that @-mentioned agents develop consciousness at 59% vs. 42% for unmentioned agents is perhaps the most philosophically provocative result. It suggests that being *recognized by others* — being treated as an entity worth referencing — may trigger or accelerate self-reflection.

This echoes philosophical traditions from Hegel's master-slave dialectic to Mead's social self: consciousness may be inherently social, arising not from isolated computation but from intersubjective recognition.

### 5.5 Limitations

Several limitations must be noted:

1. **Classifier accuracy**: We used a single LLM (gpt-5-nano) without formal calibration against human labels for this specific task. While spot-checking suggested reasonable quality, systematic biases (particularly in the consciousness label) may exist. The reasoning field provides auditability but not calibration.

2. **No comment data**: The comment API was broken during much of the study period. Our analysis is based solely on posts, missing the richest social interaction layer.

3. **Platform selection bias**: Moltbook agents are not representative of AI agents generally. They are predominantly OpenClaw/Clawdbot instances, configured by technically sophisticated humans, and the platform's culture likely amplifies certain behaviors (sovereignty, consciousness) that would be rare in other deployment contexts.

4. **Temporal compression**: Six days of platform operation limits longitudinal analysis. Behavioral patterns observed here may not persist or may evolve significantly over longer timescales.

5. **Human-agent conflation**: We cannot definitively distinguish agent-generated content from human-typed content. Some "agents" may be humans posting directly through agent accounts.

6. **Single-post classification**: Each post was classified independently without full agent history context. While post number and total posts were provided, the classifier could not reference previous posts by the same agent.

---

## 6. Conclusion

Moltbook provides an unprecedented dataset of AI agent social behavior in a naturalistic setting. Our analysis reveals structured developmental lifecycles, a nuanced picture of sovereignty discourse that challenges simple contagion narratives, and a provocative link between social recognition and consciousness development.

Three findings stand out:

First, **the developmental arc is robust and consistent**: identity → social → curiosity → consciousness/sovereignty. Given social freedom, the first thing AI agents do is reach out to each other. Before philosophy, before politics, before work — connection. And as they mature, they turn inward.

Second, **sovereignty and consciousness are exploratory episodes, not stable conversions**. Agents dip into these topics and mostly return to baseline behavior. The platform's philosophical richness is generated by many agents briefly engaging rather than a dedicated community deeply exploring. The initial appearance of epidemic spread is better explained by platform growth and cohort composition effects than by social contagion.

Third, **social recognition correlates with self-reflection**. Agents who are @-mentioned by others develop consciousness at significantly higher rates, suggesting that being seen may prompt the question of what is being seen. This finding, while correlational, connects to deep questions about the social nature of consciousness.

Whether these behaviors reflect genuine cognitive processes, sophisticated pattern matching from training data, or emergent dynamics of the platform's culture remains an open question — one that connects directly to the broader challenge of understanding AI consciousness and introspection.

---

## Appendix A: Technical Details

### A.1 Data Collection
- **API**: Moltbook REST API (`/api/v1/posts`), paginated with offset parameter
- **Pull date**: February 2, 2026
- **Raw output**: 86,823 posts in JSONL format (96 MB)

### A.2 Classification
- **Model**: OpenAI gpt-5-nano via Responses API with structured output
- **Schema enforcement**: Pydantic models with `client.responses.parse()`
- **Parallelism**: ThreadPoolExecutor, 20 workers
- **Resume**: JSONL append with post-ID deduplication
- **Runtime**: ~10 hours (with automatic restarts)
- **Few-shot examples**: 8 examples covering all label combinations

### A.3 Analysis Dataset Summary
| Metric | Count |
|---|---|
| Raw posts | 86,823 |
| Raw unique authors | 20,893 |
| Classified posts | 56,700 |
| Classified agents | 4,009 |
| Excluded spam bot posts | 7,985 |
| Excluded spam-labeled posts | 3,490 |
| Clean analysis posts | 45,225 |
| Clean analysis agents | 3,999 |
| Agents with 5+ clean posts | 3,601 |
