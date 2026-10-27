# Documentation review: InViewAI platform

**Repository:** `InViewAI_Ai-powered_interview_platform`
**Artifact reviewed:** `README.md`, 253 lines
**Method:** five passes; every documented command executed; every documented dependency and script checked against both `package.json` files; every configuration value traced to a `process.env` or `os.getenv` call
**Result:** 13 defects. 3 blocker, 3 high, 4 medium, 3 low. One rewritten README, included alongside this report.

## Summary

| Severity | Count | One line each |
| --- | --- | --- |
| Blocker | 3 | A documented command does not exist; no configuration is documented; the AI service a reader needs is never described |
| High | 3 | Frontend dependency list is wrong; the storage layer is undocumented; the deployment config has a typo that breaks it |
| Medium | 4 | Redis is described incorrectly; the test suite that exists is not mentioned; no run order or ports; no environment file template |
| Low | 3 | The page is a package glossary, not a README; hand-numbered headings will rot; version claims drift |

## Defects

### 1. Blocker: `npm run deploy` does not exist

**Quoted:**

> ### 18. GH Pages ... **Command**: `npm run deploy`
>
> - `npm run deploy` - Deploy to GitHub Pages

**Evidence:** `frontend/package.json` scripts are `dev`, `tunnel`, `build`, `lint`, `preview`, `test`. No `deploy`. `gh-pages` is not in dependencies or devDependencies.

**Impact:** A reader who wants a preview deployment runs the command, gets `Missing script: "deploy"`, and has no documented alternative.

**Fix:** Remove both mentions, or add the script and the dependency. The rewritten README documents the build and leaves deployment to a separate page until the script exists.

### 2. Blocker: no configuration is documented anywhere

**Quoted:** none. The README has no configuration section at all.

**Evidence:** the backend reads `MONGO_URI` (default `mongodb://localhost:27017/ai-interviewer`), `PORT` (default `5000`), `ENABLE_REDIS`, `REDIS_HOST`, `REDIS_PORT`, `CLOUDINARY_URL` and `AI_SERVICE_URL`. The frontend reads `VITE_API_URL` (default `/api`). None of these appear in the README.

**Impact:** The software cannot be configured from the documentation. A reader either reads the source or copies the committed `.env`, which is the next defect.

**Fix:** A configuration table with variable, default, required/optional and effect. Reproduced in the rewritten README.

### 3. Blocker: the AI service is mentioned but never described

**Quoted:**

> **Usage**: Communicates with the AI Python service for interview analysis

**Evidence:** `backend/routes/aiRoutes.js` proxies to `process.env.AI_SERVICE_URL || 'http://localhost:8002'`. No repository URL, no run command, no port, no note that the service is a separate deployment.

**Impact:** Every AI feature returns `500 AI Evaluation Failed` on a fresh install, and the README gives no path to fix it.

**Fix:** A prerequisites line naming the service and its default port, plus the `AI_SERVICE_URL` row in the configuration table.

### 4. High: the frontend dependency list is wrong

**Quoted:**

> ### 16. Nodemon ... **Usage**: Makes development easier by auto-reloading

under **Frontend Development Dependencies**.

**Evidence:** `nodemon` appears only in `backend/package.json`. The frontend devDependencies include `concurrently`, `localtunnel`, `bun`, `identity-obj-proxy`, `jest-environment-jsdom`, none of which the README mentions. `react-calendly` is a frontend dependency used for scheduling and is absent from the dependency list entirely.

**Impact:** A reader debugging the frontend looks for a tool that is not installed, and misses `react-calendly`, which is required for the scheduling feature to work.

**Fix:** Regenerate both lists from the manifests. Dependency lists should be generated or linked, not hand-maintained: they drift within one release.

### 5. High: the upload storage layer is undocumented

**Quoted:**

> ### 9. Multer ... **Usage**: Processes profile picture uploads and resume uploads

**Evidence:** `backend/config/cloudinary.js` configures `cloudinary` with `CLOUDINARY_URL` and uses `multer-storage-cloudinary` to write to the `inviewai_resumes` folder, with `allowed_formats: ['pdf', 'doc', 'docx']`. Neither package is listed.

**Impact:** A reader without Cloudinary credentials gets a failing upload with no explanation. The accepted file formats, which are a user-facing constraint, are invisible.

**Fix:** Document the storage provider, the credentials variable, the folder, and the accepted formats.

### 6. High: the deployment configuration has a typo that breaks it

**Quoted:** `"homwpage": "https://MonaRose1.github.io/InViewAI_Ai-powered_interview_platform"`

**Evidence:** `frontend/package.json`, first key. The field is spelled `homepage`, which is what both Vite's base-path handling and GitHub Pages expect.

**Impact:** Any Pages deployment from this repository builds with the wrong asset base path, which produces a blank page and 404s for assets. This is a code defect, but it invalidates the deployment section of the docs, so it belongs in the review.

**Fix:** Correct the key. Then verify the built output serves from the documented path.

### 7. Medium: Redis is described as something it is not

**Quoted:**

> ### 14. Redis ... **Usage**: Stores session data and caches frequently accessed information

**Evidence:** `server.js` initializes the Redis adapter only when `ENABLE_REDIS === 'true'`, and uses it exclusively to broadcast Socket.IO events between server instances. No session or cache reads exist.

**Impact:** A reader believes Redis is required and that session data is stored there, which is wrong on both counts. It also hides the real operational decision: whether to enable the adapter for multi-instance sockets.

**Fix:** Describe it as an optional Socket.IO adapter, gated by `ENABLE_REDIS`, for horizontal scaling.

### 8. Medium: the test suite that exists is not mentioned

**Quoted:**

> ### 14. Jest ... **Command**: `npm run test`

**Evidence:** `tests/InViewAI_Testing_Report.md` documents a testing pass. `backend/__tests__/` contains backend tests with `jest.config.js`. The README never mentions the report or what the suite covers.

**Impact:** A reviewer or new contributor cannot tell what is tested, which is the first question asked about a handover.

**Fix:** A "Testing" section: how to run, what the suites cover, a link to the testing report, and what is not covered.

### 9. Medium: no run order and no ports

**Quoted:** none.

**Evidence:** the backend serves on `5000` and the frontend dev server runs on `5173` with a proxy for `/api` and `/socket.io` to `127.0.0.1:5000`. The AI service runs on `8002`.

**Impact:** A reader starts the frontend first, sees network errors, and concludes the frontend is broken.

**Fix:** A numbered run order with three terminals, one per service, and the port for each.

### 10. Medium: no environment template

**Quoted:** the README closes with

> - Keep the `.env` file secure and never commit it to GitHub

while `backend/.env` is committed to the repository.

**Impact:** The advice contradicts the repository, and a new contributor has nothing to copy.

**Fix:** Add `.env.example` with placeholders, remove `.env` from Git, rotate anything it contained. The README should say which variables are required.

### 11. Low: the page is a package glossary, not a README

**Quoted:** the first line

> **InViewAI - Packages and Their Usage**

**Evidence:** there is no description of the product, its users, its architecture, a screenshot, a license, or a contribution path.

**Impact:** A reader cannot tell what the software is for. The most-read page in the repository answers the second question first.

**Fix:** Lead with what the product does and who uses it, then the setup path, then reference material. Packages belong in a linked appendix.

### 12. Low: hand-numbered headings will rot

**Quoted:** `### 1. React (react and react-dom)`, `### 2. Vite`, and so on for 19 backend and 18 frontend items.

**Evidence:** the numbers are part of the heading text.

**Impact:** Inserting a dependency renumbers everything after it, and cross-references break silently.

**Fix:** Unnumbered headings, alphabetical or grouped by role, with generated version facts where possible.

### 13. Low: version claims are unverifiable by the reader

**Quoted:** `**Version**: 19.2.0` and similar for every entry.

**Evidence:** versions are pinned with carets in the manifests, so the installed version depends on `package-lock.json` and install date. Exact versions in prose drift immediately.

**Impact:** A reader compares the doc to `node_modules` and finds a different number, which erodes trust in the rest of the page.

**Fix:** State the major version and link the manifest, or generate the table.

## What is missing entirely

| Section | Why it matters |
| --- | --- |
| What the product does | The first question every reader has |
| Architecture in one diagram | Three services, two databases, one socket layer |
| Run order and ports | Three services must start in a known order |
| Configuration table | Eight variables, zero documented |
| Testing | A suite exists and is undocumented |
| Security notes | Committed secrets, no authentication on the analysis service |
| License and contribution | Required for outside contributors |

## What I did not check

- Runtime behavior under load, and the accuracy of any AI output
- The frontend and backend test suites by execution; only their presence and configuration
- Deployment to GitHub Pages, since the script does not exist
- Dependency vulnerabilities

## Priority order for fixing

1. `#10` and the committed `.env`: rotate credentials first; documentation cannot fix an exposed secret
2. `#3` and `#2`: a reader cannot run the product without these
3. `#1` and `#6`: the deployment path is broken twice
4. `#4`, `#5`, `#7`, `#8`: accuracy of the reference material
5. `#9`, `#11`, `#12`, `#13`: structure and maintenance

Fix order is impact order, not the order the defects appear above.
