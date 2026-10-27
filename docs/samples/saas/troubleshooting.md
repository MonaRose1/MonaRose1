# Troubleshooting

Six problems produce almost every support message. Each one names the symptom, the cause and the fix.

## The camera shows a black square

**Cause:** The browser blocked camera access, or another app holds the device.

**Fix:**

1. Look for the camera icon in the address bar and allow access for the site.
2. Close other tabs using the camera, then reload.
3. On macOS, check **System Settings → Privacy & Security → Camera** and confirm the browser is listed.
4. If you opened the app over plain `http://` from another device, the browser blocks the camera by design. Use `https://` or `localhost`.

## Audio works but nobody can hear me

**Cause:** The microphone is muted in the app, or the wrong input device is selected.

**Fix:** Check the mute control in the player bar first. If it shows unmuted, check the operating system input device. Player video and audio controls are per player, so a muted player stays muted for the whole game until they unmute.

## "Room not found" when joining

**Cause:** A typo in the code, or the host closed the room.

**Fix:** Room codes are case-sensitive. Ask the host to read the code again from the lobby. If the host left or the tab closed, the room no longer exists and a new one has to be created.

## The page loads but nothing happens

**Cause:** Usually a missing or wrong Firebase configuration, which fails silently in the client.

**Fix:**

1. Open the browser console.
2. Look for Firestore permission errors or an invalid API key message.
3. Confirm `firebase-applet-config.json` contains your project's values, not the placeholders.
4. Confirm the rules were deployed to the same project the config points at.

## Changes do not appear after a rebuild

**Cause:** `npm run preview` is serving an old build from `dist`.

**Fix:**

```bash
npm run clean
npm run build
npm run preview
```text

## The dev server starts on the wrong port

**Cause:** The dev script is pinned to port 3000 but the port is already in use, or you ran a bare `vite`.

**Fix:** Stop whatever holds port 3000 and run `npm run dev` again. If you need another port, pass it explicitly: `npx vite --port 3001`. Then update `APP_URL` and `VITE_ALLOWED_ORIGIN` to match, or sign-in and video calls will point at the old address.

## Still stuck

Collect three things before asking for help: the browser and version, the console error text, and whether the problem happens on `localhost` or a network address. Those three answers separate a configuration problem from a permissions problem in almost every case.
