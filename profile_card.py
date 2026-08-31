#!/usr/bin/env python3
"""Generate Sai Pavan's light and dark GitHub profile cards from public data."""

from __future__ import annotations

import argparse
import html
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


USERNAME = "saipavan2702"
API = "https://api.github.com"
ROOT = Path(__file__).resolve().parent

THEMES = {
    "dark": {
        "background": "#11151c",
        "panel": "#181c25",
        "border": "#303645",
        "text": "#cdd6f4",
        "muted": "#7f849c",
        "key": "#89b4fa",
        "value": "#a6e3a1",
        "accent": "#f9e2af",
        "prompt": "#cba6f7",
    },
    "light": {
        "background": "#eff1f5",
        "panel": "#e6e9ef",
        "border": "#ccd0da",
        "text": "#4c4f69",
        "muted": "#8c8fa1",
        "key": "#1e66f5",
        "value": "#40a02b",
        "accent": "#df8e1d",
        "prompt": "#8839ef",
    },
}

FALLBACK = {
    "public_repos": 42,
    "followers": "syncing",
    "following": "syncing",
    "stars": "syncing",
    "joined": "GitHub",
}


def github_json(path: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-profile-card",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"{API}{path}", headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_stats() -> dict[str, int | str]:
    user = github_json(f"/users/{USERNAME}")
    repos = []
    page = 1
    while True:
        batch = github_json(
            f"/users/{USERNAME}/repos?type=owner&sort=updated&per_page=100&page={page}"
        )
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    return {
        "public_repos": user["public_repos"],
        "followers": user["followers"],
        "following": user["following"],
        "stars": sum(repo["stargazers_count"] for repo in repos if not repo["fork"]),
        "joined": user["created_at"][:4],
    }


def line(y: int, key: str, value: str, theme: dict[str, str]) -> str:
    return (
        f'<text x="510" y="{y}" class="row">'
        f'<tspan fill="{theme["key"]}">{html.escape(key)}</tspan>'
        f'<tspan fill="{theme["muted"]}">: </tspan>'
        f'<tspan fill="{theme["value"]}">{html.escape(value)}</tspan>'
        "</text>"
    )


def render(theme_name: str, stats: dict[str, int | str]) -> str:
    theme = THEMES[theme_name]
    rows = [
        (130, "Role", "Software Engineer"),
        (158, "Based", "India"),
        (186, "Frontend", "React · TypeScript · Tailwind"),
        (214, "Backend", "Node.js · Go · Java · Python"),
        (242, "Tools", "Shell · Neovim · VS Code"),
        (270, "Hobbies", "Anime · Gym · Building things"),
        (326, "Public repos", str(stats["public_repos"])),
        (354, "Followers", str(stats["followers"])),
        (382, "Stars earned", str(stats["stars"])),
        (410, "On GitHub since", str(stats["joined"])),
    ]
    row_svg = "\n    ".join(line(y, key, value, theme) for y, key, value in rows)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="980" height="500" viewBox="0 0 980 500" role="img" aria-labelledby="title desc">
  <title id="title">Sai Pavan's GitHub profile</title>
  <desc id="desc">A terminal-inspired profile card showing Sai Pavan's stack, interests, and public GitHub statistics.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{theme["background"]}"/>
      <stop offset="1" stop-color="{theme["panel"]}"/>
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity=".12"/>
    </filter>
  </defs>
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }}
    .row {{ font: 15px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }}
  </style>
  <rect x="18" y="18" width="944" height="464" rx="22" fill="url(#bg)" stroke="{theme["border"]}" filter="url(#shadow)"/>
  <circle cx="52" cy="48" r="6" fill="#f38ba8"/>
  <circle cx="72" cy="48" r="6" fill="#f9e2af"/>
  <circle cx="92" cy="48" r="6" fill="#a6e3a1"/>
  <text x="490" y="54" text-anchor="middle" class="mono" font-size="12" fill="{theme["muted"]}">~/saipavan2702/profile</text>
  <line x1="468" y1="82" x2="468" y2="446" stroke="{theme["border"]}"/>

  <g class="mono">
    <text x="64" y="120" font-size="18" font-weight="700" fill="{theme["prompt"]}">sai@github</text>
    <text x="64" y="146" font-size="14" fill="{theme["muted"]}">$ whoami</text>
    <text x="64" y="210" font-size="50" font-weight="800" letter-spacing="5" fill="{theme["key"]}">SAI</text>
    <text x="64" y="266" font-size="50" font-weight="800" letter-spacing="5" fill="{theme["value"]}">PAVAN</text>
    <path d="M65 287 H386" stroke="{theme["border"]}" stroke-width="2"/>
    <text x="64" y="326" font-size="14" fill="{theme["accent"]}">build · learn · repeat</text>
    <text x="64" y="356" font-size="14" fill="{theme["muted"]}">One Piece enthusiast</text>
    <text x="64" y="414" font-size="14" fill="{theme["prompt"]}">❯</text>
    <rect x="83" y="400" width="9" height="17" rx="1" fill="{theme["text"]}" opacity=".8"/>
  </g>

  <text x="510" y="102" class="mono" font-size="18" font-weight="700" fill="{theme["text"]}">profile</text>
  {row_svg}
  <text x="510" y="298" class="mono" font-size="18" font-weight="700" fill="{theme["text"]}">github.public</text>
  <text x="510" y="446" class="mono" font-size="12" fill="{theme["muted"]}">public data · refreshed daily by GitHub Actions</text>
</svg>
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--offline",
        action="store_true",
        help="generate with safe placeholders instead of calling the GitHub API",
    )
    args = parser.parse_args()

    stats = FALLBACK
    if not args.offline:
        try:
            stats = fetch_stats()
        except (HTTPError, URLError, TimeoutError, KeyError, TypeError) as error:
            raise SystemExit(f"Could not fetch GitHub data: {error}") from error

    for theme_name in THEMES:
        (ROOT / f"profile-{theme_name}.svg").write_text(
            render(theme_name, stats), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
