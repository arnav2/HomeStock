# HomeStock Mobile (React Native / Expo)

React Native client for HomeStock that talks to the existing FastAPI backend, so you can
monitor and trigger actions from **iPad** and **Android** devices.

> Note: The **backend still runs on a desktop/server** (macOS or Windows). This app is
> a mobile UI that calls the same HTTP API (`/health`, `/download`, `/pipeline`, etc.).

## Requirements

- Node.js 20+
- `npm` or `yarn`
- `expo` CLI (installed globally is recommended):

```bash
npm install -g expo-cli
```

## Install & Run

```bash
cd mobile
npm install       # or: yarn
npm start         # starts Expo dev server
```

Then:

- Press `a` to open **Android emulator** (or use Expo Go on a real Android device)
- Press `i` to open **iOS simulator** (on macOS)

On a real device, open the **Expo Go** app and scan the QR code from the terminal/Expo UI.

## Pointing to Your Backend

In `App.jsx` the backend URL defaults to:

```js
const DEFAULT_BACKEND_URL = "http://localhost:5001";
```

On a physical device, `localhost` is **the device itself**, not your desktop. Change it in
the UI at runtime to point to your desktop/server, for example:

- `http://192.168.1.10:5001`

Where `192.168.1.10` is the LAN IP of the machine running the FastAPI backend.

## Current Features

- Simple screen to:
  - Configure backend base URL
  - Call `/health` and display status
  - Show basic error information if the backend is unreachable

## Next Steps / Extensions

You can extend this app to:

- Trigger downloads (`POST /download/`)
- Trigger parsing (`POST /parse/`)
- Trigger / monitor pipeline runs (`POST /pipeline/run`)
- Show logs and recent download status

All API contracts are the same as used by the Electron/React frontend.


