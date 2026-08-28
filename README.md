# HideBlitz Update Storage

Public update storage for HideBlitz portable builds.

Upload new portable builds to `hideblitz/releases/` using the filename format:

`HideBlitz-vMAJOR.MINOR.PATCH.exe`

Example: `HideBlitz-v0.9.1.exe`

After an EXE is uploaded, GitHub Actions recalculates SHA-256 and updates `hideblitz/latest.json`. HideBlitz clients read that file automatically on startup.

`hideblitz/policy.json` controls whether an update is optional or required.
