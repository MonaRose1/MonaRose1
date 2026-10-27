# Accessibility conformance statement

**Target standard:** WCAG 2.2 level AA
**Status:** Partially conformant
**Date of last assessment:** self-assessed, no third-party audit
**Scope:** candidate portal and interviewer console, desktop and mobile web

A "partially conformant" statement with a dated issue list is honest and useful. A claim of full conformance without an audit is neither.

## What was tested

| Method | Coverage |
| --- | --- |
| Keyboard-only navigation | Sign-in, profile, application form, interview room, notes panel |
| Screen reader | NVDA with Firefox, VoiceOver with Safari, primary flows only |
| Automated checks | axe-core on the main screens, zero critical issues expected |
| Zoom and reflow | 200 percent zoom, 320 px viewport |
| Contrast measurement | Text and status colors against the WCAG contrast formula |
| Motion and timing | Interview timers, transitions, video controls |

Not tested: every combination of assistive technology and browser, PDF reports with a screen reader, and the code editor's screen-reader behavior under a live coding interview.

## Conforms

- **Text alternatives (1.1.1):** profile images and status icons carry text alternatives; decorative graphics are hidden from assistive technology.
- **Keyboard access (2.1.1):** every control reachable by keyboard, including video and microphone toggles.
- **Focus visible (2.4.7):** focus ring present on all interactive elements in the candidate portal.
- **Name, role, value (4.1.2):** form controls are labeled; buttons expose their state.
- **Resize text (1.4.4):** text scales to 200 percent without loss of content.
- **Error identification (3.3.1):** validation errors name the field and the problem.

## Partially conforms

| Criterion | Issue | Impact | Planned fix |
| --- | --- | --- | --- |
| 1.2.2 Captions (AA) | Interview recordings have no captions | Deaf and hard-of-hearing candidates cannot review a recorded interview | Captions for recordings, transcript export |
| 1.4.3 Contrast (AA) | Secondary text and disabled states fall below 4.5:1 in the dark theme | Hard to read for low-vision users | Palette revision with measured contrast |
| 1.4.11 Non-text contrast (AA) | Video control icons at 2.6:1 against the control bar | Controls hard to locate | Icon and border tokens raised to 3:1 |
| 2.4.3 Focus order (A) | Focus order in the interview room does not follow visual order when the notes panel is open | Keyboard users lose their place | DOM order fix in the interview layout |
| 2.2.2 Pause, stop, hide (A) | Timers keep running while a modal is open | Users with cognitive disabilities lose time to read a dialog | Pause timers while a blocking dialog is open |
| 2.5.7 Dragging movements (AA) | The video filter slider requires dragging | Users who cannot drag cannot change the filter | Add a click target on the track |
| 3.3.7 Redundant entry (A) | The application form asks for contact details already in the profile | Extra work for everyone, especially with memory or attention difficulties | Prefill from the profile |

## Does not conform

| Criterion | Issue | Impact | Status |
| --- | --- | --- | --- |
| 1.2.4 Captions (live) (AA) | Live interview audio has no real-time captions | Deaf and hard-of-hearing candidates cannot participate in a live interview without an accommodation | Live transcription under evaluation |
| 2.1.1 Keyboard (A) in the code editor | The in-interview code editor traps focus and does not expose a keyboard path to all editor commands | A keyboard-only candidate cannot complete a live coding exercise | Editor configuration under review |
| 3.3.4 Error prevention (AA) in destructive actions | Ending an interview has no confirmation step and no undo | An accidental end costs the candidate the session | Confirmation dialog with a typed confirmation for end-session |

## Accommodation path

A candidate who needs an accommodation (extra time, captions, an alternative to the live code editor) requests it when accepting the interview invitation. Accommodations are recorded on the interview and shown to the interviewer before the session starts.

The product does not decide whether an accommodation is reasonable; the recruiting organization does. Documentation states the mechanism, not the policy.

## Known workarounds

- **Screen reader users in the interview room:** use the notes panel collapsed, which restores focus order.
- **Low vision in the dark theme:** the light theme passes contrast in more places.
- **Live captions:** the interviewer can enable the platform's transcription panel while live captions are unavailable.

## How to report an accessibility problem

Send the screen, the assistive technology and version, the browser, and what happened instead of what you expected. Reports go to the address in the product footer and are acknowledged within two business days.

## Roadmap

| Quarter | Work |
| --- | --- |
| Next | Contrast tokens, focus order in the interview layout, confirmation on end-session |
| Following | Recorded-interview captions and transcript export |
| Later | Live captioning, code editor keyboard path |

Dates are commitments to review, not delivery promises. The statement is re-published with every change to this table.
