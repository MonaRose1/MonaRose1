# Behavior metrics

Four numbers come out of a session. This page defines each one, in the order the service computes it, with the range and the way it fails.

## When a sample is taken

Metrics never recompute on every frame. A sample is taken only when at least `FRAME_SAMPLING_INTERVAL_S` seconds have passed since the last one, default `3.0`.

```
if now - last_sample_time < 3.0: return previous metrics
```

Consequences for anyone reading the numbers:

- A 60-second session contains about 20 samples, not 1,800 frames.
- Calls inside the window return the previous metrics with a new timestamp. The timestamp is when you asked, not when the value was measured.
- `total_frames_processed` in the session summary counts samples, not frames.

## 1. Blink count

An eye-aspect-ratio (EAR) below `EAR_THRESHOLD` (default `0.25`) counts as one blink, with a 0.25-second debounce so a single blink is not counted repeatedly.

```
if ear < 0.25 and now - last_blink_time > 0.25: blink_count += 1
```

**Note:** Both frame paths currently pass a fixed `ear = 0.3`, which is above the threshold, so the count stays at zero. The mechanism is implemented; the input is not.

## 2. Eye contact ratio

The share of samples in which the gaze deviation stayed inside `GAZE_THRESHOLD_DEG` (default `15.0°`).

```
deviation = sqrt(pitch² + yaw²)
if deviation < 15.0: engaged_frames += 1
eye_contact_ratio = engaged_frames / max(1, total_frames)
```

| Property | Value |
| --- | --- |
| Range | `0.0` to `1.0` |
| Unit | Ratio of samples, not of time |
| Sensitive to | Session length: the denominator grows with every sample, so early samples dominate |
| Fails when | Angles are constant, which makes every sample "engaged" and the ratio converge on `1.0` |

There is no smoothing on this metric. A single long look away lowers the ratio permanently for that session.

## 3. Average gaze deviation

The mean angular distance from the camera axis across retained samples.

```
avg_gaze_deviation = mean(sqrt(pitch² + yaw²)) over retained samples
```

| Property | Value |
| --- | --- |
| Range | `0.0` to about `85°`, bounded by the ±60° clamp |
| Unit | Degrees |
| Window | The last `MAX_BUFFER` samples, default `120`, roughly six minutes at a 3-second interval |
| Note | This is a mean of a mean: with constant angles it reports the constant's magnitude, not the person's behavior |

Average deviation is the most interpretable of the four because it stays in the model's native unit. If one number has to appear in a report, this is the honest choice.

## 4. Engagement score

A weighted combination of eye contact and blink rate, scaled to `0.0` to `1.0`.

```
blink_score      = 1 - min(1, |blink_rate - 0.25| / 0.25)
engagement_score = 0.7 × eye_contact_ratio + 0.3 × blink_score
```

The shape of `blink_score` deserves a sentence: it peaks at a rate of `0.25` and falls to zero at `0.0` or `0.5`. It rewards a "normal" blink frequency and penalizes both staring and blinking often. That is a design opinion, not a measurement, and it should be labeled as one wherever the score appears.

| Property | Value |
| --- | --- |
| Range | `0.0` to `1.0` |
| Composition | 70 percent eye contact, 30 percent blink proximity |
| Fails when | Blink rate is unavailable, which zeroes 30 percent of the score regardless of gaze |
| Do not | Compare scores across sessions of different lengths, cameras or lighting |

## Worked example

Two samples, both at or beyond the sampling interval, with the current constant inputs:

| Step | Value |
| --- | --- |
| pitch, yaw | `0.0`, `0.0` |
| deviation | `0.0`, inside 15°, so `engaged_frames = 1` |
| `total_frames` | `1` |
| `eye_contact_ratio` | `1 / 1 = 1.0` |
| `blink_count` | `0`, because `ear = 0.3` never drops below `0.25` |
| `blink_rate` | `blink_count / max(1, sample_count)` = `0.0` |
| `blink_score` | `1 - min(1, |0.0 - 0.25| / 0.25) = 0.0` |
| `engagement_score` | `0.7 × 1.0 + 0.3 × 0.0 = 0.7` |

Every session with a detected face therefore reports `0.7`. If you see exactly `0.7` in production, you are looking at this state, not at a person.

## Known defects

Both are visible in the formulas above and are listed here instead of being smoothed over.

| Defect | Effect | Fix |
| --- | --- | --- |
| `blink_rate` divides by sample count, not elapsed time | It is a per-sample count, not a rate per minute. The name promises a rate the code does not compute | Divide `blink_count` by elapsed seconds and multiply by 60 |
| The timestamp series used for duration is never appended to | Duration stays at `1.0`, so `blink_rate` equals `blink_count` exactly | Append `ts` on every sample, then compute duration from first and last |
