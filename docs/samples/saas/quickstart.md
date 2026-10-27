# Quickstart: host your first game

Eight players, one room code, nothing for them to install. This page takes about five minutes.

## What you need

- Node.js 20 or later
- A Firebase project with Firestore enabled
- A Gemini API key, only if you want the AI features in a local build
- A camera and a microphone for the video features

## 1. Get the code

```bash
git clone https://github.com/MonaRose1/Mafia.git
cd Mafia
npm install
```text

## 2. Point the app at your Firebase project

The app reads its Firebase configuration from `firebase-applet-config.json` in the project root. Replace the values with the ones from your project's Firebase console: **Project settings → Your apps → SDK setup and configuration**.

```json
{
  "apiKey": "<WEB_API_KEY>",
  "authDomain": "<PROJECT_ID>.firebaseapp.com",
  "projectId": "<PROJECT_ID>",
  "storageBucket": "<PROJECT_ID>.appspot.com",
  "messagingSenderId": "<SENDER_ID>",
  "appId": "<APP_ID>"
}
```text

Then publish the security rules so the app can read and write rooms:

```bash
npx firebase-tools deploy --only firestore:rules --project <PROJECT_ID>
```text

## 3. Create your environment file

```bash
cp .env.example .env
```text

Set the values you need for local work:

| Variable | Use in local development |
| --- | --- |
| `GEMINI_API_KEY` | AI-assisted features. Leave the placeholder if you do not need them |
| `APP_URL` | `http://localhost:3000` |
| `VITE_ALLOWED_ORIGIN` | `http://localhost:3000` |
| `VITE_RAILWAY_ID` | Leave as is unless you deploy the socket server yourself |

**Warning:** `.env` stays out of Git. The example file contains placeholders only.

## 4. Start it

```bash
npm run dev
```text

Open <http://localhost:3000>. The dev server is configured for port 3000 and accepts connections from your network, so phones on the same Wi-Fi can join with your machine's IP address.

**Note:** Browsers only allow camera and microphone access on `https://` or `localhost`. Testing from a phone over plain `http://192.168.x.x` will block the camera.

## 5. Host a game

1. Sign in on the splash screen.
2. Choose **Create game**.
3. Set the player count, the role mix and the three timers. The defaults work for a first game.
4. Choose **Create**. A room code appears in the lobby.
5. Share the code. Players choose **Join game** and enter it.
6. Wait for every player to show a ready state, then start. Roles are revealed privately.

## Next steps

- [Run a game](../saas/how-to-run-a-game.md): the full host flow, phase by phase
- [Troubleshooting](../saas/troubleshooting.md): camera, room code and connection problems
