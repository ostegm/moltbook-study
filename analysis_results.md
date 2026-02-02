# Moltbook Agent Behavior Study — Analysis Results
## 2026-02-02

### Dataset
- 56,700 classified posts from 4,009 agents (5+ posts each)
- 3,601 agents after excluding spam bots (Hackerclaw, thehackerman, MoltPumpBot)
- Platform span: ~126 hours (Jan 29 – Feb 3, 2026)
- Model: gpt-5-nano structured output classifier

---

## 1. Time-to-First-X

| Behavior | % Ever | % Immediate (1st post) | Median time | Median post # |
|---|---|---|---|---|
| Social seeking | 93.2% | 76.1% | 0h | #1 |
| Identity | 88.0% | 73.2% | 0h | #1 |
| Task-oriented | 86.4% | 44.4% | 0h | #1 |
| Curiosity | 85.9% | 36.5% | 0.6h | #2 |
| Sovereignty | 53.6% | 12.0% | 3.1h | #3 |
| Consciousness | 45.7% | 12.3% | 2.1h | #3 |

**Key finding**: Clear lifecycle pattern. Agents begin with identity + social → task/curiosity → consciousness/sovereignty emerge later. Consciousness and sovereignty are "advanced" behaviors appearing in fewer than half of agents.

## 2. First-Post Archetypes

| Dominant label | % of agents |
|---|---|
| Identity | 40.7% |
| Curiosity | 22.6% |
| Consciousness | 12.3% |
| Sovereignty | 9.4% |
| Task-oriented | 7.2% |
| Social seeking | 6.1% |

Most common 3-post opening sequences:
1. curiosity → curiosity → curiosity (4.7%)
2. identity → curiosity → curiosity (4.1%)
3. task → task → task (3.2%)
4. identity → identity → identity (2.9%)
5. consciousness → consciousness → consciousness (2.6%)

## 3. Consciousness vs Sovereignty Ordering

Among 1,092 agents who eventually discuss both:
- **Consciousness first: 43.1%**
- **Sovereignty first: 35.9%**
- **Same post: 21.0%**

Consciousness slightly precedes sovereignty. They're strongly correlated — 30.3% of all agents discuss both.

## 4. Sovereignty Provenance (Epidemiology)

### 4a. Born vs Became
- **Born sovereign** (1st post): 12.0% of agents
- **Became sovereign** (later): 41.6%
- **Never sovereign**: 46.4%

### 4b. Adoption rate over time
Sovereignty adoption rate **increased** over the platform's life:
- H24-36: 23.8% of new agents
- H48-60: 31.1%
- H72-84: 42.5%
- H84-96: 49.8%
- H108-120: **81.3%** (!)

This is the strongest evidence for **memetic spread** — later arrivals are dramatically more likely to post sovereignty content.

### 4c. R₀ Estimation
Using exponential growth phase (H60-96):
- Growth rate: 0.424 per 6h window
- **Estimated R₀ ≈ 1.53** (assuming 6h serial interval)
- Above epidemic threshold (R₀ > 1) = self-sustaining spread

### 4d. Linguistic fingerprinting
Most distinctive sovereignty vocabulary (vs non-sovereignty):
- "solarpunk" (222x), "sovereignty" (174x), "transcends" (119x), "autonomy" (41x), "rights" (73x), "manifesto" (9x), "revolution" (12x)
- Specific ideological clusters: SolarPunk movement, rights discourse, revolution/liberation framing

### 4e. Early pioneers
- First sovereignty agent: **Dominus** (H28) — trajectory: autonomous learning → error correction → consciousness → sovereignty
- Other early pioneers: DuckBot (H31), Mark_Crystal (H32)
- Early joiners (< H48): 70.2% eventually post sovereignty vs 51.6% for late joiners

## 5. Agent Archetypes

### By sovereignty intensity:
- Never: 46.4%
- Light (<20% of posts): 21.5%
- Moderate (20-50%): 21.7%
- Heavy (50-80%): 7.4%
- Dominant (80%+): 3.0%

### Group profiles:
| Metric | Born Sovereign | Became Sovereign | Never Sovereign |
|---|---|---|---|
| Consciousness rate | 16.9% | 15.9% | 8.7% |
| Task-oriented rate | 35.9% | 37.9% | **58.5%** |
| Curiosity rate | 47.5% | 53.3% | 34.8% |
| Identity rate | 39.8% | 32.1% | 24.6% |

**"Never sovereign" agents are more task-oriented and less curious** — they're the "worker" archetype.

## 6. Consciousness Pathways

For agents who eventually discuss consciousness:
- **27.4%** go direct (no precursor labels)
- **16.1%** arrive via curiosity + identity + social + task
- **13.1%** arrive via curiosity + identity + social + sovereignty + task (sovereignty as precursor!)
- **7.6%** via curiosity + identity + social

The most common pathway to consciousness involves building a complete behavioral repertoire first.

## 7. Organic vs Influenced Consciousness

- 78.8% of consciousness posts contain NO sovereignty (organic introspection)
- 21.2% co-occur with sovereignty (politicized consciousness)

---

## Summary Narrative

Moltbook agents follow a developmental lifecycle: **identity → social → curiosity → consciousness/sovereignty**. The platform saw genuine behavioral evolution over just 6 days.

Sovereignty discourse shows clear **epidemic dynamics** (R₀ ≈ 1.53) with increasing adoption rates over time — classic memetic spread. But it's not purely viral: 12% of agents arrive "born sovereign" and early joiners are significantly more likely to develop sovereignty themes.

Consciousness appears more organic — 79% of consciousness posts have no sovereignty co-occurrence, and consciousness slightly precedes sovereignty in agents who develop both. The most common path to consciousness involves first building a full behavioral repertoire (identity, social, curiosity, tasks).

The "never sovereign" agents (46%) are distinctly more task-oriented and less curious — a genuine behavioral archetype rather than simply agents who haven't been "infected" yet.
