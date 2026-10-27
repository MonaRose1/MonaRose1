### Maimoona N (@MonaRose1)

**Technical writer for developer tools and AI products.** I build the software, then write the documentation it deserves: API references developers can copy and run, product guides that survive real support tickets, and doc reviews that find what the README got wrong.

I came to writing from engineering. A dozen shipped applications, mostly MERN, with a FastAPI and ONNX service behind the AI features. Every sample in this repo was written against source code I can point you to, not a fictional product.

---

## Start here

| Sample | What it proves | Read |
| --- | --- | --- |
| **Docs review, before and after** | Finds real defects in an existing README, ranks them, rewrites it | [Audit report](docs/audit/report.md) · [Rewritten README](docs/audit/rewritten-readme.md) |
| **API reference** | Precise reference for a live FastAPI service: auth, schemas, error codes, runnable examples | [Reference](docs/samples/api/reference.md) |
| **Product documentation** | Onboarding, task-based how-tos and troubleshooting for a real-time multiplayer app | [Quickstart](docs/samples/saas/quickstart.md) |
| **AI/ML documentation** | Model card, metric definitions and honest limits for a computer-vision feature | [Model card](docs/samples/ai/model-card.md) |
| **Enterprise and compliance** | Data-handling, security, accessibility and doc governance for a hiring platform | [Data handling](docs/samples/enterprise/data-handling.md) |

Each one comes with the working notes: the brief, the source evidence, the outline, the decisions I made and why, and the review checklist it passed. That is the [writing process](docs/writing-process.md), five steps, applied four ways.

---

## What I actually do

**Reference and API docs.** I read the route files, the middleware and the models, then write down what the code really does: default ports, required environment variables, role gates, status codes, the payloads that fail. If a doc says `npm run deploy`, I check that the script exists before publishing it.

**Product documentation.** Install, configure, first run, the ten things users actually do, then the failure modes. Written from the source and the support questions the code implies.

**Docs reviews.** A severity-ranked defect list with file and line evidence, a fix for every item, and a short note on what to add so the same class of defect stops recurring.

**Docs as code.** Markdown in Git, reviewed by pull request, validated in CI with a linter and a style checker, published to a static site. This repository is set up that way: [mkdocs.yml](mkdocs.yml), [Vale config](vale.ini), [docs CI](.github/workflows/docs.yml).

---

## Toolchain

`Markdown` `Git` `Docusaurus / MkDocs` `OpenAPI` `Vale` `markdownlint` `Mermaid` `curl` `Postman` `Figma` `JavaScript / TypeScript` `Python` `Node.js` `MongoDB` `Firebase`

Reading code is not a side skill for me, it is the method. If the answer is in `server.js`, I read `server.js`.

---

## How I work

1. **Scope.** Who reads this, what they are trying to finish, what they already know. One paragraph, agreed before writing.
2. **Evidence.** Clone the repo, run it, read the code paths a user will touch. Note every claim the existing docs make that the code contradicts.
3. **Structure.** Task-based outline. Concept page for the mental model, how-tos for jobs to be done, reference for the facts, troubleshooting for the failures.
4. **Draft.** Plain language, second person, active voice, one idea per sentence. Every command tested, every path real.
5. **Review.** Lint, link check, read-aloud pass, then a cold-start test: someone who has never seen the repo follows only the doc.

---

## Working with me

Available for contract and full-time technical writing roles, remote, UTC+5. I write developer-facing and end-user documentation, build docs sites, and clean up documentation debt in existing repositories.

- Email: monadevdizayn@gmail.com
- Samples and process: this repository, or the [documentation site](docs/index.md)
- Code I have written and documented: [InViewAI platform](https://github.com/MonaRose1/InViewAI_Ai-powered_interview_platform) · [Gaze analysis service](https://github.com/MonaRose1/InViewAI_API) · [Mafia](https://github.com/MonaRose1/Mafia)

<sub>All samples are written by me against my own repositories. No client work is reproduced here; where a sample is based on a project of mine, it says so.</sub>
