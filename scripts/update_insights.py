"""Refresh the "Latest insights" list in profile/README.md from the website's RSS feed."""
import email.utils
import pathlib
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

FEED = "https://hafezsecure.ir/en/insights/feed.xml"
README = pathlib.Path(__file__).resolve().parent.parent / "profile" / "README.md"
COUNT = 3
ATTEMPTS = 4
RETRY_SECONDS = 45
BLOCK = re.compile(r"(<!-- INSIGHTS:START -->\n).*?(<!-- INSIGHTS:END -->)", re.S)


def fetch_feed():
    # The CDN in front of the site intermittently drops connections from GitHub's
    # runners, so retry before giving up.
    req = urllib.request.Request(FEED, headers={"User-Agent": "HafezSecure-profile-updater"})
    for attempt in range(1, ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except OSError as err:
            print(f"attempt {attempt}/{ATTEMPTS} failed: {err}")
            if attempt < ATTEMPTS:
                time.sleep(RETRY_SECONDS)
    return None


def latest(body):
    root = ET.fromstring(body)
    items = []
    for item in root.iter("item"):
        title, link = item.findtext("title", "").strip(), item.findtext("link", "").strip()
        date = email.utils.parsedate_to_datetime(item.findtext("pubDate", ""))
        if title and link.startswith("https://hafezsecure.ir/"):
            items.append((date, title, link))
    items.sort(reverse=True)
    return items[:COUNT]


def main():
    body = fetch_feed()
    if body is None:
        # Keep the current list rather than fail the scheduled run every time the CDN blips.
        print("::warning::Could not reach the insights feed; the list was left unchanged.")
        return
    items = latest(body)
    if not items:
        sys.exit("feed returned no articles; leaving the README unchanged")
    lines = "".join(f"- [{t}]({l}) · {d:%d %b %Y}\n" for d, t, l in items)
    text = README.read_text(encoding="utf-8")
    if not BLOCK.search(text):
        sys.exit("insights markers not found in profile/README.md")
    README.write_text(BLOCK.sub(lambda m: m.group(1) + lines + m.group(2), text), encoding="utf-8")


if __name__ == "__main__":
    main()
