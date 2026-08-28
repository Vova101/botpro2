# HideBlitz update channel

This public folder is the static update server for HideBlitz 0.9+.

## One-time setup

Repository Settings → Secrets and variables → Actions → New repository secret:

- Name: `HIDEBLITZ_UPDATE_PRIVATE_KEY`
- Value: base64 Ed25519 private key kept by the HideBlitz owner.

Never commit the private key to GitHub.

## Publish a new version

1. Upload a single portable EXE to `hideblitz/releases/`.
2. Name it exactly `HideBlitz-vMAJOR.MINOR.PATCH.exe`, for example `HideBlitz-v0.9.1.exe`.
3. GitHub Actions automatically hashes every release EXE, selects the highest version, signs the update payload and rewrites `hideblitz/latest.json`.
4. HideBlitz clients see the new signed version on their next automatic check and ask the user whether to update.

`hideblitz/policy.json` controls `minimumVersion` and `required`. Set `required: true` only for a release that must block older clients until they update.
