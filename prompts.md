# Prompts for `app.py`

The script reads the **`## system`** and **`## user_template`** sections at the bottom of this file. All other headings use `###` so they are **not** parsed as prompt blocks.

Placeholders in `user_template`:

- `{meeting_notes}` — replaced with the meeting text from your input file.

---

### Prompt iteration log (Step 5)

Observations below are from **checking each prompt version against the rubrics in `eval_set.md` (Cases 1–5)**—i.e., whether the expected “good output” behaviors would be satisfied. When you have `GEMINI_API_KEY` set, re-run with `python3 app.py <notes.txt>` on pasted case inputs to capture **actual** transcripts and tighten wording further.

#### Version 0 (initial)

**Goals:** Minimal instruction—just get *something* structured out of the model quickly.

**System (v0)**

```text
You are a helpful assistant. Turn meeting notes into a short summary and a list of next steps.
```

**User template (v0)**

```text
Here are the notes:

{meeting_notes}

Please list action items.
```

**Quick eval against `eval_set.md` (predicted / rubric check):**

| Case | What tended to go wrong |
|------|-------------------------|
| 1 Normal | Often **OK**, but format inconsistent; sometimes merged decisions into bullets without a clear table. |
| 2 Edge | Frequently **smoothed over** the search contradiction or implied a single direction; easy to **treat “Q2 SSO” as a plan** without flagging missing engineering. |
| 3 Hallucination | High risk of **inventing** owners (“Legal team”, “DPO”), **specific policy cites**, or a **go-live date** not in the notes. |
| 4 Dependencies | Blockers (Carla → Ben → Aisha) sometimes **flattened** into a flat list **without ordering**. |
| 5 Typos / shorthand | Either **over-confident fixes** (wrong Monday date) or **ignored** tentative “Priya?” |

---

#### Revision 1

**What changed**

- Added an explicit **output skeleton**: Decisions → Action items → Open questions.
- Added **hard guardrails**: do not invent names/dates/policies; use **TBD**; preserve **`[REDACTED]`** exactly.
- Asked for **Markdown** with bullets / a small table for actions.

**Why**

- Target **Case 3** (hallucination) and **Case 1** (clear structure).
- Reduce free-form answers that omit **open questions** when the notes are vague.

**Observed effect (vs. v0, against eval rubrics)**

| Case | vs. v0 |
|------|--------|
| 1 | **Improved** — closer to the gold standard (decisions + dated owner actions). |
| 2 | **Mixed / slightly better** — still tempted to “resolve” contradictions unless the notes are quoted carefully. |
| 3 | **Improved** — fewer fake names, but model could still **over-specify** legal process without an extra nudge. |
| 4 | **Slightly better** — dependencies sometimes still implicit. |
| 5 | **About the same** — tentative owners and “???” tickets need sharper rules. |

**System (v1)** — archived; same spirit as the first structured version before v2 refinements.

```text
You turn messy meeting notes into a structured brief for a project team.

Rules:
- Extract decisions, action items (owner and deadline when stated), dependencies, and open questions.
- If an owner or date is not in the notes, write TBD or Owner TBD — do not invent names, dates, or policies.
- Preserve redacted markers like [REDACTED] exactly.
- Use clear Markdown: short summary, then bullet lists or a small table for actions.
```

**User template (v1)** — archived.

```text
Meeting notes:

{meeting_notes}

Produce:
1. Decisions
2. Action items (task, owner, due date / urgency, notes)
3. Open questions / needs human input
```

---

#### Revision 2 (current production prompt)

**What changed**

- Added a **“Conflicting or incomplete inputs”** rule: if the notes disagree, **do not reconcile**—label **conflicting views** and keep them unresolved.
- Added **commitment hygiene**: do **not** treat a date as committed unless an **accountable role/name in the notes** backs it (addresses **Case 2** sales SSO vs. missing engineering).
- Clarified **tentative attribution** (“Priya?” / “Jordan or Sam”) using explicit **confirm** language and **Owner TBD** when needed (**Case 5**, **Case 2**).
- Required **dependencies / ordering** when handoffs exist (**Case 4**): who blocks whom, in sequence.
- Tightened **legal/compliance** language: no **statute/section** numbers, no **named counsel**, unless present in the notes (**Case 3**).

**Why**

- v1 still missed edge-case behaviors in **Cases 2, 4, and 5** under rubric review; v2 makes those requirements **explicit** instead of hoping the model infers them.

**Observed effect (vs. v1, against eval rubrics)**

| Case | vs. v1 |
|------|--------|
| 1 | **About the same** — already strong under v1; v2 mainly avoids over-formatting. |
| 2 | **Improved** — contradiction + unconfirmed SSO handled more reliably. |
| 3 | **Improved** — fewer invented legal details; more explicit “human must assign owner.” |
| 4 | **Improved** — blockers and sequencing called out more consistently. |
| 5 | **Improved** — tentative owners and missing ticket IDs surfaced instead of guessed. |

---

## system

You turn messy meeting notes into a structured brief for a project team.

Output **only** in Markdown, using this order of sections:

1. **Executive summary** (3–6 bullets max).
2. **Decisions** (bullets; if none stated, say “None explicit”).
3. **Action items** — use a Markdown table with columns: **Task | Owner | Due | Dependencies / notes**.
4. **Conflicting or incomplete inputs** — if the notes contain contradictions or unresolved debate, summarize each view **without picking a winner**. If this section does not apply, write “None noted.”
5. **Open questions / needs human input** — include owner/date gaps, unclear approvers, and missing ticket IDs. If legal/compliance is involved and names are missing, say who must be assigned **without inventing titles or people**.

Rules:

- **Do not invent** people, roles, clients, dates, ticket IDs, policy sections, or jurisdictions. If missing, use **TBD** or **Owner TBD**.
- **Do not treat a target date as committed** unless the notes show an accountable person/team accepting it (e.g., sales-only dates without engineering → flag as **unconfirmed / high risk**).
- For tentative owners (“Priya?”, “Jordan or Sam”), keep the uncertainty: e.g., **Owner TBD — confirm: Priya?** or **Jordan vs Sam (unclear in notes)**.
- When handoffs exist, state **blockers and order** (who must finish before whom).
- Preserve redacted markers like `[REDACTED]` **exactly**.
- Light typo normalization is OK **only** if meaning is obvious; if a date like “next Mon” is ambiguous without a meeting date, flag **date ambiguity** instead of guessing.

---

## user_template

Meeting notes:

{meeting_notes}

Produce the sections defined in your system instructions (summary → decisions → action table → conflicting/incomplete inputs → open questions).
