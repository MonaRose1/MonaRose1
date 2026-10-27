# InViewAI: AI-assisted interview platform

Candidates apply, interviewers schedule and run interviews, and the platform records each answer, evaluates it and produces a report. Final hiring decisions stay with people; the platform supplies structure and a record.

This README replaces the package glossary that was here. It covers what the product is, how the three services fit together, and the shortest path to a running install. Package detail now lives in [the dependency appendix](#dependency-appendix).

## Who uses it

| Role | Can do |
| --- | --- |
| Candidate | Register, build a profile, upload a résumé, browse and apply to jobs, attend interviews, see their status |
| HR manager | Post jobs, review applications, schedule interviews, run them, take notes, request evaluations, read reports |
| Admin | Everything above, plus user and platform administration |

## What it includes

- Job postings, applications and candidate profiles
- Interview scheduling with live sessions over WebSockets
- Per-question answer evaluation through a separate AI service
- Session-level behavior metrics (gaze and blink analysis) from the same service
- Interviewer notes, interview reports as PDF
- Notifications, ranking and scoring views

**Status note:** the AI evaluation endpoint currently returns a fixed payload and the HTTP frame-analysis path returns constant angles. Both are documented in the AI service's own reference, and both are placeholders waiting on a real implementation. Do not present them as working analysis.

## Architecture

Three services, two data stores, one socket layer:

```text
Browser (React, Vite)
   |  HTTPS, JWT Bearer
   v
Platform API (Express, :5000)   <--MongoDB-->  app database
   |        |
   |        +--Cloudinary: résumé files
   |
   +--HTTP--> Analysis service (FastAPI, :8002)  [in-memory sessions]
   |
   +--Socket.IO--> live interview events
```text

- **Platform API**: authentication, jobs, applications, interviews, notifications, reports. Port `5000`.
- **Analysis service**: frame and answer analysis over HTTP and WebSocket. Port `8002`, separate deployment, public repo `InViewAI_API`.
- **Frontend**: React 19 single-page app. Dev server on port `5173`, proxies `/api` and `/socket.io` to the API.

## Prerequisites

- Node.js 20 or later
- Python 3.10 or later, for the analysis service
- MongoDB 6 or later, local or hosted
- A Cloudinary account, for résumé storage
- An SMTP-capable mail account, for notifications
- Redis, only if you run more than one API instance

## Setup

Run the services in this order. Each runs in its own terminal.

### 1. Analysis service

```bash
git clone https://github.com/MonaRose1/InViewAI_API.git
cd InViewAI_API
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ONNX_MODEL_PATH=resnet18_gazevec_best.onnx
python main.py
```text

It listens on `:8002`. `GET /health` reports `"model_loaded": true` when the model artifact loaded. See that repository's reference for endpoint detail and current limitations.

### 2. Platform API

```bash
cd backend
npm install
cp .env.example .env   # then fill in the values below
npm run dev
```text

It listens on `:5000`. On startup it connects to MongoDB; a failed connection exits the process with a database error rather than retrying.

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env   # optional; defaults work with the dev proxy
npm run dev
```text

Open <http://localhost:5173>. The dev server proxies `/api` and `/socket.io` to `http://127.0.0.1:5000`, so the default `VITE_API_URL=/api` is correct for local work.

## Configuration

### Platform API (`backend/.env`)

| Variable | Required | Default | Effect |
| --- | --- | --- | --- |
| `MONGO_URI` | No | `mongodb://localhost:27017/ai-interviewer` | Database connection. Startup fails if unreachable |
| `JWT_SECRET` | **Yes** | none | Signs and verifies access tokens. No safe default; the app cannot authenticate without it |
| `PORT` | No | `5000` | API port |
| `AI_SERVICE_URL` | No | `http://localhost:8002` | Where the analysis service lives. Point this at the service host in any non-local deployment |
| `CLOUDINARY_URL` | **Yes** for uploads | none | `cloudinary://<key>:<secret>@<cloud>`. Without it, résumé and image uploads fail |
| `ENABLE_REDIS` | No | unset (off) | Set to `true` to broadcast Socket.IO events across instances |
| `REDIS_HOST` | No | `127.0.0.1` | Redis host, used only when `ENABLE_REDIS=true` |
| `REDIS_PORT` | No | `6379` | Redis port, used only when `ENABLE_REDIS=true` |
| `NODE_ENV` | No | unset | Set to `production` in deployments |

Mail settings for notifications come from the deployment's transport configuration.

### Frontend (`frontend/.env`)

| Variable | Required | Default | Effect |
| --- | --- | --- | --- |
| `VITE_API_URL` | No | `/api` | API base URL. The dev proxy makes `/api` work locally; set an absolute URL in production builds |

### Analysis service

Documented in the service repository. The variables that matter first are `PORT`, `ONNX_MODEL_PATH`, `ALLOWED_ORIGINS` and `FRAME_SAMPLING_INTERVAL_S`.

**Never commit a `.env` file.** The repository previously contained one; treat any value that was in it as compromised and rotate it.

## Testing

```bash
cd backend && npm run test    # Jest, API-level tests
cd frontend && npm run test   # Jest with Testing Library
cd frontend && npm run lint   # ESLint
```text

`tests/InViewAI_Testing_Report.md` records the last full pass, what it covered and what it did not. There is no end-to-end suite and no test for the AI output, so treat analysis behavior as untested.

## Project structure

```text
backend/
  config/        database, Cloudinary
  controllers/   request handlers
  middleware/    authentication, authorization, uploads
  models/        Mongoose schemas: Admin, HRManager, Candidate, Job, Application, Interview, Notification, Note
  routes/        one router per resource, mounted under /api/*
  services/      AI proxy, mail, PDF
  server.js      entry point, CORS, socket setup, route mounts
frontend/
  src/pages/      screens by role
  src/components/ shared UI
  src/context/    auth and session state
  src/services/   API clients
  vite.config.js  dev proxy to :5000
tests/            testing report
```text

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| API exits at startup | MongoDB unreachable | Check `MONGO_URI` and that MongoDB is running |
| `401 Not authorized, token failed` | Missing, expired or wrongly signed token | Sign in again; confirm `JWT_SECRET` matches the secret that issued the token |
| `403 Account suspended` | The account status is `suspended` | An admin must reinstate the account |
| `500 AI Evaluation Failed` | The API cannot reach the analysis service | Check `AI_SERVICE_URL` and that `:8002` is up |
| Uploads fail with no clear error | Cloudinary credentials missing or wrong | Set `CLOUDINARY_URL`; accepted formats are PDF, DOC and DOCX only |
| Frontend calls fail with 404 | Frontend started before the API, or `VITE_API_URL` points elsewhere | Start the API first; keep `VITE_API_URL=/api` for local work |
| Socket features dead in production | More than one API instance without the Redis adapter | Set `ENABLE_REDIS=true` and configure Redis |

## Deployment notes

There is no deployment script in this repository. A production setup needs:

1. A build of the frontend served by a static host, with `VITE_API_URL` set to the public API URL
2. The API behind HTTPS, with `NODE_ENV=production`
3. The analysis service on a private network, never publicly routed, since it has no authentication
4. CORS restricted to the real frontend origin. The development configuration accepts any localhost and private-network origin

## Dependency appendix

Frontend runtime: React 19, React Router 7, Axios, Socket.IO client, Tailwind CSS 4, Framer Motion, Lucide icons, Monaco editor, react-easy-crop, react-calendly, browser-image-compression, clsx, tailwind-merge.

Frontend tooling: Vite 7, ESLint 9, Jest 30 with Testing Library, Babel presets, localtunnel, concurrently.

Backend runtime: Express 5, Mongoose 9, bcryptjs, jsonwebtoken, dotenv, cors, Socket.IO, Axios, Multer with multer-storage-cloudinary, Cloudinary, Nodemailer, PDFKit, express-rate-limit, ua-parser-js, Redis with the Socket.IO Redis adapter.

Backend tooling: Nodemon, Jest 30, Supertest, cross-env.

Versions are pinned in each `package-lock.json`. This list is maintained by hand and should be regenerated when dependencies change.

## License

Not specified in this repository. Add a license before distributing or accepting contributions.
