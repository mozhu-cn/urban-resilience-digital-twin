"""Download portable Git for Windows (self-extracting 7z) into tools/vendor."""
import os
import subprocess
import sys

import requests

VENDOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor")
DEST = os.path.join(VENDOR, "git")
os.makedirs(DEST, exist_ok=True)

HEADERS = {"User-Agent": "git-vendor/1.0"}


def download(url, dest_path, size_hint=0):
    for attempt in range(5):
        try:
            with requests.get(url, timeout=60, headers=HEADERS, stream=True) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", size_hint))
                done = 0
                with open(dest_path, "wb") as fh:
                    for chunk in r.iter_content(chunk_size=1 << 16):
                        fh.write(chunk)
                        done += len(chunk)
                if total and done < total:
                    raise IOError(f"short read {done}/{total}")
                return
        except Exception as exc:  # noqa: BLE001
            print(f"  attempt {attempt+1} failed: {type(exc).__name__}: {str(exc)[:80]}", flush=True)
    raise RuntimeError("download failed after retries")


def main():
    # resolve latest Git for Windows release
    r = requests.get("https://api.github.com/repos/git-for-windows/git/releases/latest",
                     timeout=30, headers=HEADERS)
    r.raise_for_status()
    tag = r.json()["tag_name"]
    print("latest release:", tag)

    asset_url = None
    asset_name = None
    for a in r.json()["assets"]:
        name = a["name"]
        if name.startswith("PortableGit-") and name.endswith("-64-bit.7z.exe"):
            asset_url = a["browser_download_url"]
            asset_name = name
            break
    if not asset_url:
        print("PortableGit asset not found; assets:", [a["name"] for a in r.json()["assets"]][:10])
        sys.exit(1)

    local = os.path.join(VENDOR, asset_name)
    print(f"downloading {asset_name} ...")
    download(asset_url, local)
    print(f"downloaded {os.path.getsize(local)/1e6:.1f} MB -> {local}")

    # self-extracting 7z: extract to DEST silently
    print("extracting ...")
    proc = subprocess.run([local, f"-o{DEST}", "-y"], capture_output=True, text=True)
    if proc.returncode != 0:
        print("extract stderr:", proc.stderr[:500])
        sys.exit(1)
    os.remove(local)

    git_exe = os.path.join(DEST, "cmd", "git.exe")
    print("git ready at:", git_exe, "| exists:", os.path.exists(git_exe))


if __name__ == "__main__":
    main()
