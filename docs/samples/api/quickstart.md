# Quickstart: gaze and behavior analysis service

Get the service running and analyze one frame in about five minutes.

## Before you start

- Python 3.10 or later
- About 500 MB of disk for dependencies
- The ONNX model file (`resnet18_gazevec_best.onnx`, roughly 45 MB) in the project root

## 1. Install

```bash
git clone https://github.com/MonaRose1/InViewAI_API.git
cd InViewAI_API
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Point the service at the model

The service looks for its model file at the path in `ONNX_MODEL_PATH`, and the default in the code does not match the file name in the repository. Set it explicitly:

```bash
export ONNX_MODEL_PATH=resnet18_gazevec_best.onnx
```

**Note:** If the path does not resolve, the service still starts. `GET /health` returns `"model_loaded": false` and frame analysis falls back to constant angles instead of failing.

## 3. Run it

```bash
python main.py
```

Expected output:

```
INFO:     Uvicorn running on http://0.0.0.0:8002 (Press CTRL+C to quit)
```

**Warning:** The service has no authentication and binds to all interfaces. Run it on a private network, or behind a reverse proxy that authenticates requests. Do not expose port 8002 to the internet.

## 4. Check that it is alive

```bash
curl -s http://localhost:8002/health
```

```json
{
  "status": "ok",
  "timestamp": "2026-01-01T12:00:00.123456",
  "model_loaded": true
}
```

`model_loaded` reports only that the ONNX artifact was found and loaded. It does not report that inference is wired up; see [Reference](../api/reference.md#post-apianalyze-frame).

## 5. Analyze a frame

Send a base64-encoded image and a session identifier. The session accumulates metrics across calls.

```bash
IMG=$(base64 -w0 face.jpg)

curl -s -X POST http://localhost:8002/api/analyze-frame \
  -H "Content-Type: application/json" \
  -d "{\"image_data\": \"$IMG\", \"session_id\": \"demo-1\"}"
```

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
```

## 6. Read the session summary

```bash
curl -s http://localhost:8002/api/session-summary/demo-1
```

```json
{
  "session_id": "demo-1",
  "summary": {
    "avg_gaze_deviation": 0.0,
    "eye_contact_ratio": 1.0,
    "blink_rate": 0.0,
    "engagement_score": 0.7
  },
  "total_frames_processed": 1,
  "timestamp": "2026-01-01T12:00:10.111222"
}
```

## Next steps

- [Full reference](../api/reference.md): every endpoint, schema and status code
- [Error catalogue](../api/errors.md): what each failure means and how to fix it
- [Behavior metrics](../ai/behavior-metrics.md): how each number is computed
