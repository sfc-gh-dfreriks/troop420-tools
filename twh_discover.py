"""Discover every export available to your TroopWebHost login (read-only).

Logs in via a visible window (you sign in), then breadth-first crawls the
logged-in app's menu pages, collecting every link to an .aspx page. For each
"Open in Excel"-style export URL (ReportFormat=XLS) it fetches the export and
records ONLY metadata: HTTP status, content type, column names, row count.
No row contents are written or printed.

Never submits forms or follows anything that looks like an action
(delete/save/update/logout/email/send). GET only.

Output: exports/_catalog.json and exports/_catalog.md
"""
import csv
import io
import json
import re
import sys
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs

from playwright.sync_api import sync_playwright

ROOT = "https://www.troopwebhost.org/"
HOME = ROOT + "Troop420Bothell/Index.htm"
HERE = Path(__file__).resolve().parent
OUT = HERE / "exports"
PROFILE = HERE / ".browser-profile"
MAX_PAGES = 400
# Link text / URL fragments we refuse to follow, to stay strictly read-only.
UNSAFE = re.compile(r"delete|remove|logout|logoff|signout|save|update|submit|send|email|mail|approve|"
                    r"post|upload|import|purge|reset|password|pay|charge|refund|void", re.I)

LINK_JS = """() => {
  const out = [];
  const grab = (el, raw) => {
    if (!raw) return;
    const m = raw.match(/['"]([^'"]*\\.aspx[^'"]*)['"]/i);
    const u = m ? m[1] : (/\\.aspx/i.test(raw) ? raw : null);
    if (u) out.push({u, t: (el.innerText || el.title || el.value || '').trim().slice(0, 120)});
  };
  document.querySelectorAll('a,[onclick],option,frame,iframe').forEach(el => {
    grab(el, el.getAttribute('href')); grab(el, el.getAttribute('onclick'));
    grab(el, el.getAttribute('src')); grab(el, el.getAttribute('value'));
  });
  return {title: document.title, h: (document.querySelector('h1,h2,.PageTitle,#PageTitle')||{}).innerText||'', links: out};
}"""


def norm(u, base):
    full = urljoin(base, u.replace("&amp;", "&"))
    p = urlparse(full)
    if p.netloc.lower().replace("www.", "") != "troopwebhost.org":
        return None
    return f"{ROOT}{p.path.lstrip('/')}" + (f"?{p.query}" if p.query else "")


def key(u):
    p = urlparse(u); q = parse_qs(p.query)
    keep = {k: q[k][0] for k in sorted(q) if k in ("Menu_Item_ID", "Form_ID", "Custom_Form_ID", "ReportFormat", "Report_ID", "ID")}
    return p.path.lower() + "|" + json.dumps(keep, sort_keys=True)


def is_export(u):
    return "reportformat=" in u.lower()


def logged_in(page):
    r = page.request.get(ROOT + "FormReport.aspx?Menu_Item_ID=46093&Stack=1&ReportFormat=XLS",
                         max_redirects=0, fail_on_status_code=False)
    return r.status == 200


def main():
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(str(PROFILE), headless=False)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(HOME)
        print("Log in to TroopWebHost in the browser window (waiting up to 5 min)...", flush=True)
        for _ in range(100):
            if logged_in(page):
                break
            page.wait_for_timeout(3000)
        else:
            print("Login not detected; aborting."); ctx.close(); return 1
        print("Logged in. Crawling menus...", flush=True)

        # Seed: whatever pages the logged-in frameset is showing.
        page.goto(HOME); page.wait_for_timeout(3000)
        seeds = [f.url for f in page.frames if ".aspx" in f.url.lower()]
        queue = deque((s, "(start)", "") for s in seeds)
        seen, pages, exports = set(), [], {}
        crawl = ctx.new_page()

        while queue and len(pages) < MAX_PAGES:
            url, label, parent = queue.popleft()
            k = key(url)
            if k in seen:
                continue
            seen.add(k)
            if is_export(url):
                exports[k] = {"url": url, "label": label, "found_on": parent}
                continue
            if UNSAFE.search(label) or UNSAFE.search(urlparse(url).path):
                continue
            try:
                resp = crawl.goto(url, wait_until="domcontentloaded", timeout=30000)
            except Exception as e:  # noqa: BLE001
                pages.append({"url": url, "label": label, "error": str(e)[:120]}); continue
            if resp is None or resp.status != 200 or "troopwebhost.com/index" in crawl.url.lower():
                pages.append({"url": url, "label": label, "status": resp.status if resp else None, "redirected": crawl.url})
                continue
            info = crawl.evaluate(LINK_JS)
            for fr in crawl.frames[1:]:
                try: info["links"] += fr.evaluate(LINK_JS)["links"]
                except Exception: pass  # noqa: BLE001,E701
            pages.append({"url": url, "label": label, "title": info["title"], "heading": info["h"][:120],
                          "links": len(info["links"])})
            print(f"  [{len(pages):3}] {label[:50]:50} {urlparse(url).path}", flush=True)
            for l in info["links"]:
                n = norm(l["u"], crawl.url)
                if n and key(n) not in seen:
                    queue.append((n, l["t"] or label, url))

        print(f"Crawled {len(pages)} pages; probing {len(exports)} exports (metadata only)...", flush=True)
        for e in exports.values():
            r = crawl.request.get(e["url"], max_redirects=0, fail_on_status_code=False)
            e["status"], e["content_type"] = r.status, r.headers.get("content-type", "")
            body = r.body()
            text = body.decode("utf-8-sig", errors="replace") if r.status == 200 else ""
            if text and not text.lstrip()[:20].lower().startswith(("<!doc", "<htm")):
                rows = list(csv.reader(io.StringIO(text)))
                e["columns"] = rows[0] if rows else []
                e["rows"] = max(len(rows) - 1, 0)
            else:
                e["columns"], e["rows"] = None, None
            e["bytes"] = len(body)
        ctx.close()

    exp = sorted(exports.values(), key=lambda e: (e["status"] != 200, e["label"].lower()))
    (OUT / "_catalog.json").write_text(json.dumps({"pages": pages, "exports": exp}, indent=2))
    md = ["# TroopWebHost export catalog (Troop 420 Bothell)", "",
          f"Pages crawled: {len(pages)}. Export links found: {len(exp)}.", "",
          "| Menu_Item_ID | Label | Status | Rows | Columns |", "|---|---|---|---|---|"]
    for e in exp:
        mid = parse_qs(urlparse(e["url"]).query).get("Menu_Item_ID", ["?"])[0]
        cols = ", ".join(e["columns"] or [])[:300]
        md.append(f"| {mid} | {e['label'].replace('|', '/')} | {e['status']} | {e['rows'] if e['rows'] is not None else '-'} | {cols.replace('|', '/')} |")
    (OUT / "_catalog.md").write_text("\n".join(md) + "\n")
    print(f"Wrote {OUT/'_catalog.md'} and _catalog.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
