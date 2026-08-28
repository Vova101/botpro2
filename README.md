# HideBlitz Update Storage

Public storage for official HideBlitz portable updates.

## One-time setup

Add the repository Actions secret `HIDEBLITZ_UPDATE_PRIVATE_KEY`. Its value must be the base64 raw 32-byte Ed25519 private seed matching the public key embedded in HideBlitz 0.9.

Never commit that private key to this repository.

## Publishing a new version

Upload the final one-file portable EXE to `hideblitz/releases/` using exactly:

`HideBlitz-vMAJOR.MINOR.PATCH.exe`

Example:

`HideBlitz-v0.9.1.exe`

After the upload, GitHub Actions:

1. Calculates SHA-256 and file size.
2. Reads `hideblitz/policy.json`.
3. Creates a schema-2 update manifest.
4. Signs its canonical payload with Ed25519.
5. Updates `hideblitz/latest.json`.

HideBlitz clients check `latest.json` automatically on startup and accept it only when the signature matches the public key embedded in the client.

`hideblitz/policy.json` controls `minimumVersion`, whether an update is `required`, and optional release notes.
