"""Create the GitHub repository using a Personal Access Token from env.

Usage:
    set GITHUB_TOKEN=...   (environment variable)
    python tools/upload_github.py

Steps: verify token -> get username -> create public repo.
"""
import json
import os
import sys

import requests

TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_NAME = "urban-resilience-digital-twin"
DESCRIPTION = ("Physics-guided digital twin framework for urban infrastructure "
               "resilience assessment under extreme flooding (Miyazaki City case "
               "study): terrain-informed CA flood simulation, delayed cascading "
               "failures, adaptive restoration, and reproducible experiments.")
H = {"Authorization": f"Bearer {TOKEN}",
     "Accept": "application/vnd.github+json",
     "User-Agent": "repo-upload/1.0"}


def main():
    if not TOKEN:
        print("GITHUB_TOKEN env var is required")
        sys.exit(1)

    r = requests.get("https://api.github.com/user", headers=H, timeout=30)
    if r.status_code != 200:
        print(f"token verification FAILED: HTTP {r.status_code}")
        print(r.text[:300])
        sys.exit(1)
    user = r.json()["login"]
    print(f"token OK -> GitHub user: {user}")

    r = requests.post(
        "https://api.github.com/user/repos",
        headers=H, timeout=30,
        json={"name": REPO_NAME, "private": False,
              "description": DESCRIPTION,
              "auto_init": False})
    if r.status_code == 201:
        print(f"repo created: {r.json()['html_url']}")
    elif r.status_code == 422:
        # repo may already exist; verify visibility
        print("repo already exists (422); checking access ...")
        r2 = requests.get(f"https://api.github.com/repos/{user}/{REPO_NAME}",
                          headers=H, timeout=30)
        if r2.status_code == 200:
            print(f"repo accessible: {r2.json()['html_url']} "
                  f"(private={r2.json()['private']})")
        else:
            print(f"cannot access existing repo: HTTP {r2.status_code}")
            print(r2.text[:300])
            sys.exit(1)
    else:
        print(f"repo creation FAILED: HTTP {r.status_code}")
        print(r.text[:500])
        sys.exit(1)

    print(f"PUSH_TARGET={user}/{REPO_NAME}")


if __name__ == "__main__":
    main()
