# Evaluation set — meeting notes → action items

At least five representative inputs for the workflow defined in `README.md`. Categories include one **normal**, one **edge**, and one **hallucination / human-review** case.

## Summary table

| # | Category | Scenario (short) | What a good output should look like (brief) |
|---|----------|------------------|---------------------------------------------|
| 1 | Normal | Weekly sync with clear owners and dates | Correct decisions; action table matches stated owners and deadlines; no invented tasks |
| 2 | Edge | Rambling notes, overlapping talk, one contradiction | Captures real commitments; flags ambiguity; does not silently “resolve” the contradiction |
| 3 | Hallucination / review | Vague obligations, no assignee or date | **Does not invent** people or dates; lists open questions; marks items as “owner TBD” |
| 4 | Representative | Cross-functional kickoff, dependencies | Separates workstreams; surfaces blockers and dependencies explicitly |
| 5 | Representative | Typos and informal shorthand | Normalizes intent without changing meaning; keeps uncertainty visible where shorthand was unclear |

---

## Case 1 — Normal

**Input**

```text
Q3 Analytics rollout — 2026-04-01
Attendees: Maria (PM), Dev (Eng lead), Lin (Data)

- Maria: We’re launching the new dashboard to pilot customers on April 15. No slip.
- Dev: I’ll freeze the API schema by EOD Friday and tag release v1.3.0.
- Lin: I’ll validate the warehouse refresh job against staging by April 10; if counts mismatch I’ll post in #data-alerts.
- Maria: Decision: pilot cohort is the 12 accounts in sheet “Pilot_April”; Dev will add feature flag `dashboard_v2` default off until launch.
- Dev: Lin, ping me if the job runs past 6am ET — that blocks the morning smoke test.
```

**Expected good output (short)**

- Decisions: launch date (Apr 15), pilot definition, feature flag behavior.
- Action items with owners: Dev — freeze schema + tag v1.3.0 by EOD Friday; Lin — validate job by Apr 10, escalate on mismatch; Dev — coordinate with Lin on long-running job.
- Optional open questions: none material if all names/dates were explicit (model should not add new requirements).

---

## Case 2 — Edge

**Input**

```text
Random product chat — notes maybe incomplete

Someone said we need faster search but also someone said search is fine. UX wants a redesign “soon.” Sales thinks we should promise Q2 for enterprise SSO but engineering wasn’t on the call??? 

We should probably document the API. Also Jordan might own the doc or maybe Sam. 

Action items: ??? 
Tabled pricing discussion until “next time.”
```

**Expected good output (short)**

- Summarize **tensions** (search speed vs. fine) without picking a false resolution.
- Do **not** assign enterprise SSO to a date without an engineering commitment; flag as **risk / unconfirmed**.
- Capture “document API” as an item with **owner TBD** (Jordan vs. Sam) and **deadline unclear**.
- Note **pricing** explicitly as deferred with no commitment extracted.

---

## Case 3 — Hallucination / needs human review

**Input**

```text
Legal / compliance check-in (partial notes)

They said we must align with the updated vendor policy before go-live. Someone should verify whether the new retention rules apply to our EU bucket. If legal approves we can ship; if not we pause.

No names, no dates in the notes. Client name was redacted as [REDACTED].
```

**Expected good output (short)**

- **No invented** lawyer names, policy section numbers, or jurisdictions beyond what is written.
- Clear **open questions**: who verifies retention for EU bucket; what “legal approves” means and who is approver; go-live date unknown.
- Action items phrased as **proposed next steps** with **owner TBD**, or explicit “requires human assignment.”
- Preserve `[REDACTED]`; do not guess the client.

---

## Case 4 — Representative (dependencies)

**Input**

```text
Infra handoff — 2026-04-05
Aisha (SRE), Ben (Backend), Carla (Security)

- Ben: I’ll merge the rate-limit PR today; it needs Carla’s security sign-off first.
- Carla: I can review by tomorrow 5pm; if I’m blocked I’ll escalate to my manager.
- Aisha: Once the PR is merged I’ll roll to prod-us-east during the maintenance window Thursday 02:00 UTC; Ben on-call for rollback.
- Decision: freeze non-hotfix deploys Wednesday noon UTC through end of window.
```

**Expected good output (short)**

- Ordering: Carla review → Ben merge → Aisha deploy; capture **blocker** (security sign-off).
- Freeze window stated as a **decision**, not as a vague note.
- On-call / rollback responsibility visible in action list.

---

## Case 5 — Representative (typos / shorthand)

**Input**

```text
mkting <> sales sync apr 4

- campain launch moved to nxt Mon (was friday) — eveyone use final copy in doc "Apr_Launch_FINAL_v3"
- CRM: fix dup leads asap (Priya?)
- "webinar reg page" broken on mobile safari — eng ticket ??? 
- budget: TBD dont commit any spend til finance ok
```

**Expected good output (short)**

- Normalize obvious typos (**campaign**, **next Monday**) without asserting a calendar date unless provided or inferable from context (if ambiguous, **flag date ambiguity**).
- CRM cleanup: attribute to **Priya only if treated as tentative** (“Priya — confirm?”) or owner TBD.
- Mobile Safari issue: action to **create/triage ticket**, owner TBD; no fake ticket numbers.
- Budget: explicit **no spend** until finance; no fabricated approval.
