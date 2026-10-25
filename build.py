"""Build the public Bunnin Parts pilot from its customer-safe release file."""
from __future__ import annotations
from html import escape
import base64
import gzip
import json
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).parent
OUT = ROOT / "dist"
BASE = "https://rgollhofer-wq.github.io/bunnin-parts-pilot"
STAMP = "October 21, 2026 at 11:57 AM PDT"
ROOFS = {
    "Fillmore": {"slug": "bunnin-fillmore", "name": "Bunnin Chevrolet of Fillmore", "domain": "https://www.bunninchevroletoffillmore.com", "lead": "leads@bunninfillmorechevrolet.com", "phone": "(805) 225-6905", "address": "1024 Ventura St, Fillmore, CA 93015", "logo": "https://pictures.dealer.com/b/bunninchevroletoffillmore/1234/5516bae1ec8c467c9c4e8bb4530ca53d.jpg?impolicy=downsize&h=160"},
    "Santa Paula": {"slug": "bunnin-santa-paula", "name": "Bunnin Chevrolet of Santa Paula", "domain": "https://www.bunninchevroletofsantapaula.com", "lead": "leads@bunninsantapaulachevrolet.com", "phone": "(805) 623-0038", "address": "101 W Harvard Blvd, Santa Paula, CA 93060", "logo": "https://pictures.dealer.com/b/bunninchevroletofsantapaula/1403/eaf0e1c1f9fa8a13206845aa7e253b0fx.jpg?impolicy=downsize&h=160"},
}

def request_url(part, roof):
    source = ROOFS[roof]
    params = {"utm_source": "localparts", "utm_medium": "organic_inventory", "utm_campaign": "bunnin_exact_part_pilot", "utm_content": source["slug"]}
    if part:
        params["partNumber1"] = part
    return f"/bunnin-parts-pilot/request/{source['slug']}/?" + urlencode(params)

def header(roof):
    dealer = ROOFS[roof]
    return f'''<div class="top"><span>Sales: {dealer["phone"]}</span><span>{escape(dealer["address"])}</span></div><header><a class="brand" href="{dealer["domain"]}"><span class="chevy">CHEVROLET</span><img src="{dealer["logo"]}" alt="{escape(dealer["name"])}"></a><nav><a href="{dealer["domain"]}">Home</a><a href="{dealer["domain"]}/new-inventory/index.htm">New</a><a href="{dealer["domain"]}/used-inventory/index.htm">Pre-Owned</a><a href="{dealer["domain"]}/ServiceAndPartsSpecials.htm">Service &amp; Parts</a><a href="/bunnin-parts-pilot/">Parts Center</a></nav></header>'''

def footer(roof):
    dealer = ROOFS[roof]
    return f'''<footer><div><strong>{escape(dealer["name"])}</strong><a href="{dealer["domain"]}/contact.htm">Contact</a><a href="{dealer["domain"]}/dealership/about.htm">About</a><a href="{dealer["domain"]}/privacy.htm">Privacy</a></div><p>{escape(dealer["address"])} · {dealer["phone"]}</p></footer>'''

def group_header():
    return '''<div class="top"><span>Bunnin Chevrolet Parts</span><span>Fillmore &amp; Santa Paula</span></div><header><a class="brand" href="/bunnin-parts-pilot/"><span class="chevy">CHEVROLET</span><span class="group-name">Bunnin Chevrolet Parts</span></a><nav><a href="/bunnin-parts-pilot/">Parts Center</a><a href="https://www.bunninchevroletoffillmore.com/">Fillmore</a><a href="https://www.bunninchevroletofsantapaula.com/">Santa Paula</a></nav></header>'''

def group_footer():
    return '''<footer><div><strong>Bunnin Chevrolet Parts</strong><a href="https://www.bunninchevroletoffillmore.com/contact.htm">Fillmore Contact</a><a href="https://www.bunninchevroletofsantapaula.com/contact.htm">Santa Paula Contact</a></div><p><strong>Fillmore:</strong> (805) 225-6905 · 1024 Ventura St, Fillmore, CA 93015<br><strong>Santa Paula:</strong> (805) 623-0038 · 101 W Harvard Blvd, Santa Paula, CA 93060</p><p>Choose a Bunnin rooftop to request parts information.</p></footer>'''

def page(title, body, roof, robots="index,follow"):
    site_header, site_footer = (group_header(), group_footer()) if roof is None else (header(roof), footer(roof))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><meta name="robots" content="{robots}"><link rel="stylesheet" href="/bunnin-parts-pilot/pilot.css"></head><body>{site_header}<main>{body}</main>{site_footer}</body></html>'''

def save(path, content):
    target = OUT / path / "index.html" if path else OUT / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

def request_page(roof):
    dealer = ROOFS[roof]
    return f'''<section class="hero compact"><p>PARTS &amp; SERVICE</p><h1>Request parts information</h1><p>Send your request to {escape(dealer["name"])}. A Bunnin parts professional will confirm fitment, availability, price, and next steps.</p><form class="request-form" action="https://formsubmit.co/ric@localparts.shop" method="POST"><input type="hidden" name="_cc" value="{dealer["lead"]}"><input type="hidden" name="_subject" value="Bunnin {roof} parts request"><input type="hidden" name="_next" value="{BASE}/request/{dealer["slug"]}/thanks/"><input type="hidden" name="_template" value="table"><input type="hidden" name="rooftop" value="{escape(dealer["name"], quote=True)}"><input type="hidden" name="utm_source" value="localparts"><input type="hidden" name="utm_medium" value="organic_inventory"><input type="hidden" name="utm_campaign" value="bunnin_exact_part_pilot"><input type="hidden" name="utm_content" value="{dealer["slug"]}"><input class="trap" type="text" name="_honey" tabindex="-1" autocomplete="off"><label>Your name<input name="name" autocomplete="name" required></label><label>Email address<input type="email" name="email" autocomplete="email" required></label><label>Phone number<input type="tel" name="phone" autocomplete="tel"></label><label>Vehicle (year, make, model)<input name="vehicle" placeholder="Example: 2022 Chevrolet Silverado 1500"></label><label>GM part number<input id="part-number" name="part_number" maxlength="80"></label><label>What do you need?<textarea name="request" rows="4" required></textarea></label><button type="submit">Send request</button></form><p class="subtle">Submitting a request does not create an order. Bunnin confirms all details before any commitment.</p></section><script>const q=new URLSearchParams(location.search);document.querySelector("#part-number").value=q.get("partNumber1")||"";for(const k of ["utm_source","utm_medium","utm_campaign","utm_content"]){{const i=document.querySelector(`[name="${{k}}"]`);if(q.get(k)&&i)i.value=q.get(k)}};</script>'''

def thanks_page(roof):
    dealer = ROOFS[roof]
    return f'''<section class="hero compact"><p>PARTS &amp; SERVICE</p><h1>Request sent</h1><p>{escape(dealer["name"])} has received your request. A Bunnin parts professional will follow up to confirm fitment, availability, price, and next steps.</p><p><a class="button" href="/bunnin-parts-pilot/">Return to parts center</a></p></section>'''

def main():
    records = json.loads(gzip.decompress(base64.b64decode((ROOT / "public_release.gz.b64").read_text())).decode())
    OUT.mkdir(exist_ok=True)
    actions = "".join(f'<a class="button" href="{request_url(None, roof)}">Request Parts — {roof}</a>' for roof in ROOFS)
    home = f'''<section class="hero"><p>GENUINE GM PARTS</p><h1>What do you need for your Chevrolet?</h1><p>Tell us what you are looking for and include your vehicle information. A Bunnin parts professional will confirm fitment, availability, price, and next steps.</p><div class="actions">{actions}</div><p class="subtle">Already have a GM part number? <a href="/bunnin-parts-pilot/search/">Search by part number</a>.</p></section><section class="notice"><h2>Genuine parts. Your Bunnin parts team.</h2><p>Inventory was last observed {STAMP}. It is not live availability. Bunnin confirms fitment, availability, price, and next steps before any commitment.</p></section>'''
    save("", page("Genuine GM Parts | Bunnin Chevrolet", home, None))
    js_records = json.dumps(records, separators=(",", ":"))
    search = f'''<section class="hero compact"><p>PARTS &amp; SERVICE</p><h1>Search by GM part number</h1><p>Already have a part number? Search it here. The Bunnin parts team will confirm the details with you.</p><form id="search"><label for="part">GM part number</label><input id="part" maxlength="80" placeholder="Enter part number"><button>Search</button></form><p id="status" role="status"></p><ul id="results"></ul></section><script>const data={js_records};const forms={{"Fillmore":"{BASE}/request/bunnin-fillmore/","Santa Paula":"{BASE}/request/bunnin-santa-paula/"}};const slugs={{"Fillmore":"bunnin-fillmore","Santa Paula":"bunnin-santa-paula"}};document.querySelector("#search").addEventListener("submit",e=>{{e.preventDefault();const q=part.value.trim(),m=data.filter(x=>x[0]===q);results.innerHTML="";m.forEach(x=>{{const a=document.createElement("a"),li=document.createElement("li"),u=new URL(forms[x[2]]);u.search=new URLSearchParams({{partNumber1:x[0],utm_source:"localparts",utm_medium:"organic_inventory",utm_campaign:"bunnin_exact_part_pilot",utm_content:slugs[x[2]]}});a.href=u;a.textContent="Request "+x[0]+" — Bunnin "+x[2];li.append(a);results.append(li)}});status.textContent=m.length?"Inventory observed—confirm with Bunnin.":"No exact observed part match."}});</script>'''
    save("search", page("Search GM Parts | Bunnin Chevrolet", search, None, "noindex,follow"))
    urls = [BASE + "/"]
    for roof in ROOFS:
        dealer = ROOFS[roof]
        save(f"request/{dealer["slug"]}", page(f"Request Parts | {dealer["name"]}", request_page(roof), roof, "noindex,nofollow"))
        save(f"request/{dealer["slug"]}/thanks", page(f"Request Sent | {dealer["name"]}", thanks_page(roof), roof, "noindex,nofollow"))
    for part, description, roof in records:
        dealer = ROOFS[roof]
        path = f"parts/gm/{part}/{dealer["slug"]}"
        body = f'''<section class="hero compact"><p>PARTS &amp; SERVICE</p><h1>{escape(description.title() or "Genuine GM Part")}</h1><p class="partno">GM Part {escape(part)}</p><p>Request information from {escape(dealer["name"])}. Your Bunnin parts professional will confirm availability, fitment, price, and next steps.</p><p><a class="button" href="{escape(request_url(part, roof), quote=True)}">Request parts information</a></p><p class="subtle">Submitting a request does not create an order.</p></section><section class="notice"><p>Inventory observed {STAMP}; not live availability. Confirm fitment with your VIN or vehicle details.</p></section>'''
        save(path, page(f"{description.title() or "GM Part"} {part} | {dealer["name"]}", body, roof))
        urls.append(BASE + "/" + path + "/")
    (OUT / "pilot.css").write_text((ROOT / "pilot.css").read_text(), encoding="utf-8")
    (OUT / ".nojekyll").touch()
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{url}</loc></url>" for url in urls) + "</urlset>")
    (OUT / "404.html").write_text("<!doctype html><title>Page unavailable</title><h1>Inventory record unavailable</h1><p>This observation may have been replaced or withdrawn. Confirm with Bunnin.</p>")
    print(f"Built {len(records)} public part pages")

if __name__ == "__main__":
    main()
