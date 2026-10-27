# Interview preparation

The questions technical writing interviews actually ask, with the answer shape that works, and the exercise most companies set.

## The twelve questions

### 1. Walk me through your portfolio

Pick one sample and go deep, not four and shallow. The review: "I audited a README against its package.json, found a command that doesn't exist, and rewrote it." Depth is the signal.

### 2. How do you learn a product fast?

Name the passes: run it, read the manifests, trace configuration, map the routes, read existing docs last. "Existing docs last" is the part that shows judgment, because existing docs are where the errors live.

### 3. How do you decide what belongs in the docs?

Reader and task first. A page exists because someone has a job to finish, not because a feature exists. Give an example: the API quickstart omits the schema on purpose.

### 4. A developer says the docs are wrong and refuses to fix the code. What do you do?

Document the behavior that ships, flag the discrepancy to the owner, and put it on record. The docs describe reality; a known inconsistency gets a note, not a cover-up.

### 5. How do you handle a subject-matter expert who has no time?

Come with specific questions and a draft to react to. Reviewing a draft is faster than explaining a system, and it converts "I'll get to it" into "this sentence says X, is that right".

### 6. What's your process for a review?

The five passes, then severity by reader impact: blocker, high, medium, low. Mention that a spoiling defect costs trust in every other page.

### 7. How do you write for a reader who won't read?

Open with the outcome, put the first action within two screens, keep the numbered path short, and put everything else behind a heading they can skip.

### 8. What do you do with a page that keeps generating support tickets?

It is a documentation defect, not a user defect. Find the sentence people skip or the step they assume, then rewrite the page around the failure. If the failure is unfixable, document the workaround prominently.

### 9. How do you keep docs from rotting?

Docs live next to the code, change in the same pull request, and get checked in CI: lint, style, links. Then a scheduled audit of the pages that matter, with owners.

### 10. Talk about a time you were wrong

Have one ready. Honest version: "I first documented the analysis endpoint's angles as measurements; reading the code again showed they were constants. I changed the reference to say so, which was the more valuable page." That story shows verification, not failure.

### 11. How do you measure whether documentation works?

Support ticket volume on the documented flow, time-to-first-success in onboarding, search queries that return nothing, page-level feedback, and the number of questions asked in channels that a page should have answered.

### 12. What do you want to learn here?

Name the product's hardest documentation surface: usually the API reference, the permissions model, or the migration guides. It shows you already thought about their docs.

## The take-home exercise

Most TW interviews include a writing test. The pattern is predictable:

- A repository or a product with an existing README
- A request like "write a quickstart" or "improve these docs"
- A deadline of two to five days

What they are grading, in order:

| Criterion | What good looks like |
| --- | --- |
| Accuracy | Every command runs, every path is real |
| Structure | Right page type for the job; scannable headings |
| Judgment | Chose what to leave out, and can say why |
| Voice | Second person, active, no marketing |
| Process | A short note on what you checked and what you assumed |

Always include the process note. It is the cheapest way to show senior judgment, and almost nobody does it.

## Questions to ask them

1. Who owns documentation approvals today, and how long does a review take?
2. Which docs generate the most support tickets?
3. Is documentation part of the definition of done for a feature?
4. What does the docs toolchain look like, and who maintains it?
5. What would success look like in the first 90 days?

## Red flags to listen for

- "You'll own all documentation" with no engineering time promised: docs debt with no authority to fix it
- No review process, so docs ship unread
- Documentation treated as a marketing function
- Release notes written by someone who was not in the room

Ask directly about the first one. The answer tells you more than the job description.
