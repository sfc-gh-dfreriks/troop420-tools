"""Read-only export of TroopWebHost reports using your own logged-in session.

TroopWebHost has no published API. Every report with an "Open in Excel" link
can be fetched as CSV from
    https://www.troopwebhost.org/FormReport.aspx?Menu_Item_ID=<id>&Stack=1&ReportFormat=XLS
once a browser session is logged in. This drives a local Chromium (Playwright)
so YOU log in; the script never sees or stores a password.

CLI:
    python3 twh_export.py --login 46093 46012        # opens a window, waits for login
    python3 twh_export.py 46093                      # headless, reuses a still-valid session
    options: --troop Troop420Bothell  --out ./exports  --profile ./.browser-profile

Library:
    from twh_export import export_reports
    results = export_reports(["46093"], out_dir="exports", login=True)
    # -> [{"menu_id": "46093", "path": Path, "header": [...], "rows": 177}, ...]

Exit codes: 0 ok, 1 login timed out / no access, 2 session expired (rerun with --login).
"""
import argparse
import csv
import io
import sys
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = "https://www.troopwebhost.org/"
DEFAULT_TROOP = "Troop420Bothell"
LOGIN_TIMEOUT_S = 300
# Named report bundles. volunteer-points feeds the Troop 420 Adult Volunteer Points tracker
# (troop420-volunteer-points): positions -> post credit, event leaders -> event-lead credit.
PRESETS = {"volunteer-points": ["54040", "53104", "45935"]}


class SessionExpired(Exception):
    """Headless run found no valid session; rerun with login=True."""


class LoginTimeout(Exception):
    """Login did not complete, or this login lacks the role for the report."""


def report_url(menu_id: str) -> str:
    # The .aspx app is served from the site root, not /<Troop>/; the session
    # cookies select the troop.
    return f"{ROOT}FormReport.aspx?Menu_Item_ID={menu_id}&Stack=1&ReportFormat=XLS"


def _fetch(page, menu_id: str):
    # max_redirects=0: an unauthenticated request 302s to the TroopWebHost home
    # page, which would otherwise look like a 200 HTML page.
    resp = page.request.get(report_url(menu_id), max_redirects=0, fail_on_status_code=False, timeout=180_000)  # big exports (e.g. 45935) exceed 30s
    # Exports start with a UTF-8 BOM; strip it so the first header is clean.
    return resp.status, resp.headers.get("location", ""), resp.body().decode("utf-8-sig", errors="replace")


def _is_csv(status: int, text: str) -> bool:
    head = text.lstrip()[:200].lower()
    return status == 200 and not head.startswith(("<!doctype", "<html")) and ("," in head or "\t" in head)


def export_reports(menu_ids, out_dir="exports", troop=DEFAULT_TROOP, profile=".browser-profile",
                   login=False, timeout_s=LOGIN_TIMEOUT_S, log=print):
    """Download each report as CSV. Returns one dict per report saved."""
    out_dir, profile = Path(out_dir), Path(profile)
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(str(profile), headless=not login)
        try:
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            # The troop entry page is only a frameset with the login form
            # (reCAPTCHA, so it must be a human). Only load it when signing in;
            # reloading it on an existing session appears to reset the context.
            if login:
                page.goto(f"{ROOT}{troop}/Index.htm")

            first = menu_ids[0]
            status, loc, text = _fetch(page, first)
            if not _is_csv(status, text):
                if not login:
                    raise SessionExpired("Saved session has expired. Re-run with --login.")
                log("Log in to TroopWebHost in the browser window that just opened.")
                log(f"Waiting up to {timeout_s // 60} minutes...")
                for _ in range(timeout_s // 3):
                    page.wait_for_timeout(3000)
                    status, loc, text = _fetch(page, first)
                    if _is_csv(status, text):
                        break
                else:
                    raise LoginTimeout(f"Report {first} returned HTTP {status} {loc}".strip()
                                       + " - login didn't complete or this login lacks the role.")

            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            for i, menu_id in enumerate(menu_ids):
                if i:
                    status, loc, text = _fetch(page, menu_id)
                if not _is_csv(status, text):
                    log(f"[{menu_id}] not a CSV export (HTTP {status} {loc}). Check the ID / your role.")
                    continue
                path = out_dir / f"report_{menu_id}_{stamp}.csv"
                path.write_text(text, encoding="utf-8")
                rows = list(csv.reader(io.StringIO(text)))
                header = rows[0] if rows else []
                results.append({"menu_id": menu_id, "path": path, "header": header, "rows": max(len(rows) - 1, 0)})
                # Column names and counts only - never print row contents (PII).
                log(f"[{menu_id}] saved {path}")
                log(f"[{menu_id}] {max(len(rows) - 1, 0)} rows, {len(header)} columns: {', '.join(header)}")
        finally:
            ctx.close()
    return results


def main(argv=None):
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description="Export TroopWebHost reports as CSV (read-only).")
    ap.add_argument("menu_ids", nargs="*", default=["46093"], help="Menu_Item_ID from the 'Open in Excel' link")
    ap.add_argument("--preset", choices=sorted(PRESETS), help="named bundle of report IDs, e.g. volunteer-points")
    ap.add_argument("--login", action="store_true", help="open a window and wait for you to log in")
    ap.add_argument("--troop", default=DEFAULT_TROOP, help="troop slug in the site URL")
    ap.add_argument("--out", default=str(here / "exports"))
    ap.add_argument("--profile", default=str(here / ".browser-profile"))
    a = ap.parse_args(argv)
    if a.preset:
        a.menu_ids = PRESETS[a.preset] + [m for m in a.menu_ids if m != "46093" and m not in PRESETS[a.preset]]
    try:
        export_reports(a.menu_ids, a.out, a.troop, a.profile, login=a.login)
    except SessionExpired as e:
        print(e); return 2
    except LoginTimeout as e:
        print(e); return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
