# Product Build Pipeline

## Overview

This is a 6-agent sequential pipeline that takes a raw product idea and produces a fully built, tested, and shippable application. Each agent builds on the output of the previous agents.

## Pipeline

```
User Idea
    │
    ▼
┌─────────────────────┐
│  01 Product Manager  │  → Product Spec (features, user stories, acceptance criteria)
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  02 Designer         │  → Design Spec (user flows, screens, design system)
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  03 Tech Designer    │  → Technical Design (architecture, data model, file structure)
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  04 Engineer         │  → Working Code (complete implementation)
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  05 Code Reviewer    │  → Reviewed & Fixed Code
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  06 QA               │  → Tested & Ship-Ready Application
└─────────┘
```

## How to Use

Type `/build` followed by your product idea:

```
/build a workout tracking app
/build a personal finance dashboard
/build a recipe manager with meal planning
```

The pipeline will execute all 6 agents in sequence, producing a complete application.

## Agent Details

| # | Agent | Input | Output |
|---|-------|-------|--------|
| 01 | Product Manager | Raw idea | Product Spec |
| 02 | Designer | Product Spec | Design Spec |
| 03 | Tech Designer | Product Spec + Design Spec | Technical Design |
| 04 | Engineer | All specs | Working code |
| 05 | Code Reviewer | All specs + code | Reviewed code |
| 06 | QA | All specs + code | Ship-ready app |

## Principles

1. **Each agent is opinionated.** Agents make decisions rather than deferring or listing options.
2. **Output is cumulative.** Each agent can reference all previous agents' output.
3. **No scope creep.** Each agent stays within the MVP defined by Agent 01.
4. **Fix, don't flag.** Agents 05 and 06 fix issues directly rather than just reporting them.
5. **Ship-ready output.** The final result must be a working application that runs out of the box.
