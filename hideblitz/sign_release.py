#!/usr/bin/env python3
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import quote

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

OWNER = "Vova101"
REPO = "botpro2"
KEY_ID = "hideblitz-prod-1"


def version_key(value: str):
    try:
        parts = tuple(int(x) for x in value.split("."))
        return parts if len(parts) == 3 else (-1, -1, -1)
    except Exception:
        return (-1, -1, -1)


def load_builds(latest_path: Path):
    builds = {}
    if not latest_path.exists():
        return builds
    try:
        old = json.loads(latest_path.read_text(encoding="utf-8"))
        if old.get("schema") == 2 and old.get("payload"):
            payload = json.loads(base64.b64decode(old["payload"]).decode("utf-8"))
            builds.update(payload.get("builds") or {})
    except Exception as exc:
        print(f"Ignoring unreadable previous manifest: {exc}")
    return builds


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--exe", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--tag", required=True)
    p.add_argument("--latest", default="hideblitz/latest.json")
    p.add_argument("--policy", default="hideblitz/policy.json")
    args = p.parse_args()

    if version_key(args.version) == (-1, -1, -1):
        raise SystemExit("version must be MAJOR.MINOR.PATCH")
    if args.tag != f"hideblitz-v{args.version}":
        raise SystemExit(f"tag/version mismatch: {args.tag} vs {args.version}")

    exe_path = Path(args.exe)
    latest_path = Path(args.latest)
    policy_path = Path(args.policy)
    data = exe_path.read_bytes()
    if len(data) < 2 or data[:2] != b"MZ":
        raise SystemExit("HideBlitz.exe is not a Windows PE executable")
    digest = hashlib.sha256(data).hexdigest()
    size = len(data)

    builds = load_builds(latest_path)
    existing = builds.get(args.version)
    if existing:
        old_hash = str(existing.get("sha256") or "").lower()
        if old_hash and old_hash != digest:
            raise SystemExit(
                f"Version {args.version} is immutable: registered {old_hash}, got {digest}"
            )

    # Compatibility bridge: 0.9.0-0.9.3 binaries already stored in Git remain
    # valid for old clients that only accept raw.githubusercontent.com. Future
    # releases do not need a Git copy: when the versioned raw file is absent,
    # the signed manifest points directly to the GitHub Release asset.
    raw_candidate = Path(f"hideblitz/releases/HideBlitz-v{args.version}.exe")
    if raw_candidate.exists():
        raw_data = raw_candidate.read_bytes()
        raw_hash = hashlib.sha256(raw_data).hexdigest()
        if raw_hash != digest:
            raise SystemExit(
                f"Raw compatibility file for {args.version} differs from Release asset"
            )
        filename = raw_candidate.name
        download_url = (
            f"https://raw.githubusercontent.com/{OWNER}/{REPO}/main/"
            f"{quote(raw_candidate.as_posix(), safe='/')}"
        )
        storage = "legacy-raw-bridge"
    elif existing and str(existing.get("sha256") or "").lower() == digest and existing.get("url"):
        # Never silently rewrite the trust location for an already registered
        # immutable build merely because the publishing workflow itself changed.
        filename = str(existing.get("filename") or "HideBlitz.exe")
        download_url = str(existing["url"])
        storage = "existing-registration"
    else:
        filename = "HideBlitz.exe"
        download_url = (
            f"https://github.com/{OWNER}/{REPO}/releases/download/"
            f"{quote(args.tag, safe='')}/HideBlitz.exe"
        )
        storage = "github-release"

    builds[args.version] = {
        "filename": filename,
        "url": download_url,
        "sha256": digest,
        "size": size,
    }

    valid = [v for v in builds if version_key(v) != (-1, -1, -1)]
    if not valid:
        raise SystemExit("No registered HideBlitz builds")
    latest_version = max(valid, key=version_key)
    latest = builds[latest_version]

    policy = {"minimumVersion": "0.9.0", "required": False, "notes": ""}
    if policy_path.exists():
        policy.update(json.loads(policy_path.read_text(encoding="utf-8")))

    payload_obj = {
        "latest": {"version": latest_version, **latest},
        "minimumVersion": str(policy.get("minimumVersion") or latest_version),
        "required": bool(policy.get("required", False)),
        "notes": str(policy.get("notes") or ""),
        "builds": dict(sorted(builds.items(), key=lambda kv: version_key(kv[0]))),
    }
    payload = json.dumps(
        payload_obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")

    seed = base64.b64decode(os.environ["HIDEBLITZ_UPDATE_PRIVATE_KEY"].strip())
    if len(seed) != 32:
        raise SystemExit(
            "HIDEBLITZ_UPDATE_PRIVATE_KEY must be base64 of a raw 32-byte Ed25519 seed"
        )
    signature = Ed25519PrivateKey.from_private_bytes(seed).sign(payload)
    envelope = {
        "schema": 2,
        "product": "HideBlitz",
        "keyId": KEY_ID,
        "payload": base64.b64encode(payload).decode("ascii"),
        "signature": base64.b64encode(signature).decode("ascii"),
    }
    latest_path.write_text(
        json.dumps(envelope, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"signed latest={latest_version} build={args.version} sha256={digest} "
        f"size={size} storage={storage}"
    )


if __name__ == "__main__":
    main()
