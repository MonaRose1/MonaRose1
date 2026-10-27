# Sample 3: documentation for an AI feature

**Niche:** AI and ML documentation
**Subject:** the ONNX gaze model and the behavior metrics built on it
**Shipped:** [Model card](../samples/ai/model-card.md) · [Behavior metrics](../samples/ai/behavior-metrics.md) · [Evaluation notes](../samples/ai/evaluation-notes.md)

## Step 1: Scope

Three readers, one page each:

| Reader | Needs | Page |
| --- | --- | --- |
| Integrator | What the model returns, in what units, at what cost | Model card |
| Analyst | Exactly how `engagement_score` is computed, and what it does not mean | Behavior metrics |
| Reviewer, hiring manager, or auditor | What was measured, what was not, and where the number becomes a decision about a person | Evaluation notes |

The third reader drives the tone. This feature observes people during job interviews, so documentation that sounds more confident than the evidence is a liability, not a marketing asset.

## Step 2: Evidence

Read: `main.py` in full (`init_ort_session`, `preprocess_face_for_model`, `gaze_vector_to_pitch_yaw_deg`, `update_behavior`, both frame paths), `requirements.txt`, `test_api.py`, `test_frame_analysis.py`, and the committed artifact list.

What the code actually established, and what it did not:

| Established | Not established |
| --- | --- |
| Input is 224×224 RGB, ImageNet mean/std normalization, NCHW float32 | Which dataset the model was trained on, its size, its demographics |
| Output is a 3-vector converted to pitch and yaw in degrees, clamped to ±60° | Accuracy against ground-truth angles: no labelled set exists in the repo |
| Inference runs on CPU via ONNX Runtime, thread counts configurable | Latency under load: no benchmark in the repo |
| MediaPipe face detection selects the frame's face, one face per frame | Behavior with glasses, occlusions, low light, or more than one person |
| Metrics sample at most every 3 seconds, buffer 120 samples | Whether 3-second sampling is adequate for the intended use |

That second column is the model card. A capability section with no evaluation section is a sales document.

## Step 3: Structure

Model cards have a conventional shape, and convention is the point: reviewers scan for known sections.

```
Model card          purpose, inputs, outputs, training, limits, ethical considerations
Behavior metrics    each published number, its formula, its range, its failure mode
Evaluation notes    what the test suite proves, how to build a real eval, what is missing
```

The metrics page exists because the API returns derived numbers, not raw angles. An integrator who reads only the endpoint reference will assume `engagement_score` is a model output. It is a hand-written weighted sum, and the weights belong in the documentation.

## Step 4: Draft decisions

- **Separate "what the model does" from "what the endpoint currently returns".** They differ today: the ONNX session loads, but neither frame path calls `ort_sess.run`, so the published angles are constants. Both facts are in the docs, in that order, because the second one changes what an integrator builds.
- **Give every metric a formula.** Not "a weighted score" but `0.7 × eye_contact_ratio + 0.3 × blink_score`. A reader who has the formula can challenge the metric; that is the point of documenting it.
- **Name the failure modes in the metric, not only in the model.** `blink_rate` divides blinks by sample count, not elapsed time, so it is not a per-minute rate despite the name. That is documented as a known defect with the fix, not smoothed into a vaguer definition.
- **Ethics gets a section, not a disclaimer.** Biometric inference during hiring is a regulated activity in several jurisdictions. The card says so, and says what the product does not do: no automated rejection, no identity inference, no emotion label.
- **No capability claims without a citation to code or test.** Every "supports" line in the card points at a line of source or a test.

## Step 5: Review

- Recomputed every formula by hand against a two-sample trace and matched the service's output.
- Confirmed the constant-angle claim by reading both branches of both endpoints, then verifying against `test_api.py`, which sends a solid-color image and asserts only a `200`.
- Checked terminology against the [style guide](../style-guide.md): "gaze deviation" not "eye tracking accuracy", "session" for the API object, "interview" for the product concept.
- Removed two sentences that implied validated accuracy. Nothing in the repository supports them.

## What this sample demonstrates

Writing about a model honestly: conventional model-card structure, metric definitions precise enough to argue with, and the discipline to publish limits next to capabilities. For an AI company, this is the difference between documentation that survives a security review and documentation that gets rewritten after it.
