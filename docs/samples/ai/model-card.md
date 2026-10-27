# Model card: gaze vector model

What this model does, what it was built from, and where it should not be used.

## Overview

| Field | Value |
| --- | --- |
| Task | Regress a 3-vector gaze direction from a single face image |
| Architecture | ResNet-18 backbone with a regression head, exported to ONNX |
| Artifact | `resnet18_gazevec_best.onnx`, approximately 46 MB, committed to the repository |
| Runtime | ONNX Runtime, `CPUExecutionProvider`, configurable intra-op and inter-op threads |
| Upstream detector | MediaPipe face detection, one face per frame |
| Version | Unversioned. The artifact name is the only identifier |
| Maintainer | InViewAI |

## Inputs

| Property | Value |
| --- | --- |
| Image | RGB, resized to 224×224 |
| Normalization | ImageNet mean `[0.485, 0.456, 0.406]`, standard deviation `[0.229, 0.224, 0.225]` |
| Layout | NCHW, float32 |
| Faces per frame | One. The largest detected face is cropped before inference |
| Source format | Base64 JPEG or PNG, sent by the client |

## Outputs

| Property | Value |
| --- | --- |
| Raw output | 3-element vector, interpreted as a direction |
| Converted | Pitch and yaw in degrees, each clamped to ±60 |
| Angular convention | Yaw from `atan2(x, -z)`, pitch from `atan2(y, sqrt(x² + z²))` |
| Post-processing | Optional smoothing over a window of retained samples (`GAZE_SMOOTHING_WINDOW`, default 5) |

A positive yaw means the face is turned to one side of the camera axis, a positive pitch means looking up. Sign conventions are relative to the image, not to the room.

## Intended use

Estimating whether a person is looking toward the camera during a remote interview, aggregated over a session into a summary metric.

### Reasonable uses

- A live indicator that helps an interviewer notice when a candidate is looking away
- A session-level summary an interviewer reads alongside their own notes
- Research and demonstration in a controlled setting

### Out of scope

- Any automated hiring decision, score or rejection
- Identity verification, emotion detection, attention measurement for assessment
- Medical, diagnostic or psychological inference
- Continuous monitoring of a person who has not consented
- Use on minors

## Limitations

- **No published accuracy.** No labelled dataset, no benchmark and no tolerance analysis exist in the repository. Until there is one, treat the output as an unvalidated estimate.
- **Single face, single person.** Group scenes, partial faces and heavy occlusion are outside the trained distribution.
- **Angle range.** Output is clamped to ±60°, so extreme head turns saturate and read as the same value.
- **No per-person calibration.** Different face shapes, camera heights and screen positions shift the neutral point. A fixed threshold applied to everyone will misclassify some of them.
- **CPU only.** Throughput depends on the host; thread counts are configurable but not benchmarked.
- **Sampling, not tracking.** Metrics update at most every 3 seconds by default, so short events are invisible.
- **The published API currently returns constants.** `POST /api/analyze-frame` and the socket path feed fixed angles (`0.0`) into the metrics function; the ONNX session loads but its output is not consumed. `model_loaded: true` in `/health` reports artifact loading only.

## Training data

Not documented in the repository. Unknown: dataset, size, collection method, geographic and demographic composition, consent process, labelling protocol, train and test split. This is a documentation gap, and it is recorded as one rather than filled with an assumption.

## Ethical considerations

This model observes people in a hiring context, which makes it a sensitive use in several jurisdictions.

- **Consent.** A candidate should be told that gaze is estimated, what is stored and for how long, before the interview starts.
- **Biometric classification.** Gaze estimation from face images may be treated as biometric processing under GDPR and similar regimes, which carries explicit-consent and impact-assessment obligations.
- **No decision authority.** The output must never gate a candidate automatically. A human makes the decision and the model's output, if shown at all, is one signal among many.
- **Aggregation bias.** Session-level ratios hide individual frames; a candidate who looked away once for a legitimate reason and a candidate who never looked at the camera can produce similar summaries at different session lengths.
- **Accessibility.** People with motor conditions, visual impairments or atypical gaze patterns are systematically disadvantaged by any threshold that assumes a stable forward gaze.

## How to cite

> InViewAI gaze vector model (ResNet-18, ONNX). Unversioned artifact. Not independently evaluated.
