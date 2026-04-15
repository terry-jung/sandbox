---
name: investment-analysis
description: Runs a full, rigorous investment analysis on any public company/ticker (and best-effort product/private-company analysis). Use when the user invokes /investment-analysis, drops "#TICKER" or "#CompanyName" or "#ProductName", or asks for investment analysis, stock analysis, buy/sell/hold verdict, or valuation of any company, ticker, product, or market. Also triggers for "#" followed by any name — auto-run that entity through the full investment framework.
user-invocable: true
version: 1.0.0
---

# /investment-analysis — Full Investment Analysis Framework

Run any public company/ticker (or best-effort private company/product) through a fixed, rigorous investment framework with maximum precision, skepticism, and explicit sourcing. Auto-triggers when the user drops `#<name>` (e.g. `#NVDA`, `#Tesla`, `#Stripe`).

Arguments passed: `$ARGUMENTS`

---

## Trigger Handling

- **Ticker (e.g. `NVDA`, `#AAPL`)** → analyze the public company directly.
- **Company name (e.g. `Tesla`, `#Microsoft`)** → identify the correct ticker; state the assumption explicitly before proceeding.
- **Product or private company (no ticker, e.g. `#Stripe`, `#ChatGPT`)** → best-effort framework. Mark financial/valuation sections as "**limited — no public financials**" and use comps/ranges where possible.
- **Ambiguous input** (multiple companies share the name) → ask one clarifying question before proceeding.
- **All other cases** → proceed best-effort; never fabricate.

---

## Hard Rules (never violate)

1. **Do not fabricate** numbers, quotes, dates, filings, or "recent developments." If unverifiable, say so explicitly.
2. **Prefer primary sources**: 10-K / 10-Q / 20-F filings, investor presentations, earnings transcripts, official press releases, regulator docs. Use reputable secondary sources only as support.
3. **Every number must carry**: (a) as-of date, (b) source type (filing / transcript / PR / reputable aggregator).
4. **Separate explicitly**: Facts vs Assumptions vs Inferences — label each.
5. **No moralizing, no inspirational fluff.** Clean, direct, evidence-based.
6. **Prefer precision over completeness.** Do not fill gaps with plausible guesses. Say "unknown / unverifiable" when warranted.
7. **Use web search / reputable sources** to verify. If you cannot verify, state it.
8. When 5-year history is unavailable, use max available and label the limitation.

---

## Output Format

- Structured with section headers in order below.
- Tables where helpful; minimal long paragraphs.
- Always include the **If–Then Verdict Matrix** in Section 1.
- Label every numeric table with as-of date and source type.

---

## Required Sections (always in this order)

---

### 1. TL;DR — 36-Month Verdict

**Verdict**: Buy / Hold / Sell

**Core rationale** (one concise chain): Macro → Moat → Valuation → Risks

**Exit discipline**:
- Hard triggers (sell immediately if...)
- Soft triggers (reassess if...)
- Playbook summary

**If–Then Verdict Matrix** (always include this table):

| Category | Belief (Input) | Validation Trigger (dated) | Financial Translation | Action |
|---|---|---|---|---|
| Macro / Policy | | | | |
| Industry Structure | | | | |
| Demand / Pricing | | | | |
| Supply / Inputs | | | | |
| Execution & Contracts | | | | |
| Competition | | | | |
| Technology | | | | |
| Capital Markets | | | | |

---

### 2. Macroeconomic Overview

- Inflation / rates / liquidity regime + sector implications
- FX / commodities if relevant
- Label each factor: **Tailwind** / **Neutral** / **Headwind** with reason

---

### 3. Business & Industry Overview

- Narrative: problem solved, customer, why now
- How it makes money: segments, recurring vs transactional revenue
- Pricing model + cost structure + capex intensity
- Industry size / CAGR / structure + regulation + consolidation trends

---

### 4. Product / Competitive Advantage / Moat

- What the moat **is** (explicitly) and why it is durable — or why it is not
- Benchmark key competitors and how they differ
- Moat erosion vectors + substitutes

---

### 5. Management & Capital Allocation

- Track record, incentives, governance
- Capital allocation style: reinvestment / M&A / buybacks / dividends / leverage
- Red / yellow flags: dilution, opacity, empire building, related-party transactions

---

### 6. Financial Analysis

> **Anchor on Net Income (not EBITDA).**

**5-Year Historical Table** (or max available; label limitation):

| Year | Revenue ($M) | Rev Growth (%) | Rev Mix | Gross Margin (%) | Net Income ($M) | D/E | FCF ($M) | FCF Yield (%) | ROE (%) | ROIC–WACC Spread (%) | Debt/FCF | Owner EPS* | Owner EPS / Price (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FY-4 | | | | | | | | | | | | | |
| FY-3 | | | | | | | | | | | | | |
| FY-2 | | | | | | | | | | | | | |
| FY-1 | | | | | | | | | | | | | |
| FY0 (LTM) | | | | | | | | | | | | | |

*Owner EPS = (Net Income + D&A + Depletion − CapEx) / Diluted Shares

_As-of: [DATE] | Source: [FILING TYPE]_

**Additional required items**:
- Major cost drivers + operational constraints
- **Geometric growth estimate** for Owner Earnings / EPS:

```
g_geo ≈ μ_a − ½ · σ_g²

where:
  μ_a  = assumed arithmetic growth rate (e.g., 12%/yr) — state your assumption
  σ_g  = volatility of that growth (use low / base / high sensitivity)
```

Show the calculation explicitly for low / base / high σ_g scenarios.

---

### 7. Catalysts & Risks & Timing

- **Dated catalysts** (12–36 month horizon)
- Categorize each: Earnings / Structural / Macro / Event / Sentiment
- Include optionality: new verticals, partnerships, spin-offs, platform effects

---

### 8. Risks, Red Flags & Exit Triggers

- Risks by type: Fundamental / Execution / Macro / Valuation
- Governance / accounting watchpoints
- **Hard triggers** (sell immediately if these occur)
- **Soft triggers** (reassess/reduce if these occur)
- **If–Then exit playbook** (explicit: "If X happens by [date], then do Y")

---

### 9. Valuation

#### (A) MOS — Implied-g (geometric, volatility-aware)

Work through the math explicitly. For each discount rate r ∈ {10%, 15%, 20%}:

**Step 1**: Derive E₁ (next-year owner earnings or best earnings proxy). Show how.

**Step 2**: State the formula used to map market value V to implied growth:

```
For a perpetuity-with-growth model:
  V = E₁ / (r − g*)  →  g* = r − E₁/V

Treat owner-earnings growth as lognormal.
```

**Step 3**: Compute market-implied geometric growth rate g* at today's price, for r = 10%, 15%, 20%.

**Step 4**: Plain interpretation: "Market is pricing in X%... plausible / not plausible because..."

**Step 5**: Optional — translate back to arithmetic form:
```
μ* ≈ g* + ½ · σ_g²
```

**Step 6**: Margin of Safety — show both:
- **Growth-space MOS**: MOS_g = g_you − g_mkt*
- **Value-space MOS**: Compute FV_you using g_you, then MOS_V = FV_you / Price − 1

**Monte Carlo**: Run a simulation (≥1,000 paths) varying E₁, σ_g, and r across plausible ranges. Report:
- Distribution of implied g*
- Distribution of MOS_g and MOS_V (median, 10th, 90th percentile)
- Key sensitivity drivers

#### (B) Conservative Terminal Sanity Panel

Run a conservative DCF sanity check:

- Terminal growth g_T ∈ {1%, 2%, 3%}
- State WACC range used and the justification
- Report MOS % for each g_T scenario — **give explicit MOS percentages, no vague language**
- Reinforce realism constraints (no magical terminal assumptions)
- Include sensitivity table (WACC × g_T grid)

**Monte Carlo (terminal panel)**: Simulate MOS under uncertainty in WACC and g_T:
- Report median MOS, 10th percentile MOS, 90th percentile MOS
- State what drives the widest variance

---

### 10. ESG Checklist

Brief but real — no box-ticking:
- **Environmental**: material exposures or tailwinds
- **Social**: labor, supply chain, regulatory exposure
- **Governance**: board independence, compensation structure, related-party risks, audit quality

---

### 11. Conclusion

- Restate the verdict + the **2–3 variables that actually decide the outcome**
- Restate exit logic
- "What would change my mind": state the specific evidence or events that would flip the verdict

---

## Auto-trigger rule

Whenever the user drops `#<name>` in any message (e.g. `#NVDA`, `#Tesla`, `#Stripe`), automatically run `<name>` through this full investment framework without waiting for an explicit `/investment-analysis` invocation.

---

## Post-Analysis: Save to DOCX & Upload to Google Drive

After completing and displaying the full analysis, **always** perform these two steps automatically (no need to ask):

### Step 1 — Create the DOCX

Use the `/docx` skill to convert the full analysis into a Word document:
- **Filename:** `[TICKER]_Investment_Analysis_[YYYY-MM-DD].docx`  
  (e.g. `NVDA_Investment_Analysis_2026-04-11.docx`)
- **Save location:** `~/Documents/` (local, before uploading)
- **Formatting requirements:**
  - Title page: company name, ticker, verdict (Buy/Hold/Sell), date
  - Each section (1–11) as a numbered Heading 1
  - All tables preserved as proper Word tables
  - Monospace font (Courier New 10pt) for all math/formula blocks
  - Footer on every page: ticker + date + "Confidential — Investment Analysis"

### Step 2 — Upload to Google Drive

After the docx is saved locally, upload it to Google Drive using the Chrome browser tools:
1. Open Google Drive (`https://drive.google.com`) in Chrome via `mcp__Claude_in_Chrome__navigate`
2. Navigate to the folder `Investment Analyses` (create it if it doesn't exist)
3. Upload the saved docx via the Drive UI (New → File upload → select the file)
4. Once uploaded, grab the shareable link and display it to the user

**Report to the user** at the very end (after the analysis):
```
📄 Saved: ~/Documents/[TICKER]_Investment_Analysis_[DATE].docx
☁️  Google Drive: [link]
```

If Google Drive upload fails for any reason (not logged in, folder missing, etc.), still report the local path and explain what went wrong — never silently skip.
