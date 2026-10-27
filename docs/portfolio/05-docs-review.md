# Sample 5: documentation review with fixes

**Niche:** editorial review, documentation debt
**Repository reviewed:** [InViewAI platform](https://github.com/MonaRose1/InViewAI_Ai-powered_interview_platform)
**Shipped:** [Review report](../audit/report.md) · [Rewritten README](../audit/rewritten-readme.md)

## Why this sample exists

Anyone can write a new page. The harder, more common job is walking into an existing repository and answering: what is wrong with these docs, what does it cost the reader, and what replaces it.

This review found thirteen defects in a 253-line README. Three of them stop a new developer completely. The report ranks them by reader impact, quotes the evidence, and the rewritten README fixes all thirteen.

## Step 1: Scope

> A developer who has been handed this repository and needs it running today. They have Node and Python. They have ten minutes to decide whether the docs are trustworthy. A reviewer will also read this document to judge how I work.

Deliberately not in scope: copy-editing every sentence. A review that spends its budget on commas and misses a documented command that does not exist is a failed review.

## Step 2: Evidence

Method: five passes over the repository, about an hour.

| Pass | What I did | What it caught |
| --- | --- | --- |
| 1. Follow the doc literally | Ran every command in the README in order | `npm run deploy` has no matching script |
| 2. Compare docs to manifests | Read `frontend/package.json` and `backend/package.json`, matched every documented dependency and script | Nodemon listed under frontend; Cloudinary missing from backend; `deploy` script absent |
| 3. Trace configuration | `grep` for `process.env`, `os.getenv`, `.env` files | Eight undocumented variables, one committed `.env` |
| 4. Map the runtime | Read entry points, route mounts, proxies, ports | No documented run order, no ports, no AI service setup |
| 5. Read as the target reader | Read only the README, nothing else, and tried to state what the product does | The README never says what the product is |

### The finding that mattered most

The README's fourth section is "GH Pages" with the command `npm run deploy`. In `frontend/package.json` there is no `deploy` script and no `gh-pages` dependency. The `homepage` field is spelled `homwpage`, so even a hand-rolled Pages deploy would build with the wrong base path.

Three defects, one page, one reader: they run the command, it errors, and every other page in the repository loses credibility. That is why this class of defect is a blocker and not a nit.

## Step 3: Report structure

Reviews are read by two audiences: the person who will fix it, and the person deciding whether to trust the review. The report serves both:

1. **Summary table**: severity, count, one line each
2. **Defects**: numbered, with the exact quote, the evidence, the impact, and the fix
3. **What is missing**: the sections that should exist and do not
4. **What I did not check**: honest scope boundaries

Numbering is stable so a fix can reference `#4` in a pull request.

## Step 4: Severity definitions

| Severity | Definition |
| --- | --- |
| Blocker | A reader following the docs cannot get the software running |
| High | The docs state something false about the software |
| Medium | The docs omit something a reader needs, but the reader can recover |
| Low | Structure, consistency or maintenance risk; no direct reader failure |

Every defect gets one severity, assigned by impact on the reader, not by effort to fix. A one-word typo that breaks a deployment is a blocker; a rewritten paragraph that improves flow is low.

## Step 5: Review of the review

- Re-checked each quoted line against the current `HEAD` of the repository, since the README could have changed.
- Confirmed every claimed missing script or dependency by reading the manifest, not by memory.
- Kept security findings to the level of "rotate these secrets"; no exploit detail appears in a public document.
- Read the rewritten README cold, in a fresh clone, and ran the setup steps it prescribes.

## What this sample demonstrates

The work technical writing teams actually hire for: diagnosing documentation debt in someone else's repository, ranking by reader impact, quoting evidence, and shipping the fix. The rewritten README is included so the review ends in a deliverable, not a complaint.
