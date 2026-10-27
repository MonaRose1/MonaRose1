# Writing process

Five steps. Every sample in this portfolio went through them, and each case study shows the notes from each step.

## 1. Scope

Before opening the repo, write one paragraph: **who reads this, what they are trying to finish, what they already know.**

For the API reference sample the scope was:

> A backend or frontend developer who has cloned the service and needs a working request in under ten minutes, then needs to know exactly which payloads fail. They know HTTP and Python. They do not know our thresholds, session model or authentication.

That paragraph settles most arguments later. It is why that reference leads with a copyable request instead of an architecture diagram, and why every error code has a cause and a fix attached.

If the scope is unclear, ask the person who owns the product. Do not ask the reader.

## 2. Evidence

Documentation is a claim about behavior, so every claim needs a source. I clone the repo and collect evidence in four passes:

| Pass | What I read | What I am looking for |
| --- | --- | --- |
| Entry points | `package.json`, `requirements.txt`, entry modules, Docker files | What the install actually is, which commands exist |
| Configuration | `.env` files, `process.env` and `os.getenv` calls, config modules | Every variable, its default, what breaks without it |
| User paths | Route files, controllers, middleware | The real endpoint surface, auth gates, status codes |
| Existing docs | README, inline comments, test names | Claims that contradict the code |

The last pass is where reviews come from. A README that documents `npm run deploy` when `package.json` has no `deploy` script is not a cosmetic problem: a reader follows it, it fails, and they stop trusting the rest of the page.

## 3. Structure

I keep four page types separate, because mixing them is what makes documentation unreadable:

- **Concept**: what the thing is and how it thinks. Read once.
- **Quickstart**: shortest path to something working. Read once, at install time.
- **How-to**: one job to be done, numbered. Read on demand.
- **Reference**: exhaustive facts, no narrative. Scanned, not read.

If a page is doing two of those jobs, it becomes two pages. The API sample splits the runnable quickstart from the exhaustive reference for exactly this reason.

## 4. Draft

House rules, applied to every sample:

- Second person, active voice, present tense. "You send a frame", not "a frame is sent by the client".
- One idea per sentence. If a sentence has two "and"s, it is two sentences.
- Every command tested, every path real, every screenshot current. Untested instructions are worse than missing instructions.
- Lead with the thing the reader came for. The endpoint, the command, the fix.
- Say the limitation. A doc that hides a limitation costs more support time than it saves.
- Define a term the first time it appears, then use it identically everywhere.

## 5. Review

A checklist that runs before anything is published:

- [ ] Markdown lint passes, no broken relative links
- [ ] Vale style check passes against the project's rule set
- [ ] Every code block copy-pastes and runs
- [ ] Every environment variable appears in the configuration table
- [ ] Every endpoint has method, path, auth, request, response, and its error cases
- [ ] Cold-start test: someone who has never seen the repo follows the doc alone
- [ ] Removed claims that the code contradicts, or fixed the code and said so

That last item is the one that separates a writer from a proofreader.
