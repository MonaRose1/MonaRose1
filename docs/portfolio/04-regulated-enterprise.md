# Sample 4: documentation for a regulated, enterprise-bought product

**Niche:** enterprise, security and compliance documentation
**Repository:** [InViewAI platform](https://github.com/MonaRose1/InViewAI_Ai-powered_interview_platform) (MERN, FastAPI service, Cloudinary, Firebase-adjacent auth stack)
**Shipped:** [Data handling](../samples/enterprise/data-handling.md) · [Security and access](../samples/enterprise/security-and-access.md) · [Accessibility](../samples/enterprise/accessibility.md)

## Step 1: Scope

> A security reviewer at a company evaluating this platform, and the procurement lead who has to answer their questions. They will not read a feature page. They need to know what personal data the system collects, where it goes, who inside the customer's organization can see it, how long it is kept, and what the vendor's own controls are. Answers must be specific enough to paste into a vendor questionnaire.

This is the documentation genre most technical writers are asked to write and least often taught. The reader is adversarial, in the good sense: they are paid to find the gap. Vagueness reads as concealment.

## Step 2: Evidence

Read: `server.js` (middleware order, CORS policy, route mounts, socket setup, Redis toggle), `backend/config/db.js` and `cloudinary.js`, `backend/middleware/authMiddleware.js` and siblings, all 15 route files, `backend/models/`, the FastAPI service's data flow, and both `.env` files.

The evidence produced a data map. Facts have sources; nothing is assumed:

| Data | Where it lives | Who can reach it | Evidence |
| --- | --- | --- | --- |
| Account: name, email, hashed password, role | MongoDB `users` collection | Own account; admins; HR managers for candidates they interview | `models/`, `authRoutes`, bcrypt hashing in the auth controller |
| Résumé files | Cloudinary, folder `inviewai_resumes`, formats `pdf`, `doc`, `docx` | Uploader, HR manager, admin | `config/cloudinary.js` |
| Interview schedule and status | MongoDB `interviews` | HR manager, admin, assigned candidate | `interviewRoutes` role gates |
| Interviewer notes | MongoDB, per interview | HR manager, admin only | `PUT /api/interviews/:id/notes` |
| Video frames sent for analysis | Base64 in request body, in-process memory only | The service process; nothing persisted | gaze service session state, no writes to disk in the frame path |
| Behavior metrics | In-process memory, returned to the platform | Session-scoped; lost on restart | no persistence layer in the service |
| AI answer evaluations | MongoDB, attached to the interview | HR manager, admin | `evaluate-question` route plus stored result |
| Generated reports | Generated as PDF on request | Requesting HR manager, admin | `GET /api/interviews/:id/report` |
| Auth token | Browser `localStorage`, sent as a Bearer token | The browser origin | `frontend/src/services/api.js` |

Two things the evidence changed about the documentation:

1. **Video is not stored by the analysis service.** That is a genuinely reassuring fact, and it is invisible from the product. It belongs in the first paragraph of the data-handling page.
2. **Resumes are processed by a third party.** Cloudinary is a sub-processor and must be named in the sub-processor table. The README never mentioned it at all.

## Step 3: Structure

Enterprise documentation is a set of answers, not a narrative. Structure follows the questionnaire:

```
Data handling        what is collected, where it goes, how long, who is it shared with
Security and access  authentication, authorization matrix, encryption, logging, incidents
Accessibility        conformance statement, known issues, remediation plan, testing method
```

Each page answers in a table where the reader expects a sentence, and gives a paragraph only for a decision that needs justification.

## Step 3b: What is deliberately not written

A technical writer cannot publish a security assessment of a live product, and should not pretend to. These pages:

- describe **designed behavior** from the code, not the result of a penetration test
- state **conformance status** honestly, including "partially conformant"
- mark every control as **implemented**, **partially implemented** or **planned**, because a reviewer will ask which
- never publish an exploitable detail. Findings that would help an attacker go to the engineering team through a private channel, listed in the private notes that accompany this sample

## Step 4: Draft decisions

- **Name the sub-processors.** Cloudinary, the email provider, the database host. A reviewer who finds an unnamed processor stops trusting the rest of the document.
- **Separate the role model from the access matrix.** Roles are three (`candidate`, `hr_manager`, `admin`); permissions differ per resource. One table, resource rows by role columns.
- **State retention as a decision, not a default.** Nothing in the code expires data, so the page says data is retained until deletion is requested, and flags it as a product gap rather than describing nonexistent automation.
- **Distinguish "not collected" from "not persisted".** Frames are transmitted and processed but not stored. Both halves matter to a reviewer.
- **Accessibility as a conformance statement with a date.** "Partially conformant" plus a list of known issues is credible. "Fully accessible" without an audit is not.

## Step 5: Review

- Every claim traced to a file, a route or a config value.
- Checked the access matrix against all 15 route files, one resource at a time, rather than trusting the middleware names.
- Legal-adjacent statements marked as "requires legal review" instead of being asserted. Jurisdiction claims are not a writer's call.
- Terminology aligned with the [style guide](../style-guide.md): "personal data", "data subject request", "sub-processor", used consistently.
- Read once as a hostile reviewer: every place I wanted to write "secure" was replaced with the specific control that exists.

## What this sample demonstrates

The documentation that unblocks a sale: a data map, an access matrix, a sub-processor list, an honest conformance statement, and the judgment to separate what the product does from what it should still do. Most technical writers can explain a feature. Fewer can write the page a security reviewer accepts.
