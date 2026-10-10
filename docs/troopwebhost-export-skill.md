---
name: troopwebhost-export
description: Programmatically pull TroopWebHost report data (roster, calendar, advancement, any "Open in Excel" report) as CSV using the user's own logged-in browser session, from a local script or another project. Use when: accessing TroopWebHost data programmatically, exporting a TroopWebHost report, automating Troop 420 Bothell data, finding a Menu_Item_ID, building a tool on top of TroopWebHost data. Triggers: troopwebhost, TroopWebHost API, troop 420, Troop420Bothell, FormReport.aspx, Menu_Item_ID, export troop calendar, export troop roster, scout data export.
---

# TroopWebHost report export

TroopWebHost has **no published API**. Any report with an "Open in Excel" link can be
downloaded as CSV once a browser session is logged in. This skill packages a working,
read-only method (verified 2026-10-10 against Troop 420 Bothell).

## Script

`scripts/twh_export.py` is a self-contained CLI and importable module (needs Python
Playwright + Chromium, which are already installed on this laptop). A working copy also lives
at `~/Documents/Troop420/twh_export.py`, which holds the user's browser profile and exports.

```bash
python3 twh_export.py --login 46093 46012   # opens a window; user logs in; saves CSVs
python3 twh_export.py 46093                 # headless reuse (currently fails: see Session)
# --troop Troop420Bothell  --out <dir>  --profile <dir>
```

```python
import sys; sys.path.insert(0, "<skill dir>/scripts")
from twh_export import export_reports, SessionExpired, LoginTimeout
results = export_reports(["46093"], out_dir="exports", profile="~/Documents/Troop420/.browser-profile", login=True)
# [{"menu_id", "path", "header", "rows"}]
```

For another project, copy the script in or import it. Point `--profile` at
`~/Documents/Troop420/.browser-profile` to share one login, or use a separate profile per project.

## How it works (the non-obvious parts)

- **Report URL is at the site root**:
  `https://www.troopwebhost.org/FormReport.aspx?Menu_Item_ID=<id>&Stack=1&ReportFormat=XLS`.
  `https://www.troopwebhost.org/Troop420Bothell/Index.htm` is only a frameset with the login
  form. `/Troop420Bothell/FormReport.aspx` returns **404**. The session cookies select the troop.
- **Response**: `text/plain` CSV with a UTF-8 BOM, despite `ReportFormat=XLS`. Decode with `utf-8-sig`.
- **Not logged in / no role**: a 302 to `http://www.TroopWebhost.com/index.htm`. Fetch with
  `max_redirects=0`, otherwise it looks like a 200 HTML page.
- **Login must be human**: the login page has a Google reCAPTCHA. Never automate credentials.
  Open a headed window and poll the report URL until it returns CSV.
- **Menu_Item_ID**: from the report's "Open in Excel" link, e.g.
  `javascript:LinkTo('FormReport.aspx?Menu_Item_ID=46093&Stack=1&ReportFormat=XLS','')`.
  IDs are site-specific. Known for Troop 420: **46093 = troop calendar of events**
  (Date, Time, Event Name, Location, Planned Activities). The gammann IDs (46012 Scout Directory,
  46013 Adult Directory, 46017 Patrol Roster) are from another troop, so verify before use.
- **Cookies seen**: `User_Login_ID`, `Session_Key`, `Language_ID`, `ScreenWidth`.

## Session limitation (open problem)

A login does **not** survive closing the browser. A headless rerun gets the 302 and the script
exits with code 2. `Session_Key` is most likely a session cookie that Chromium drops on close
(unconfirmed). Also avoid reloading `Index.htm` on an existing session, because that appeared
to reset it. Untested next step for unattended runs: save `ctx.storage_state()` / the cookies
after a successful export and re-add them with `ctx.add_cookies()` on the next launch.
TroopWebHost may still expire the session server-side.

## Environment gotchas

- `cortex browser` refuses troopwebhost.org with `net::ERR_BLOCKED_BY_CLIENT`, and no allowlist
  setting was found. Use local Python Playwright instead (`launch_persistent_context`, headed for login).
- `npx playwright` is not installed. Python Playwright is.

## Rules

- **Read-only.** Only GET exports the user can already download by hand. Do not POST to
  `FormList.aspx` admin grids (the gammann Med_Form uploader does this to write records).
  Writes change live troop data and need explicit user approval.
- **PII**: roster and directory exports contain minors' addresses, contacts and medical data.
  Keep files local, never print row contents to chat (headers and counts only), and never
  upload them anywhere.
- **Unofficial**: this replays internal endpoints that TroopWebHost may change without notice.
  The user is responsible for the Terms of Service. It is fine for personal use on this laptop.
  Don't deploy it to the troop site or share it without the user's OK.

## Reference

- Community tools using the same endpoints: https://github.com/gammann/TroopWebHost (Custom-Page
  HTML tools that run inside TWH same-origin; roles per report are listed in each tool's README).
- Official guide (manual import/export only): https://www.troopwebhost.org/help.aspx
