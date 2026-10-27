# Security and access

Authentication, authorization, and the controls around them. Designed behavior read from the source code; not a penetration test.

**Status legend:** *Implemented* means the code does it. *Partially* means the mechanism exists but coverage or configuration is incomplete. *Planned* means it does not exist yet. A reviewer needs all three words, not just the first.

## Authentication

| Control | Status | Detail |
| --- | --- | --- |
| Password hashing | Implemented | bcrypt, salted per password. No plaintext password is stored or logged |
| Credential verification | Implemented | Sign-in compares the submitted password against the stored hash |
| Session mechanism | Implemented | JSON Web Token issued on sign-in |
| Token transport | Implemented | `Authorization: Bearer <token>` on every protected request |
| Token lifetime | Partially | Expiry is set at issue time; no refresh-token rotation exists |
| Token revocation | Planned | A signed-out token remains valid until it expires. There is no denylist |
| Multi-factor authentication | Planned | No second factor |
| Password policy | Partially | Length and complexity rules exist at registration; strength feedback is client-side only |
| Account lockout after failed attempts | Planned | No lockout or backoff on repeated failures |

**Note for integrators:** the frontend stores the token in `localStorage`. Any script running on the origin can read it, so a cross-site scripting defect becomes an account takeover. Moving to an httpOnly cookie with CSRF protection is the recommended fix, and it is recorded as an open item rather than described as already done.

## Authorization

The platform enforces access at the route level with two middlewares: `protect` validates the token and loads the user, `authorize(...)` checks the role. Access is therefore deny-by-default for any route that declares them.

Roles: `candidate`, `hr_manager`, `admin`.

| Resource | candidate | hr_manager | admin | Evidence |
| --- | --- | --- | --- | --- |
| Register, sign in | Yes | Yes | Yes | `authRoutes`, public by design |
| Read job listings | Yes | Yes | Yes | `GET /api/jobs` unauthenticated |
| Create, edit, delete a job | No | No | Yes | `jobRoutes`, `authorize('admin')` |
| View own interviews | Yes | n/a | n/a | `GET /api/interviews/candidate`, `authorize('candidate')` |
| View managed interviews | No | Yes | Yes | `GET /api/interviews`, `authorize('hr_manager', 'admin')` |
| View one interview | Own record | Yes | Yes | `GET /api/interviews/:id`, all three roles with record scoping |
| Interview report | No | Yes | Yes | `GET /api/interviews/:id/report` |
| Change interview status, end it | No | Yes | Yes | `PUT /api/interviews/:id/status`, `POST /api/interviews/:id/end` |
| Read or write interviewer notes | No | Yes | Yes | `PUT /api/interviews/:id/notes` |
| Run an AI evaluation on an interview | No | Yes | Yes | `POST /api/interviews/:id/evaluate-question`, `evaluate-behavior` |
| Call the AI proxy | Authenticated users | Authenticated users | Authenticated users | `POST /api/ai/evaluate-answer`, `protect` only |

**Warning:** the AI proxy route requires authentication but not a role. Any signed-in candidate can call `POST /api/ai/evaluate-answer`. If answer evaluation is meant to be an interviewer-only action, that route needs `authorize('hr_manager', 'admin')`.

Two policy gaps are worth stating in a review rather than leaving for discovery: the admin permission set is not granular (an admin can do everything), and role assignment is not audited.

## The analysis service

| Control | Status | Detail |
| --- | --- | --- |
| Authentication | **Not implemented** | No endpoint checks a credential |
| Network exposure | Partially | Binds `0.0.0.0` on port 8002. Must be reachable only from the platform backend |
| CORS | Implemented | Origin allowlist, comma-separated, default localhost only |
| Input validation | Partially | Decoded image and Pydantic field types; no size limit on the request body |
| Rate limiting | Planned | `WS_FRAME_RATE_LIMIT` is read from the environment and never enforced |
| Session expiry | Planned | `SESSION_TTL_S` is read and never enforced, so session memory grows until restart |

**Recommendation:** run the service on a private network segment with no public route, and add a shared-secret header before any multi-tenant deployment.

## Transport and platform

| Control | Status | Detail |
| --- | --- | --- |
| HTTPS | Deployment | Terminated at the reverse proxy. The app does not redirect `http` to `https` |
| CORS policy | Partially | The backend reflects any `localhost`, `127.0.0.1` or `192.168.*` origin. Convenient in development, too permissive for production if left unset |
| Security headers | Planned | No CSP, HSTS, `X-Content-Type-Options` or frame-ancestors policy is set by the app |
| Secrets | Partially | Read from the environment. See the warning below |
| Dependency updates | Process | No automated update tooling in the repository |
| File upload restrictions | Implemented | Cloudinary storage accepts `pdf`, `doc`, `docx` only |

**Warning:** the platform repository contains a committed `.env` file, and the analysis repository contains one as well. Anything in a committed environment file must be treated as compromised: rotate the JWT signing secret, the database URI, the Cloudinary URL and the mail credentials, then remove the file from the working tree and from history. This is listed as the first item in the [review report](../../audit/report.md).

## Logging and monitoring

| Control | Status | Detail |
| --- | --- | --- |
| Request logging | Partially | Framework diagnostics only; no structured request log |
| PII in logs | Partially | Oversized AI-service error responses are logged through `error.message`, which can echo upstream detail. Review before shipping |
| Access audit trail | Planned | No record of who read candidate data |
| Alerting | Planned | No alerting configuration in the repository |

## What a reviewer should still ask for

1. A penetration test report, or the date of the next one
2. Evidence of secret rotation after the committed `.env` incident
3. The access-review process for admin accounts
4. The backup and restoration test record
5. Data processing agreements for each sub-processor
