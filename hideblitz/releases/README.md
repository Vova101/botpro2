# HideBlitz release storage

Do **not** commit HideBlitz EXE files to this directory anymore.

Official binaries live only in GitHub Releases as the asset `HideBlitz.exe`. The signed `latest.json` is published beside the EXE in the same Release.

Normal release flow is local from the private HideBlitz repository:

```powershell
.\scripts\build-windows.ps1
.\scripts\publish-release.ps1
```

`publish-release.ps1` signs `latest.json` locally with the owner's Ed25519 key, creates the GitHub Release as a draft, uploads both `HideBlitz.exe` and `latest.json`, and only then publishes the Release. This prevents clients from observing a half-published update and avoids automatic GitHub Actions usage.

The workflow in `.github/workflows/hideblitz-index.yml` is manual recovery only.
