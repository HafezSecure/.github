"""Refresh the "Latest insights" list in profile/README.md from the website's RSS feed."""
import email.utils
import pathlib
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

FEED = "https://hafezsecure.ir/en/insights/feed.xml"
README = pathlib.Path(__file__).resolve().parent.parent / "profile" / "README.md"
COUNT = 3
BLOCK = re.compile(r"(<!-- INSIGHTS:START -->\n).*?(<!-- INSIGHTS:END -->)", re.S)


def latest():
    req = urllib.request.Request(FEED, headers={"User-Agent": "HafezSecure-profile-updater"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        root = ET.fromstring(resp.read())
    items = []
    for item in root.iter("item"):
        title, link = item.findtext("title", "").strip(), item.findtext("link", "").strip()
        date = email.utils.parsedate_to_datetime(item.findtext("pubDate", ""))
        if title and link.startswith("https://hafezsecure.ir/"):
            items.append((date, title, link))
    items.sort(reverse=True)
    return items[:COUNT]


def main():
    items = latest()
    if not items:
        sys.exit("feed returned no articles; leaving the README unchanged")
    lines = "".join(f"- [{t}]({l}) · {d:%d %b %Y}\n" for d, t, l in items)
    text = README.read_text(encoding="utf-8")
    if not BLOCK.search(text):
        sys.exit("insights markers not found in profile/README.md")
    README.write_text(BLOCK.sub(lambda m: m.group(1) + lines + m.group(2), text), encoding="utf-8")


if __name__ == "__main__":
    main()
