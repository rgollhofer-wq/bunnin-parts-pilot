"""Release gate for Bunnin public pages.

It verifies only facts controlled by this static publisher: exact rooftop
identity, part-number handoff, and the approved four UTM parameters. It does
not claim that Dealer.com accepted or routed a submitted lead.
"""
from __future__ import annotations

import gzip
import base64
from html import unescape
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from build import OUT, ROOFS, request_url

ROOT = Path(__file__).parent

def records():
    return json.loads(gzip.decompress(base64.b64decode((ROOT / "public_release.gz.b64").read_text())).decode())

def main():
    rows = records()
    assert len(rows) == 3485, f"unexpected record count: {len(rows)}"
    expected = {"utm_source": "localparts", "utm_medium": "organic_inventory", "utm_campaign": "bunnin_exact_part_pilot"}
    for part, _description, roof in rows:
        assert roof in ROOFS, f"unknown rooftop: {roof}"
        page = OUT / "parts" / "gm" / part / ROOFS[roof]["slug"] / "index.html"
        html = page.read_text(encoding="utf-8")
        assert ROOFS[roof]["phone"] in html
        assert ROOFS[roof]["address"] in html
        url = request_url(part, roof)
        query = parse_qs(urlparse(url).query)
        assert url in unescape(html)
        assert query.get("partNumber1") == [part]
        for key, value in expected.items():
            assert query.get(key) == [value]
        assert query.get("utm_content") == [ROOFS[roof]["slug"]]
    home = (OUT / "index.html").read_text(encoding="utf-8")
    assert "Bunnin Chevrolet Parts" in home
    for roof in ROOFS:
        dealer = ROOFS[roof]
        request = OUT / "request" / dealer["slug"] / "index.html"
        request_html = request.read_text(encoding="utf-8")
        assert 'action="https://formsubmit.co/ric@localparts.shop"' in request_html
        assert dealer["lead"] in request_html
    assert request_url(None, "Fillmore") in home
    assert request_url(None, "Santa Paula") in home
    print(f"PASS: {len(rows)} rooftop pages; all routed request and UTM handoffs valid")

if __name__ == "__main__":
    main()
