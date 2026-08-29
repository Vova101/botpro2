# HideBlitz releases

HideBlitz binaries are distributed through **GitHub Releases**, not through Git history.

## Normal release flow (0.9.4 and newer)

1. Build `HideBlitz.exe` locally from the private HideBlitz repository.
2. Create a public GitHub Release in `Vova101/botpro2` with tag `hideblitz-vMAJOR.MINOR.PATCH`.
3. Upload exactly one asset named `HideBlitz.exe` and publish the Release.
4. The public workflow hashes the EXE, signs `latest.json` with the repository secret, attaches `latest.json` to the Release, and keeps only the tiny signed compatibility index in Git.

Do **not** commit normal future EXE files into this folder.

## One-time 0.9.3 compatibility bridge

Clients up to 0.9.2 only accept `raw.githubusercontent.com` update binaries. Therefore `HideBlitz-v0.9.3.exe` is the final binary that must also be committed to this folder. The workflow will publish the same bytes as the user-facing `HideBlitz.exe` Release asset. Once users can run 0.9.3, all later binaries can live only in GitHub Releases.

Clients never trust a file only because it exists on GitHub. They verify the Ed25519-signed manifest and then verify the downloaded EXE size and SHA-256.

Never store the HideBlitz Ed25519 private signing key in the repository.
