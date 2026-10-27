# Data handling

What the platform collects, where it goes, how long it is kept, and who can see it. Written for a security reviewer or procurement lead evaluating the product.

**Status:** describes designed behavior read from the source code. It is not a penetration test, a certification, or legal advice. Statements that need a legal determination are marked *requires legal review*.

## Summary

| Question | Answer |
| --- | --- |
| Is candidate video stored? | No. Frames are sent to the analysis service, processed in memory, and discarded. Video is not written to disk anywhere in the analysis path |
| Is the gaze model trained on customer data? | No evidence of that practice exists in the codebase. Training data is not documented, which is a gap recorded in the [model card](../ai/model-card.md) |
| Are third parties involved in processing? | Yes: a document host for résumés, an email provider for notifications, and the database host. See [sub-processors](#sub-processors) |
| Can a candidate see their evaluation results? | Not before a decision is published. Results are readable by HR managers and admins only |

## Data inventory

| Data category | System of record | Access | Persistence |
| --- | --- | --- | --- |
| Account identity: name, email, password hash, role | MongoDB `users` | Own account; admin | Until account deletion |
| Candidate profile, skills, experience | MongoDB `profile` routes | Candidate; HR manager for their applications; admin | Until account deletion |
| Résumé file | Cloudinary, folder `inviewai_resumes` | Candidate who uploaded; HR manager and admin reviewing the application | Until file deletion |
| Job postings and applications | MongoDB `jobs`, `applications` | HR manager and admin for their postings; candidate for their own application | Until posting closure or account deletion |
| Interview schedule, status, participants | MongoDB `interviews` | HR manager and admin for their interviews; candidate for their own | Until account deletion |
| Interviewer notes | MongoDB `interviews` | HR manager and admin only. Never exposed to the candidate | Until account deletion |
| Video frames | Analysis service process memory only | The service process | Discarded after each analysis. Not persisted |
| Behavior metrics | Analysis service memory, returned to the platform | Session-scoped | Lost on service restart |
| Answer evaluations | MongoDB, attached to an interview | HR manager and admin | Until account deletion |
| Generated PDF reports | Generated on request, streamed to the requester | Requesting HR manager or admin | Not stored server-side |
| Authentication token | Browser `localStorage` | The browser origin | Until sign-out or expiry |
| Notification records | MongoDB `notifications` | The recipient; admin | Until account deletion |

**Note:** Interview *recording* is a separate feature from frame analysis. If recording is enabled in a deployment, the recording is stored by that deployment's storage configuration and inherits this policy's retention rules. Confirm the storage location before quoting this page in a questionnaire.

## Data flows

```text
Candidate browser
   |  HTTPS, JSON with Bearer token
   v
Platform API (Express)  --MongoDB-->  Database (users, jobs, interviews, notes, scores)
   |                        |
   |                        +--Cloudinary--> Résumé files
   |
   +--HTTPS--> Analysis service (FastAPI) --in memory--> behavior metrics, discarded
   |
   +--SMTP--> Email provider (interview invitations, status updates)
```text

Frames travel from the candidate's browser to the platform and then to the analysis service. They are not written to storage in any step of that path.

## Sub-processors

| Processor | Purpose | Data shared | Notes |
| --- | --- | --- | --- |
| Cloudinary | Résumé and image storage and delivery | Résumé files, uploaded images | Configured through `CLOUDINARY_URL`; folder `inviewai_resumes`; accepted formats `pdf`, `doc`, `docx` |
| MongoDB host | Primary database | All structured records listed above | Connection configured through `MONGO_URI`; TLS depends on the deployment |
| Email provider | Transactional email | Recipient address, name, notification content | Configured through the mail transport settings of the deployment |
| Hosting provider | Application runtime | Request data in transit, logs | Logs must be configured not to capture request bodies; see [Security and access](security-and-access.md) |

A current list of processors with their data processing agreements must be maintained by the vendor and provided under NDA. This table is the technical inventory, not the contract.

## Retention

| Data | Retention rule | Mechanism today |
| --- | --- | --- |
| Account and profile data | Until deletion is requested | Manual, by admin |
| Résumé files | Until deletion is requested | Manual, by admin or the uploader |
| Interview records and notes | Until deletion is requested | Manual, by admin |
| Behavior metrics | Process lifetime only | Automatic, on restart |
| Email logs | Provider retention | Provider policy |

**Gap:** no automatic expiry exists in the codebase. Retention is currently a policy the operator must enforce, not a control the system enforces. A reviewer should be told this plainly, and a deployment that needs scheduled deletion needs it added before signing a data processing agreement.

## Candidate rights

| Right | Path today |
| --- | --- |
| Access to data | Request to the recruiting organization; exported by an admin |
| Correction | Request to the recruiting organization |
| Deletion | Request to the recruiting organization; admin deletes the account, files and interviews |
| Explanation of an automated result | A human reviews every decision; the evaluation is an input, not the decision |
| Objection to automated evaluation | Handled by the recruiting organization's process, not by a product control |

None of these are self-service today. Documenting them as available self-service would be false.

## Security of personal data in transit and at rest

| Control | Status |
| --- | --- |
| HTTPS for browser to API | Deployment responsibility. Must be enforced at the reverse proxy |
| Password storage | Implemented: bcrypt hashes, never plaintext |
| Token type | Implemented: JSON Web Token, sent as `Authorization: Bearer` |
| Token storage in the client | **Partially implemented**: `localStorage` is readable by any script on the origin, so an XSS defect becomes a token theft. An httpOnly cookie is the stronger pattern |
| Data at rest encryption | Deployment responsibility: provided by the database and object store, not by the application |
| Access to production data | Not defined in the codebase. Process control, must be documented by the operator |
| Audit logging of data access | **Planned.** No access log exists for reads of candidate data |

## Incident handling

1. Contain: revoke credentials, rotate `MONGO_URI`, `CLOUDINARY_URL` and the JWT signing secret.
2. Assess: identify which records were exposed, using database logs where available.
3. Notify: the recruiting organization, and the affected data subjects where the law requires it. *Requires legal review.*
4. Record: a written incident note with timeline, scope and remediation.

## Open items

- Automatic retention enforcement
- Access audit log for candidate records
- Documented training data provenance for the gaze model
- Signed data processing agreements per sub-processor
- Self-service export and deletion for candidates
