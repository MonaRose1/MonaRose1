# Sample 2: product documentation from zero

**Niche:** SaaS and end-user product documentation
**Repository:** [Mafia](https://github.com/MonaRose1/Mafia) (React 19, TypeScript, Vite, Firebase, live video)
**Shipped:** [Quickstart](../samples/saas/quickstart.md) · [Run a game](../samples/saas/how-to-run-a-game.md) · [Troubleshooting](../samples/saas/troubleshooting.md)

## Step 1: Scope

> A player who was invited to a game and has never seen the product, and a host who needs to get eight people playing without a support ticket. They are on a laptop with a camera. They do not read release notes and they will not read a README. They will scan two headings and try the first numbered list.

This is the difference between this sample and the API one: the reader is not motivated. Documentation for a player has to earn the first 30 seconds, so the quickstart opens with "create a room", not with architecture or configuration.

## Step 2: Evidence

The repository had **no README**. Zero onboarding material for a game with four roles, five game phases, live video, chat, a friend system, a leaderboard, achievements and a currency system.

Evidence gathered from source, not invented:

| Source | What it told me |
| --- | --- |
| `src/types.ts` | The product's real vocabulary: `RoleType` (Mafia, Doctor, Detective, Citizen), `TeamType`, `GamePhase` (night, morning, discussion, voting, result), `GameSettings` (three timers, role counts, private rooms, anonymous voting, dead chat, voice and video toggles) |
| `src/types.ts`, `Player` | Player states `ALIVE`, `DEAD`, `SPECTATOR`, plus `cameraOn`, `isMuted`, `isSpeaking`, `voteTarget` |
| `src/types.ts`, `UserProfile` | Level, XP, coins, gems, rank title, win rate, per-game history |
| `firestore.rules` | Six collections in play: `users`, `rooms`, `friends`, `matchmaking_queue`, `settings`, `project_settings` |
| `package.json` | Real scripts only: `dev` on port 3000, `build`, `preview`, `lint` as `tsc --noEmit`. No test runner exists, so no doc claims tests |
| `.env.example` | Four variables, two of which are build-time `VITE_` values |
| `firebase-applet-config.json` | Firebase is configured by a committed config file, not by environment variables. That is a setup step readers cannot guess |

## Step 3: Structure

Product docs fail when they are organized by feature. Players think in jobs, so the pages are organized that way:

- **Quickstart**: install, configure, run, open one room. Five steps, five minutes.
- **Run a game**: the host's job from lobby to results, with a phase table and a timer table.
- **Troubleshooting**: the six failures that produce a support message, in the order they occur.

The role list and the phase list live inside "run a game" rather than in a separate concepts page, because a host reads them while setting up, not before.

## Step 4: Draft decisions

- **Open with the outcome.** "Eight players, one room, no install for them" is the first line, not "Mafia is a social deduction game".
- **Name roles by their behavior.** "The Doctor protects one player each night" beats a table of enum values.
- **State who can do what.** Every action line says "host" or "player", because the two readers need different pages of the same product.
- **Publish the real constraints.** The dev server runs on port 3000 and binds all interfaces; camera access needs HTTPS or localhost. A reader hitting either without warning files a bug.
- **No screenshots of a build I cannot guarantee.** Interfaces change; a wrong screenshot is worse than a described step. The pages describe what to tap and what appears.

## Step 5: Review

- Walked the host path against the code: create, join by code, lobby ready state, role reveal, night action, discussion, vote, results. Each page step maps to a component or a Firestore field.
- Confirmed every command against `package.json`. `npm run test` does not exist, so it is not in the docs; the linter is `npm run lint` and it type-checks rather than lints style.
- Cold-start test: fresh clone, `.env` from the example, `npm install`, `npm run dev`, opened `http://localhost:3000`.
- Every troubleshooting entry corresponds to a real failure mode in the code path: blocked camera permission, wrong room code, Firestore rules rejection, wrong port, blocked Gemini key, and a stale build served by `preview`.

## What this sample demonstrates

Turning an undocumented product into usable documentation: extracting vocabulary from types, mapping a real user journey from source, and writing for a reader who will not read. The hard part is not prose, it is knowing which eight of the forty possible facts belong on the first page.
