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
    "Fillmore": {"slug":"bunnin-fillmore","name":"Bunnin Chevrolet of Fillmore","domain":"https://www.bunninchevroletoffillmore.com","form":"https://www.bunninchevroletoffillmore.com/PartsOrderForm.htm","phone":"(805) 225-6905","address":"1024 Ventura St, Fillmore, CA 93015","logo":"https://pictures.dealer.com/b/bunninchevroletoffillmore/1234/5516bae1ec8c467c9c4e8bb4530ca53d.jpg?impolicy=downsize&h=160"},
    "Santa Paula": {"slug":"bunnin-santa-paula","name":"Bunnin Chevrolet of Santa Paula","domain":"https://www.bunninchevroletofsantapaula.com","form":"https://www.bunninchevroletofsantapaula.com/PartsOrderForm.htm","phone":"(805) 623-0038","address":"101 W Harvard Blvd, Santa Paula, CA 93060","logo":"https://pictures.dealer.com/b/bunninchevroletofsantapaula/1403/eaf0e1c1f9fa8a13206845aa7e253b0fx.jpg?impolicy=downsize&h=160"},
}
def handoff(part, roof):
    source = ROOFS[roof]
    parameters = {"utm_source":"localparts","utm_medium":"organic_inventory","utm_campaign":"bunnin_exact_part_pilot","utm_content":source["slug"]}
    if part: parameters["partNumber1"] = part
    return source["form"] + "?" + urlencode(parameters)
def header(roof):
    dealer = ROOFS[roof]
    return f'''<div class="top"><span>Sales: {dealer["phone"]}</span><span>{escape(dealer["address"])}</span></div><header><a class="brand" href="{dealer["domain"]}"><span class="chevy">CHEVROLET</span><img src="{dealer["logo"]}" alt="{escape(dealer["name"])}"></a><nav><a href="{dealer["domain"]}">Home</a><a href="{dealer["domain"]}/new-inventory/index.htm">New</a><a href="{dealer["domain"]}/used-inventory/index.htm">Pre-Owned</a><a href="{dealer["domain"]}/ServiceAndPartsSpecials.htm">Service &amp; Parts</a><a href="/">Parts Center</a></nav></header>'''
def footer(roof):
    dealer = ROOFS[roof]
    return f'''<footer><div><strong>{escape(dealer["name"])}</strong><a href="{dealer["domain"]}/contact.htm">Contact</a><a href="{dealer["domain"]}/dealership/about.htm">About</a><a href="{dealer["domain"]}/privacy.htm">Privacy</a></div><p>{escape(dealer["address"])} · {dealer["phone"]}</p></footer>'''
def page(title, body, roof, robots="index,follow"):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><meta name="robots" content="{robots}"><link rel="stylesheet" href="/pilot.css"></head><body>{header(roof)}<main>{body}</main>{footer(roof)}</body></html>'''
def save(path, content):
    target = OUT / path / "index.html" if path else OUT / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
def main():
    records = json.loads(gzip.decompress(base64.b64decode((ROOT / "public_release.gz.b64").read_text())).decode())
    OUT.mkdir(exist_ok=True)
    actions = "".join(f'<a class="button" href="{handoff(None, roof)}">Request Parts — {roof}</a>' for roof in ROOFS)
    home = f'''<section class="hero"><p>GENUINE GM PARTS</p><h1>What do you need for your Chevrolet?</h1><p>Tell us what you are looking for and include your vehicle information. A Bunnin parts professional will confirm fitment, availability, price, and next steps.</p><div class="actions">{actions}</div><p class="subtle">Already have a GM part number? <a href="/search/">Search by part number</a>.</p></section><section class="notice"><h2>Genuine parts. Your Bunnin parts team.</h2><p>Inventory was last observed {STAMP}. It is not live availability. Bunnin confirms fitment, availability, price, and next steps before any commitment.</p></section>'''
    save("", page("Genuine GM Parts | Bunnin Chevrolet", home, "Fillmore"))
    js_records = json.dumps(records, separators=(",", ":"))
    search = f'''<section class="hero compact"><p>PARTS &amp; SERVICE</p><h1>Search by GM part number</h1><p>Already have a part number? Search it here. The Bunnin parts team will confirm the details with you.</p><form id="search"><label for="part">GM part number</label><input id="part" maxlength="80" placeholder="Enter part number"><button>Search</button></form><p id="status" role="status"></p><ul id="results"></ul></section><script>const data={js_records};const forms={{"Fillmore":"{ROOFS['Fillmore']['form']}","Santa Paula":"{ROOFS['Santa Paula']['form']}"}};const slugs={{"Fillmore":"bunnin-fillmore","Santa Paula":"bunnin-santa-paula"}};document.querySelector('#search').addEventListener('submit',e=>{{e.preventDefault();const q=part.value.trim(),m=data.filter(x=>x[0]===q);results.innerHTML='';m.forEach(x=>{{const a=document.createElement('a'),li=document.createElement('li'),u=new URL(forms[x[2]]);u.search=new URLSearchParams({{partNumber1:x[0],utm_source:'localparts',utm_medium:'organic_inventory',utm_campaign:'bunnin_exact_part_pilot',utm_content:slugs[x[2]]}});a.href=u;a.textContent='Request '+x[0]+' — Bunnin '+x[2];li.append(a);results.append(li)}});status.textContent=m.length?'Inventory observed—confirm with Bunnin.':'No exact observed part match.'}});</script>'''
    save("search", page("Search GM Parts | Bunnin Chevrolet", search, "Fillmore", "noindex,follow"))
    urls = [BASE + "/"]
    for part, description, roof in records:
        dealer = ROOFS[roof]
        path = f"parts/gm/{part}/{dealer['slug']}"
        body = f'''<section class="hero compact"><p>PARTS &amp; SERVICE</p><h1>{escape(description.title() or 'Genuine GM Part')}</h1><p class="partno">GM Part {escape(part)}</p><p>Request information from {escape(dealer['name'])}. Your Bunnin parts professional will confirm availability, fitment, price, and next steps.</p><p><a class="button" href="{escape(handoff(part, roof), quote=True)}">Request parts information</a></p><p class="subtle">You will continue to Bunnin’s parts request form. Submitting a request does not create an order.</p></section><section class="notice"><p>Inventory observed {STAMP}; not live availability. Confirm fitment with your VIN or vehicle details.</p></section>'''
        save(path, page(f"{description.title() or 'GM Part'} {part} | {dealer['name']}", body, roof))
        urls.append(BASE + "/" + path + "/")
    (OUT / "pilot.css").write_text((ROOT / "pilot.css").read_text(), encoding="utf-8")
    (OUT / ".nojekyll").touch()
    (OUT / "robots.txt").write_text(f"User-agent: *
Allow: /
Sitemap: {BASE}/sitemap.xml
")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f"<url><loc>{url}</loc></url>" for url in urls) + "</urlset>")
    (OUT / "404.html").write_text("<!doctype html><title>Page unavailable</title><h1>Inventory record unavailable</h1><p>This observation may have been replaced or withdrawn. Confirm with Bunnin.</p>")
    print(f"Built {len(records)} public part pages")
if __name__ == "__main__": main()
