"""Render recent public RoLAC events. Uses only Python's standard library."""

from collections import Counter
from datetime import datetime, timedelta, timezone
from html import escape
import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen


USERNAME = "scakki"
ORGANIZATION = "RoLACLab"
ROOT = Path(__file__).resolve().parents[1]
LABELS = {
    "PushEvent": "Pushed code",
    "PullRequestEvent": "Pull request activity",
    "PullRequestReviewEvent": "Reviewed a pull request",
    "PullRequestReviewCommentEvent": "Commented on a review",
    "IssuesEvent": "Issue activity",
    "IssueCommentEvent": "Commented on an issue or PR",
    "CreateEvent": "Created a branch, tag, or repository",
    "ReleaseEvent": "Published a release",
}


def fetch_events():
    # The explicit /public endpoint excludes private data, even with a token.
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "scakki-profile",
               "X-GitHub-Api-Version": "2022-11-28"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    events = []
    for page in range(1, 4):  # GitHub exposes at most 300 events from the past 30 days.
        url = f"https://api.github.com/users/{USERNAME}/events/public?per_page=100&page={page}"
        with urlopen(Request(url, headers=headers), timeout=30) as response:
            batch = json.load(response)
        if not isinstance(batch, list):
            raise ValueError("Expected a list of public events")
        events.extend(batch)
        if len(batch) < 100:
            break
    return events


def select_events(events, now):
    selected = {}
    for event in events:
        repo = event.get("repo", {}).get("name", "")
        if (event.get("public") is not True
                or event.get("actor", {}).get("login", "").casefold() != USERNAME.casefold()
                or repo.split("/", 1)[0].casefold() != ORGANIZATION.casefold()
                or event.get("type") not in LABELS):
            continue
        created = datetime.fromisoformat(event["created_at"].replace("Z", "+00:00"))
        if now - timedelta(days=30) <= created <= now:
            selected[event["id"]] = {
                "type": event["type"], "repo": repo,
                "date": created.strftime("%Y-%m-%d"), "created_at": event["created_at"],
            }
    return sorted(selected.values(), key=lambda item: item["created_at"], reverse=True)


def render_svg(events, now):
    counts = Counter(event["type"] for event in events)
    title = "RoLACLab / public activity"
    subtitle = f"@{USERNAME} · Recent 30-day event window · Checked {now:%d %b %Y} UTC"
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="840" height="320" viewBox="0 0 840 320" role="img" aria-labelledby="title desc">',
        f'<title id="title">{title}</title>',
        '<desc id="desc">Recent public lab events by scakki, not a total contribution count. Private activity is excluded.</desc>',
        '<rect width="840" height="320" rx="8" fill="#2a2118"/>',
        '<g font-family="system-ui, sans-serif">',
        f'<text x="28" y="42" font-size="25" font-weight="700" fill="#f5e6d0">{title}</text>',
        f'<text x="28" y="70" font-size="15" fill="#c4a882">{subtitle}</text>',
    ]
    if events:
        metrics = [(len(events), "Public events"), (counts["PushEvent"], "Push events"),
                   (len({event["repo"] for event in events}), "Repositories")]
        for i, (value, label) in enumerate(metrics):
            x = 28 + i * 267
            lines.extend([
                f'<text x="{x}" y="117" font-size="30" font-weight="700" fill="#e8c97a">{value}</text>',
                f'<text x="{x}" y="142" font-size="15" fill="#c4a882">{label}</text>',
            ])
        for i, event in enumerate(events[:3]):
            label = f"{LABELS[event['type']]} · {event['repo'].split('/', 1)[1]}"
            if len(label) > 65:
                label = label[:62] + "…"
            y = 185 + i * 35
            lines.extend([
                f'<text x="28" y="{y}" font-size="16" fill="#f5e6d0">{escape(label)}</text>',
                f'<text x="812" y="{y}" text-anchor="end" font-size="14" fill="#c4a882">{event["date"]}</text>',
            ])
    else:
        lines.extend([
            '<text x="28" y="133" font-size="22" fill="#f5e6d0">No public lab events in the current window.</text>',
            '<text x="28" y="173" font-size="17" fill="#c4a882">Research continues beyond the public feed.</text>',
            '<text x="28" y="204" font-size="17" fill="#c4a882">Explore the lab repositories and my GitHub contribution history.</text>',
        ])
    lines.extend([
        '<text x="28" y="295" font-size="14" fill="#c4a882">Public events only · Up to 300 recent account events · Refreshed daily</text>',
        '</g></svg>\n',
    ])
    return "\n".join(lines)


def main():
    # Fetch everything before writing: network errors retain the last good card.
    now = datetime.now(timezone.utc)
    events = select_events(fetch_events(), now)
    svg = render_svg(events, now)
    destination = ROOT / "assets" / "rolac-activity.svg"
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(svg, encoding="utf-8")
    print(f"Rendered {len(events)} public {ORGANIZATION} events.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Activity update failed; existing card retained: {error}", file=sys.stderr)
        sys.exit(1)
