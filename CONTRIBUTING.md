# Contributing

This repository is a portfolio, so the contribution rules are also the house rules for the writing. They apply to every page.

## Before you write

- **Name the reader and the job.** A page exists because someone has something to finish. If the page cannot name that, it is not ready to be written.
- **Pick one page type.** Concept, quickstart, how-to, or reference. A page that is two of these becomes two pages.
- **Find the evidence.** Quote the source, the route, the manifest or the test. A claim with no source gets flagged in review.

## Voice

Follow [the style guide](docs/style-guide.md). The short version:

- Second person, active voice, present tense
- One idea per sentence
- No "simply", "easily", "just", "obviously"
- Every command tested, every path real
- Warnings name the consequence

## Page structure

```markdown
# Title as a noun phrase or an imperative

One sentence saying what the page is for.

## Prerequisites or before you start   (optional)

## Numbered steps or reference tables

## Next steps or related pages
```

Every page has one level-1 heading, matching the file name, and no skipped heading levels.

## Changes

1. Branch from `main`: `docs/<short-description>`.
2. Edit Markdown only. Do not reformat unrelated pages in the same change.
3. Run the checks locally:

   ```bash
   python3 tools/check-links.py
   npx markdownlint-cli2 "**/*.md"
   vale .
   mkdocs build --strict
   ```

4. Open a pull request. Describe the reader impact, not the edit history.

## Review rubric

A reviewer checks, in this order:

| Check | Question |
| --- | --- |
| Accuracy | Is every claim true of the code today? |
| Reader fit | Does the page start where the reader starts? |
| Structure | Right page type, scannable headings, no skipped levels |
| Voice | House style, no weasel words, warnings name consequences |
| Completeness | Every variable, endpoint or field the reader touches is covered |
| Links | Relative links resolve, anchors exist, nothing points at a deleted section |

Findings are ranked by severity, defined in [the review report](docs/audit/report.md): blocker, high, medium, low. Severity follows reader impact, not effort.

## What does not belong here

- Marketing copy, feature announcements, or claims the code does not support
- Screenshots that will be stale in a month
- Client material, credentials, personal data, or anything under NDA
