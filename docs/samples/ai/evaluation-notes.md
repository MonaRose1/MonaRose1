# Evaluation notes

What the current test suite proves, what it does not, and how to build an evaluation that would let these numbers be trusted.

## What the tests cover

`test_api.py` is a smoke suite against a running service. It builds a solid-color 224×224 image, sends it to each endpoint, and asserts an HTTP `200`.

| Endpoint | Assertion | What that proves |
| --- | --- | --- |
| `GET /health` | `200` | The app started and the route is mounted |
| `POST /api/analyze-frame` | `200` with a blank image | A frame that decodes returns a response; it does not prove face handling, because a blank image contains no face |
| `POST /api/evaluate-answer` | `200` | The endpoint exists. The payload is fixed by design, so a value assertion would be misleading |
| `GET /api/session-summary/{id}` | `200` | Session state was created by the previous call |
| Socket path | Connection and one message | The socket accepts a frame and replies |

`test_frame_analysis.py` exercises the frame path with local files. Neither file asserts accuracy: no labelled angle, no tolerance, no comparison to a reference implementation.

**Conclusion for a reader:** the suite is a contract test for the API surface. It is not an evaluation of the model, and it cannot detect the constant-angle behavior because a constant satisfies every current assertion.

## What a real evaluation needs

Four parts, in the order they become useful.

### 1. A labelled set

Ground truth for pitch and yaw per image. Two practical routes:

- **Head-pose rig.** A person (or a mannequin head) at measured angles on a marked arc, captured at several camera distances and lighting levels. Twenty angles × three conditions is enough to expose gross error.
- **Synthetic renders.** A 3D head model rendered at known angles. Cheap, precise, and weaker evidence about real faces. Use it to catch regressions, not to claim accuracy.

Label at least: `image`, `pitch_true`, `yaw_true`, `lighting`, `distance`, `glasses` (y/n), `skin_tone_bucket` if you intend to report subgroup error.

### 2. Metrics

| Metric | Why |
| --- | --- |
| Mean absolute error per angle | The headline number, in degrees |
| P90 absolute error | Shows the tail; the tail is what users notice |
| Error at clamp boundaries | Confirms ±60° saturation behavior |
| Detection failure rate | Share of labelled images where no face is found at all |
| Per-subgroup MAE | The only way to show the model is not systematically worse for a group |
| Latency p50 and p95 | Whether a 3-second sampling interval is achievable on the deployment host |

Report MAE in degrees, never as a percentage or an invented "accuracy score". A percentage hides which direction the error goes.

### 3. Acceptance thresholds

Set them before running the test, or the test becomes a search for a flattering cut:

- MAE ≤ 10° per angle on the rig set
- P90 ≤ 20° per angle
- Detection failure ≤ 2 percent on well-lit frontal images
- No subgroup with MAE more than 1.5× the overall figure
- Latency p95 under one third of the sampling interval

Missing a threshold is a result, not a failure of the evaluation. Publish it.

### 4. Versioning

Every stored metric needs the model version that produced it. Today the artifact is unversioned and the API returns no model identifier, which makes two sessions from different builds indistinguishable.

Add `model_version` and `sampling_interval_s` to every metric payload. Both are one line of code and they make every historical number interpretable.

## What is missing before this feature can be shown to a customer

| Gap | Consequence | Owner |
| --- | --- | --- |
| No labelled evaluation | Accuracy cannot be stated | ML |
| Constant angles on the live paths | No measurement is happening today | Backend |
| `blink_rate` divides by sample count | The metric name misleads | Backend |
| No calibration step | Thresholds misclassify individuals | Product |
| No consent or retention documentation | Biometric processing without a stated basis | Legal and docs |
| No model version in output | Historical data cannot be compared | Backend |
| Unversioned 46 MB artifact in Git | No reproducibility, large clones | Engineering |

Written down, this table is a roadmap. Left unwritten, each row becomes a support ticket or a compliance finding.
