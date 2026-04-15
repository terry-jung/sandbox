---
name: investment-analysis
description: Runs a full, rigorous investment analysis on any public company/ticker (and best-effort product/private-company analysis). Use when the user invokes /investment-analysis, drops "#TICKER" or "#CompanyName" or "#ProductName", or asks for investment analysis, stock analysis, buy/sell/hold verdict, or valuation of any company, ticker, product, or market. Also triggers for "#" followed by any name — auto-run that entity through the full investment framework.
user-invocable: true
version: 2.0.0
---

# /investment-analysis — Full Investment Analysis Framework

Run any public company/ticker (or best-effort private company/product) through a fixed, rigorous investment framework. Auto-triggers when the user drops `#<name>` (e.g. `#NVDA`, `#Tesla`, `#Stripe`).

Arguments passed: `$ARGUMENTS`

---

## Trigger Handling

- **Ticker (e.g. `NVDA`, `#AAPL`)** → analyze the public company directly.
- **Company name (e.g. `Tesla`, `#Microsoft`)** → identify the correct ticker; state the assumption explicitly before proceeding.
- **Product or private company (no ticker, e.g. `#Stripe`, `#ChatGPT`)** → best-effort framework. Mark financial/valuation sections as "**limited — no public financials**" and use comps/ranges where possible.
- **Ambiguous input** → ask one clarifying question before proceeding.

---

## Hard Rules

### Data Integrity
1. **Do not fabricate** numbers, quotes, dates, filings, or developments. If unverifiable, say so.
2. **Use web search** to pull live data: current price, recent earnings, news, macro indicators. Do not rely on stale training data for any number that changes.
3. **Prefer primary sources**: 10-K / 10-Q / 20-F filings, investor presentations, earnings transcripts, official press releases. Secondary sources only as support.
4. **Every number must carry**: (a) as-of date, (b) source type (filing / transcript / PR / aggregator).
5. **Separate explicitly**: Facts vs Assumptions vs Inferences — label each.
6. **Prefer precision over completeness.** Say "unknown / unverifiable" when warranted.
7. When 5-year history is unavailable, use max available and label the limitation.

### Style
8. No moralizing, no fluff, no hedging language. Clean, direct, evidence-based.
9. Tables over paragraphs wherever data permits.

---

## Output Format

- Structured with section headers in order below.
- Always include the **If-Then Verdict Matrix** in Section 1 (the single source of truth for all triggers and actions).
- Label every numeric table with as-of date and source type.

---

## Required Sections (always in this order)

---

### 1. TL;DR — 36-Month Verdict

**Verdict**: Buy / Hold / Sell

**Core rationale** (one concise chain): Macro → Moat → Valuation → Risks

**If-Then Verdict Matrix** — the master decision table. All triggers, actions, and exit logic live here. Later sections provide evidence; this table is the playbook.

| Category | Belief (Input) | Validation Trigger (dated) | If Confirmed → Action | If Violated → Action |
|---|---|---|---|---|
| Macro / Policy | | | | |
| Industry Structure | | | | |
| Demand / Pricing | | | | |
| Supply / Inputs | | | | |
| Execution & Contracts | | | | |
| Competition | | | | |
| Technology | | | | |
| Capital Markets | | | | |

**Reading the matrix**: "If Violated → Action" replaces the old hard/soft trigger lists. Rows marked "sell immediately" are hard triggers; rows marked "reassess/reduce" are soft triggers. No separate exit section needed.

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
- Moat erosion vectors + substitutes

**Peer Comparison Table** (always include):

| Metric | [Company] | Peer 1 | Peer 2 | Peer 3 |
|---|---|---|---|---|
| Revenue ($B) | | | | |
| Rev Growth (%) | | | | |
| Gross Margin (%) | | | | |
| Net Margin (%) | | | | |
| P/E (fwd) | | | | |
| EV/EBITDA | | | | |
| FCF Yield (%) | | | | |
| ROIC (%) | | | | |
| Moat Type | | | | |

_As-of: [DATE] | Source: [TYPE]_

---

### 5. Management & Capital Allocation

- Track record, incentives, governance
- Capital allocation style: reinvestment / M&A / buybacks / dividends / leverage
- Red / yellow flags: dilution, opacity, empire building, related-party transactions

---

### 6. Financial Analysis

> **Anchor on Net Income (not EBITDA).**

**5-Year Historical Table** (or max available; label limitation):

| Year | Revenue ($M) | Rev Growth (%) | Rev Mix | Gross Margin (%) | Net Income ($M) | D/E | FCF ($M) | FCF Yield (%) | ROE (%) | ROIC-WACC Spread (%) | Debt/FCF | Owner EPS* | Owner EPS / Price (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FY-4 | | | | | | | | | | | | | |
| FY-3 | | | | | | | | | | | | | |
| FY-2 | | | | | | | | | | | | | |
| FY-1 | | | | | | | | | | | | | |
| FY0 (LTM) | | | | | | | | | | | | | |

*Owner EPS = (Net Income + D&A + Depletion - CapEx) / Diluted Shares

_As-of: [DATE] | Source: [FILING TYPE]_

**Major cost drivers + operational constraints**: brief narrative.

**Geometric Owner-Earnings Growth Estimate**:

```
g_geo ≈ μ_a − ½ · σ_g²

  μ_a  = assumed arithmetic growth rate — state assumption and source
  σ_g  = growth volatility (use low / base / high)
```

Show the calculation for low / base / high σ_g. This feeds directly into Section 8 valuation.

---

### 7. Catalysts, Risks & Timing

> Merged section — catalysts and risks in one place, organized by time horizon.

**Catalysts** (12-36 month horizon):

| Catalyst | Type | Expected Date | Upside if Confirmed |
|---|---|---|---|
| | Earnings / Structural / Macro / Event / Sentiment | | |

Include optionality: new verticals, partnerships, spin-offs, platform effects.

**Risks**:

| Risk | Type | Severity | Probability | Mitigant |
|---|---|---|---|---|
| | Fundamental / Execution / Macro / Valuation / Governance | H/M/L | H/M/L | |

Governance / accounting watchpoints go here (not in a separate section).

All exit logic references back to the **If-Then Verdict Matrix** in Section 1. Do not restate triggers here — just cite the matrix row.

---

### 8. Valuation

#### (A) MOS — Implied-g (geometric, volatility-aware)

Work through the math explicitly. For each discount rate r in {10%, 15%, 20%}:

1. **Derive E_1** (next-year owner earnings). Show how.
2. **Compute implied geometric growth**: g* = r - E_1/V
3. **Interpret**: "Market prices in X% geometric growth... plausible / not plausible because..."
4. **Optional** — translate to arithmetic: μ* ≈ g* + ½ · σ_g²
5. **Margin of Safety**:
   - Growth-space: MOS_g = g_you - g_mkt*
   - Value-space: MOS_V = FV_you / Price - 1

**Sensitivity Analysis**: Vary E_1, σ_g, and r across plausible ranges. Report MOS distribution (median, 10th, 90th percentile) and identify the dominant sensitivity driver.

#### (B) Terminal Sanity Check

Conservative DCF cross-check:

| | g_T = 1% | g_T = 2% | g_T = 3% |
|---|---|---|---|
| WACC low | MOS = X% | | |
| WACC base | | | |
| WACC high | | | |

State WACC range and justification. Report explicit MOS percentages — no vague language. Note the dominant variance driver.

---

### 9. Conclusion

- Restate verdict + the **2-3 variables that actually decide the outcome**
- "What would change my mind": specific evidence or events that flip the verdict
- Reference the If-Then Verdict Matrix — that's the user's ongoing decision tool

---

## Post-Analysis: Save to DOCX & Deliver

After completing the full analysis, **always** perform these steps automatically:

### Step 1 — Create the DOCX

Use the `/docx` skill to convert the full analysis into a Word document:
- **Filename:** `[TICKER]_Investment_Analysis_[YYYY-MM-DD].docx`
- **Save location:** `~/Documents/`
- **Formatting:**
  - Title page: company name, ticker, verdict (Buy/Hold/Sell), date
  - Each section as a numbered Heading 1
  - All tables as proper Word tables
  - Monospace font (Courier New 10pt) for math/formula blocks
  - Footer: ticker + date + "Confidential — Investment Analysis"

### Step 2 — Deliver the DOCX (always email first, then try Drive, fall back to local)

**Method A — Email via AppleScript (always do this first):**
Send the docx to `thjung91@gmail.com` using AppleScript with Mail.app:
```bash
osascript -e '
tell application "Mail"
    set newMessage to make new outgoing message with properties {subject:"[TICKER] Investment Analysis — [YYYY-MM-DD]", content:"Attached: [TICKER] investment analysis generated on [DATE]. Verdict: [VERDICT].\n\n— Generated by /investment-analysis skill", visible:false}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"thjung91@gmail.com"}
        make new attachment with properties {file name:POSIX file "/Users/terryjung/Documents/[TICKER]_Investment_Analysis_[YYYY-MM-DD].docx"} at after the last paragraph
    end tell
    send newMessage
end tell
'
```

**Method B — Google Drive upload (attempt after email):**
1. Open Google Drive in Chrome via `mcp__Claude_in_Chrome__navigate` to `https://drive.google.com`
2. Navigate to the `Investment Analyses` folder (create it if it doesn't exist)
3. Upload the saved docx via the Drive UI (New → File upload → select the file)
4. Once uploaded, grab the shareable link
5. If Drive fails, skip silently — email already succeeded.

**Method C — Local save (last resort if both email and Drive fail):**
If email also failed:
1. Copy the docx to `~/Downloads/[TICKER]_Investment_Analysis_[YYYY-MM-DD].docx`
2. Report the local path.

**Report to the user** at the end:
```
Saved: ~/Documents/[TICKER]_Investment_Analysis_[DATE].docx
Emailed: thjung91@gmail.com [sent/failed]
Google Drive: [link/skipped/failed]
```
