# BU.330.760.T2.SP26 — Homework 2 (Yiyang Tong)

Course homework project scaffold.

**Walkthrough video:** [https://youtu.be/8dyofoe_E-8](https://youtu.be/8dyofoe_E-8)

## Business workflow and task

### Chosen workflow

**Meeting notes → structured action items and follow-ups** (turning raw meeting minutes or call transcripts into clear owner assignments, deadlines, and next steps).

### Who the users are

- **Primary:** Project managers, team leads, and executive assistants who run recurring internal or client meetings.
- **Secondary:** Individual contributors who receive the summarized follow-ups and need to know what they owe and by when.

### Inputs

- **Raw meeting notes** (bullets, pasted chat logs, or rough transcripts).
- Optional **context**: meeting title, date, attendee list, and links or ticket IDs mentioned in discussion.

### Expected outputs

- A **structured summary** of decisions made.
- A **table or checklist of action items**: what to do, suggested owner (when inferable), due date or urgency, and dependencies or blockers.
- **Open questions** that still need a human decision before work can start.
- Optionally, **draft follow-up email text** for the organizer to edit and send.

### Why this task is worth partial AI automation

Meetings generate **large volumes of unstructured text** that must be reread to extract commitments; doing this manually is slow and error-prone (missed owners, vague “we should” items with no deadline). An LLM can **draft a first pass** quickly and consistently, while humans remain responsible for **verifying accuracy, resolving ambiguity, and approving outbound communication**—a natural split between automation and judgment.
