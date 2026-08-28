# HideBlitz releases

Put official portable update executables in this folder with the exact name `HideBlitz-vMAJOR.MINOR.PATCH.exe`.

Clients never trust a file only because it exists here. They first verify the Ed25519-signed `../latest.json`, then verify the downloaded EXE size and SHA-256 from that signed payload.

Do not store the HideBlitz Ed25519 private signing key in this repository.
