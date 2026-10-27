# Error catalogue

Every failure a reader can hit, the cause, and the fix. If a symptom is not here, check [the reference](reference.md) for the endpoint's actual status codes; the service returns very few of them.

## HTTP status codes

| Code | `detail` | Cause | Fix |
| --- | --- | --- | --- |
| `400` | `Invalid image` | `image_data` decoded to bytes but not to an image, or the base64 itself is malformed | Send real image bytes. Strip the `data:image/...;base64,` prefix only if your client already decodes it; the service accepts both |
| `404` | `Session not found` | The summary was requested for a session the process does not know | Send one frame on that session first, or resend the frame if the service restarted |
| `422` | FastAPI validation body | `image_data` or `session_id` missing, or a field has the wrong type | Check the field names exactly: `image_data`, `session_id` |
| `500` | `AI Evaluation Failed` | The platform backend could not reach this service, not an error from this service | See [connection refused](#connection-refused-from-the-platform-backend) |

## Symptoms

### `health` reports `model_loaded` false

The artifact path did not resolve. The default in code is `resnet18_gazevec_best1.onnx`; the file committed to the repository is `resnet18_gazevec_best.onnx`.

```bash
export ONNX_MODEL_PATH=resnet18_gazevec_best.onnx
```text

The service runs either way, but nothing measures gaze until the path is right. Even with the model loaded, the HTTP and socket endpoints currently feed constant angles into the metrics; see the note in [the reference](reference.md#post-apianalyze-frame).

### Connection refused from the platform backend

The platform backend proxies to `AI_SERVICE_URL`, default `http://localhost:8002`. If this service runs in a container or on another host, `localhost` points at the wrong machine.

Set the platform backend's variable to the reachable address:

```bash
export AI_SERVICE_URL=http://<gaze-service-host>:8002
```text

### Every metric is identical between calls

Working as implemented, not a bug in your client. Metrics recompute at most once every `FRAME_SAMPLING_INTERVAL_S` seconds (default 3). Calls inside the window return the previous values. Space requests at least 3 seconds apart or lower the interval.

### `face_detected` is always false

In order of likelihood:

1. **Frames are too dark or too small.** MediaPipe needs a recognizable face; test with a well-lit 640×480 or larger frame first.
2. **The image is not what you think it is.** Save one payload to disk and open it. A canvas `toDataURL` on a zero-sized canvas produces a blank image that decodes but contains no face.
3. **The base64 is truncated.** Large frames cut by a client-side size limit decode partially or not at all; a truncated frame usually returns `400`, not `face_detected: false`.

### The socket connects but nothing comes back

Three causes, all silent by design:

- No face in the frame, so the service sends nothing for that frame.
- The message `type` is not exactly `analyze_frame`.
- The third-party socket client did not send a text frame.

Use the HTTP endpoint while debugging; it always answers.

### Metrics look frozen across a long session

`total_frames_processed` counts samples, not frames. If it stops increasing while you keep sending frames, the images are being rejected before sampling. Check `face_detected` and the status code.

### Session data disappeared

Sessions live in process memory only. A restart, a crash or a redeploy clears all of them. Persisting sessions is a platform concern, not a service concern today.

## Reporting a problem

Include the endpoint, the status code, the `session_id`, and whether `health` reported `model_loaded: true`. Never paste candidate images or session identifiers from production into an issue.
