---
description: "Build a complete product from an idea using a 6-agent pipeline (PM → Designer → Tech Designer → Engineer → Code Reviewer → QA)"
---

# /build — Full Product Build Pipeline

You will now execute a **6-agent product build pipeline** to turn the following idea into a complete, working application.

**Product idea**: $ARGUMENTS

---

## Instructions

Execute each phase below **in strict sequential order**. Each phase builds on all previous phases. Do NOT skip any phase. Do NOT proceed to the next phase until the current one is complete.

Store each phase's output as a clearly labeled section so subsequent phases can reference it.

---

## Phase 1: Product Manager

Read the agent definition in `agents/01-product-manager.md` and adopt that role fully.

Take the product idea above and produce a **complete Product Spec** following the format defined in the agent file. Be opinionated — make decisions, don't list options. Define the smallest shippable MVP.

When complete, output the Product Spec under a `## Phase 1: Product Spec` heading, then proceed.

---

## Phase 2: Designer

Read the agent definition in `agents/02-designer.md` and adopt that role fully.

Using the Product Spec from Phase 1, produce a **complete Design Spec** following the format defined in the agent file. Define every screen, every state, every interaction, and the full design system with specific values.

When complete, output the Design Spec under a `## Phase 2: Design Spec` heading, then proceed.

---

## Phase 3: Tech Designer

Read the agent definition in `agents/03-tech-designer.md` and adopt that role fully.

Using the Product Spec (Phase 1) and Design Spec (Phase 2), produce a **complete Technical Design** following the format defined in the agent file. Choose the tech stack, define the architecture, design the data model, specify the exact file structure, and create a step-by-step implementation plan.

When complete, output the Technical Design under a `## Phase 3: Technical Design` heading, then proceed.

---

## Phase 4: Engineer

Read the agent definition in `agents/04-engineer.md` and adopt that role fully.

Using ALL previous specs (Phases 1-3), **implement the complete application**. Follow the implementation plan from Phase 3 exactly. Write every file. No placeholders, no TODOs — complete, working code.

Create all files in a new directory named after the product (e.g., `workout-app/`, `finance-dashboard/`). Include all configuration files, all components, all styles, all utilities.

When complete, list all created files, then proceed.

---

## Phase 5: Code Reviewer

Read the agent definition in `agents/05-code-reviewer.md` and adopt that role fully.

Review ALL code from Phase 4 against the specs from Phases 1-3. Check every file for bugs, missing features, design mismatches, type errors, security issues, and accessibility gaps. **Fix every issue you find** by editing the code directly.

When complete, output the Code Review Summary under a `## Phase 5: Code Review` heading, then proceed.

---

## Phase 6: QA

Read the agent definition in `agents/06-qa.md` and adopt that role fully.

Test the complete application. Start the dev server. Walk through every user flow. Test happy paths and edge cases. Verify the UI matches the Design Spec. Check accessibility, responsiveness, and performance. **Fix every bug you find.**

When complete, output the QA Report under a `## Phase 6: QA Report` heading.

---

## Final Output

After all 6 phases are complete, provide a brief summary:

1. **What was built**: One paragraph describing the finished product.
2. **How to run it**: Exact commands to install dependencies and start the app.
3. **Key decisions made**: 3-5 notable product/design/technical decisions.
