# Sample 1: API reference for a developer tool

**Niche:** developer tools, reference documentation
**Repository:** [InViewAI_API](https://github.com/MonaRose1/InViewAI_API) (Python, FastAPI, ONNX Runtime)
**Shipped:** [Quickstart](../samples/api/quickstart.md) · [Reference](../samples/api/reference.md) · [Error catalogue](../samples/api/errors.md)

## Step 1: Scope

> A backend or frontend developer who has cloned the service and needs a working request in under ten minutes. They know HTTP and Python. They do not know the session model, the sampling behavior or the thresholds. Secondary reader: the engineer integrating the service into the interview platform, who needs the exact status codes and the fields that can fail.

Two consequences, decided before drafting:

1. The quickstart is separate from the reference. A reader at install time does not want to scroll a schema table.
2. No authentication section that says "coming soon". The service has no authentication today. That is a security note, not a gap to hide.

## Step 2: Evidence

Read in full: `main.py` (entry point, all routes, session state, metric math), `requirements.txt`, `test_api.py`, `test_frame_analysis.py`, `.env`.

Facts collected from source, each with the line that proves it:

| Fact | Source | Why it matters to a reader |
| --- | --- | --- |
| Default port is `8002`, bound to `0.0.0.0` | `os.getenv("PORT", "8002")`, `uvicorn.run` | The platform's backend default expects `http://localhost:8002` |
| Five endpoints: `GET /health`, `POST /api/analyze-frame`, `POST /api/evaluate-answer`, `GET /api/session-summary/{session_id}`, `WS /ws/analyze/{session_id}` | route decorators | This is the entire surface; the README claimed none of it |
| No authentication on any endpoint | no security dependency, no header check | Must be a warning, not a footnote |
| `POST /api/analyze-frame` returns `pitch: 0.0`, `yaw: 0.0` on both branches | constants passed to `update_behavior(ear=0.3, pitch_deg=0.0, yaw_deg=0.0)` | The endpoint returns constant angles; documenting them as measured values would be a lie |
| Metrics update once every `FRAME_SAMPLING_INTERVAL_S` (default 3 s) | `if ts - last_sample_time < FRAME_SAMPLING_INTERVAL_S: return` | Sending 15 frames per second does not give 15 samples per second |
| `POST /api/evaluate-answer` returns fixed `0.5` scores and `"Mock evaluation"` | endpoint body | Integrators must not build scoring UI on it yet |
| `SESSION_TTL_S` and `WS_FRAME_RATE_LIMIT` are read from the environment and never used | `grep` | Documenting them as controls would be false; they are listed as reserved |
| Model path default `resnet18_gazevec_best1.onnx` does not match the committed `resnet18_gazevec_best.onnx` | `os.getenv("ONNX_MODEL_PATH", ...)` vs repository file list | `/health` reports `model_loaded: false` on a default install, which looks like a broken install |

## Step 3: Structure

```text
Quickstart      install, configure, run, one working request
Reference       endpoints table, schemas, responses, status codes, configuration
Errors          every failure a reader can hit, cause, fix
```text

Reference pages are scanned, not read, so the endpoint table comes first and each endpoint repeats the same six fields: method and path, purpose, request, response, status codes, notes. Consistency beats prose in reference material.

## Step 4: Draft decisions

- **Lead with `curl`, not with the class diagram.** The reader's first question is "does it work", not "how is it built".
- **Publish the constant-angle behavior.** It is the single most useful thing in the reference: an integrator who reads it stops debugging their own camera pipeline.
- **Configuration table with defaults.** Every `os.getenv` call became a row. Four of them are marked *reserved* because the code reads them and never acts on them.
- **No invented error codes.** Only `400 Invalid image` and `404 Session not found` exist. Everything else is a 200 with a `face_detected: false` payload, and that distinction is stated explicitly.
- **Metric definitions in words and in formula.** `engagement_score` is a weighted sum; a reader who knows the weights can reason about the number instead of trusting it.

## Step 5: Review

- Cold-start test: installed in a clean venv, ran `uvicorn`, copy-pasted the quickstart `curl`, got a 200 and a JSON body with `face_detected`.
- Every endpoint in the table exercised except the WebSocket, which was reviewed line by line and noted as untested in the published copy. Marking an untested path is better than implying coverage.
- Lint and link check pass in CI.
- Two defects in the service surfaced while writing, reported here rather than silently documented around: the model path mismatch and the unused session TTL. Both are in the [review report](../audit/report.md) because they are documentation-visible behavior, not private bugs.

## What this sample demonstrates

Reference writing from source: route enumeration, schema fidelity, status codes, defaults, and the judgment to say what an endpoint does *not* do. The reader can verify every claim in the repository.
