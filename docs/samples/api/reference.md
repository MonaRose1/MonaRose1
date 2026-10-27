# API reference

The service analyzes a video frame for face presence and accumulates behavior metrics per session. Base URL in local development: `http://localhost:8002`.

**Warning:** No endpoint authenticates requests, and the server binds to `0.0.0.0`. Treat port 8002 as internal.

## Endpoint summary

| Method | Path | Purpose | Auth |
| --- | --- | --- | --- |
| `GET` | `/health` | Liveness and model load status | None |
| `POST` | `/api/analyze-frame` | Analyze one base64 image, accumulate metrics | None |
| `GET` | `/api/session-summary/{session_id}` | Return accumulated metrics for a session | None |
| `POST` | `/api/evaluate-answer` | Score a free-text interview answer | None |
| `WS` | `/ws/analyze/{session_id}` | Stream frames over a socket | None |

Sessions are held in process memory. Restarting the service discards every session.

---

## `GET /health`

Returns liveness and whether the ONNX model artifact loaded at startup.

### Response fields

| Field | Type | Description |
| --- | --- | --- |
| `status` | string | `ok` while the process is serving |
| `timestamp` | string | ISO 8601 local time of the response |
| `model_loaded` | boolean | `true` if the ONNX artifact was found and loaded at startup |

**Note:** `model_loaded: false` does not fail any request. Frame analysis continues with constant angles instead of model output. See the [troubleshooting entry](errors.md#health-reports-model_loaded-false).

### Example

```bash
curl -s http://localhost:8002/health
```text

```json
{ "status": "ok", "timestamp": "2026-01-01T12:00:00.123456", "model_loaded": true }
```text

---

## `POST /api/analyze-frame`

Analyzes a single frame. If the session does not exist, it is created. Metrics are recomputed at most once every `FRAME_SAMPLING_INTERVAL_S` seconds (default `3.0`); calls inside that window return the previous metrics unchanged.

### Request body

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `image_data` | string | Yes | Base64-encoded image, either raw base64 or a `data:image/...;base64,` URI |
| `session_id` | string | Yes | Session to attribute the frame to. Any string; created on first use |

### Response body

| Field | Type | Description |
| --- | --- | --- |
| `session_id` | string | Echo of the request value |
| `gaze_analysis.pitch` | number | Vertical gaze angle in degrees |
| `gaze_analysis.yaw` | number | Horizontal gaze angle in degrees |
| `behavior_analysis` | object | Current metric values, see [Behavior metrics](../ai/behavior-metrics.md) |
| `face_detected` | boolean | `false` when MediaPipe found no face in the frame |
| `timestamp` | string | ISO 8601 local time |

### Behavior to know before integrating

- **The returned angles are constants.** Both the face-found and no-face branches pass fixed values (`pitch: 0.0`, `yaw: 0.0`, `ear: 0.3`) into the metrics function. The ONNX model is loaded at startup but its output is not used by this endpoint. Do not build UI that presents these angles as measurements.
- **No face is not an error.** The endpoint returns `200` with `face_detected: false` and the metrics from the previous sample.
- **Frames are sampled, not counted.** Only one call per sampling window advances `total_frames_processed`. Sending 15 frames per second does not produce 15 samples per second.
- **Session state is unbounded.** `SESSION_TTL_S` is read from the environment but no expiry is enforced, so sessions persist until the process restarts.

### Status codes

| Code | Condition | Body |
| --- | --- | --- |
| `200` | Frame decoded, with or without a face | Normal response |
| `400` | `image_data` is not decodable as an image | `{"detail": "Invalid image"}` |
| `422` | Body is missing a required field or has the wrong type | FastAPI validation error |

### Example

```bash
curl -s -X POST http://localhost:8002/api/analyze-frame \
  -H "Content-Type: application/json" \
  -d '{"image_data": "data:image/jpeg;base64,/9j/4AAQSkZJRg...", "session_id": "candidate-42"}'
```text

```json
{
  "session_id": "demo-1",
  "gaze_analysis": { "pitch": 0.0, "yaw": 0.0 },
  "behavior_analysis": {
    "avg_gaze_deviation": 0.0,
    "eye_contact_ratio": 1.0,
    "blink_rate": 0.0,
    "engagement_score": 0.7
  },
  "face_detected": true,
  "timestamp": "2026-01-01T12:00:03.456789"
}
```text

---

## `GET /api/session-summary/{session_id}`

Returns the last computed metrics for a session and how many samples it has collected.

### Path parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `session_id` | string | Session created by a previous frame call or socket connection |

### Response body

| Field | Type | Description |
| --- | --- | --- |
| `session_id` | string | Echo of the path value |
| `summary` | object | Current metrics, same schema as `behavior_analysis` |
| `total_frames_processed` | integer | Number of samples taken, not number of frames sent |
| `timestamp` | string | ISO 8601 local time |

### Status codes

| Code | Condition | Body |
| --- | --- | --- |
| `200` | Session exists | Normal response |
| `404` | No session with that identifier | `{"detail": "Session not found"}` |

A `404` here is usually a restarted service, not a wrong identifier.

---

## `POST /api/evaluate-answer`

Accepts an interview question and answer and returns a scored evaluation object.

### Request body

| Field | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `question` | string | Yes | | The interview question |
| `answer` | string | Yes | | The candidate's answer |
| `job_role` | string | No | `Software Engineer` | Role to evaluate against |

### Response body

| Field | Type | Description |
| --- | --- | --- |
| `question`, `answer`, `job_role` | string | Echo of the request |
| `evaluation.relevance_score` | number | Fixed `0.5` |
| `evaluation.completeness_score` | number | Fixed `0.5` |
| `evaluation.technical_accuracy_score` | number | Fixed `0.5` |
| `evaluation.communication_skills_score` | number | Fixed `0.5` |
| `evaluation.overall_score` | number | Fixed `0.5` |
| `evaluation.strengths` | array | Always empty |
| `evaluation.improvement_areas` | array | Always empty |
| `evaluation.sentiment_analysis` | string | Always `neutral` |
| `evaluation.detailed_feedback` | string | Always `Mock evaluation` |
| `timestamp` | string | ISO 8601 local time |

**Warning:** This endpoint returns a fixed payload. It does not call a model. Do not display these scores to candidates or use them in ranking until the implementation changes; the field names are stable, the values are not real.

---

## `WS /ws/analyze/{session_id}`

Persistent socket for continuous analysis. Same session model as the HTTP endpoint.

### Client to server

```json
{ "type": "analyze_frame", "image_data": "<base64 or data URI>" }
```text

Messages with any other `type` are ignored without a response.

### Server to client

```json
{
  "type": "analysis_result",
  "session_id": "demo-1",
  "gaze_analysis": { "pitch": 0.0, "yaw": 0.0 },
  "behavior_analysis": { "avg_gaze_deviation": 0.0, "eye_contact_ratio": 1.0, "blink_rate": 0.0, "engagement_score": 0.7 },
  "timestamp": "2026-01-01T12:00:03.456789"
}
```text

### Behavior to know

- A frame with no detectable face produces no message at all. A client waiting on a reply per frame will stall; use the HTTP endpoint if you need a response per frame.
- A frame that fails to decode is also skipped silently.
- The socket inherits the same constant-angle behavior as the HTTP endpoint.

### Example

```bash
websocat ws://localhost:8002/ws/analyze/demo-1
# then paste:
# {"type": "analyze_frame", "image_data": "<base64>"}
```text

---

## Configuration

Every variable is read with `os.getenv` at import time. Set them in the environment or in a `.env` file in the working directory.

| Variable | Default | Effect |
| --- | --- | --- |
| `PORT` | `8002` | HTTP and WebSocket port |
| `ONNX_MODEL_PATH` | `resnet18_gazevec_best1.onnx` | Model file loaded at startup. The default name does not match the file committed to the repository; set it explicitly |
| `ALLOWED_ORIGINS` | `http://localhost,http://127.0.0.1` | Comma-separated CORS origins. Requests from other origins are rejected |
| `OUT_DIR` | `./outputs` | Directory created at startup for output files |
| `ORT_INTRA_THREADS` | `2` | ONNX Runtime threads within an operator |
| `ORT_INTER_THREADS` | `1` | ONNX Runtime threads across operators |
| `MAX_BUFFER` | `120` | Samples retained per metric series in a session |
| `GAZE_SMOOTHING_WINDOW` | `5` | Retained gaze samples used for smoothing |
| `EAR_THRESHOLD` | `0.25` | Eye-aspect-ratio below this value counts as a blink |
| `GAZE_THRESHOLD_DEG` | `15.0` | Deviation below this many degrees counts as eye contact |
| `FRAME_SAMPLING_INTERVAL_S` | `3.0` | Minimum seconds between metric samples |
| `SESSION_TTL_S` | `1800` | *Reserved.* Read from the environment, no expiry is enforced |
| `WS_FRAME_RATE_LIMIT` | `15.0` | *Reserved.* Read from the environment, no rate limit is enforced |
| `ENGAGEMENT_WINDOW_S` | `60` | *Reserved.* Read from the environment, not used in the current metric math |

Variables marked *reserved* are declared and unused. Do not rely on them as controls.
