# Homework 2 Report — Meeting Notes to Action Items (Yiyang Tong)

## 1. Business scenario

The workflow converts **raw meeting notes** (bullets, chat logs, or rough transcripts) into a **structured operational brief**: decisions, action items with owners and deadlines when stated, dependencies, and explicit open questions. Primary users are **project managers, team leads, and executive assistants** who must turn messy discussions into reliable follow-ups; recipients are **individual contributors** who need clarity on what they owe and by when.

This task is document-heavy and repetitive: humans reread long notes, miss implicit commitments, and inconsistently format handoffs. A language model is a reasonable **first-pass assistant** if outputs are treated as **drafts** subject to verification before anything is sent externally or entered into systems of record.

## 2. Model choice

The prototype calls **Google Gemini** through the **Google Gen AI SDK**, defaulting to **`gemini-2.5-flash`** (overridable via `--model` or `GEMINI_MODEL`).

**Rationale:** For this assignment, **Gemini via Google AI Studio** offers a **free API key** and a **low-friction** path to a capable general model. **Flash** variants prioritize **lower latency and cost** relative to larger tiers, which fits a high-volume internal workflow where outputs are reviewed anyway. The task is primarily **structured extraction and formatting** rather than deep multi-step reasoning; a strong general-purpose model is sufficient for prototyping, with quality gated by **prompting** and **human review**.

## 3. Baseline prompt vs. improved prompt

**Baseline (Version 0)** used a minimal instruction: be helpful, summarize notes, and “list action items” with little structure or safety language.

**Improved prompt (through Revision 2)** adds:

- A **fixed Markdown outline** (summary → decisions → action **table** → conflicting inputs → open questions).
- **Explicit guardrails** against inventing people, dates, clients, ticket IDs, or legal/policy references not present in the source text, with **TBD** instead of guesses.
- Rules for **unresolved contradictions** (do not “smooth” conflicting views).
- **Commitment hygiene** (e.g., not treating a sales-only date as engineering-approved).
- **Dependency ordering** when handoffs appear in the notes.
- Handling of **tentative owners** (“Priya?”) and **light typo normalization** without over-confident inference.

In short, the baseline optimizes for *fluency*; the revised prompt optimizes for **auditability** and **epistemic honesty**, which matters when notes are incomplete or politically sensitive.

## 4. Observed results (honest assessment)

Evaluation used the **five cases** documented in `eval_set.md`, comparing model behavior against the stated “good output” rubrics (and, when an API key is available, spot-checking full runs via `app.py`).

**Where it tends to improve**

- **Structure and scanability:** The revised prompt produces more consistent sections and tables, which makes PM handoffs faster.
- **Hallucination pressure (especially legal/vague notes):** Explicit “do not invent” rules and a dedicated **open questions** section **reduce** (but do not eliminate) fabricated names, policy citations, or implicit go-live dates.
- **Edge notes with contradictions or missing engineering:** The **conflicting inputs** and **unconfirmed commitment** language **often** improves handling versus the baseline, which tended to imply false consensus.

**Where it can still fail (human review still required)**

- **Ambiguous time phrases** (“next Monday” without a meeting anchor): models may still **guess** a calendar date unless the prompt and workflow supply **explicit meeting date context** in the input file.
- **Subtle political notes:** even with instructions, models sometimes **over-summarize** tension or **under-flag** risk; reviewers should read the **original notes** side-by-side with the draft.
- **Compliance / legal:** any output touching retention, vendors, or approvals should be treated as **non-authoritative**—suitable for **scheduling a human review**, not for filing or external promises.
- **Recall errors:** the model can still **drop** a minor action buried in noisy text; the draft is not a substitute for a careful pass on high-stakes meetings.

**Bottom line on quality:** effects are **meaningfully better than the baseline for structure and safety framing**, but the system is **not trustworthy enough** to auto-send follow-ups or auto-update a work tracker without a **human gate**.

## 5. Deployment recommendation

**Suitable to deploy only as an assistive, human-in-the-loop workflow**—not as full automation.

**Conditions that make deployment reasonable**

- Every output is **reviewed by the meeting owner** before distribution; **no auto-send** to clients or executives for sensitive topics.
- Inputs include **minimal metadata** (meeting date, attendee list) when available to reduce date/owner ambiguity.
- Teams treat the tool as **draft + checklist generator**, with a **short SOP** for when to reject the draft (legal, HR, major commitments, revenue dates).
- Logging/versioning of prompts (`prompts.md`) and periodic re-evaluation against a small **frozen eval set** (as in this project).

**If effects remain middling in production**, the honest operational stance is **stricter human review** (e.g., mandatory diff against source notes for high-risk meetings) rather than loosening guardrails to make the output “prettier.”

---

*Length: approximately 1–2 pages when rendered as standard prose (single column).*
