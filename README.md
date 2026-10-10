# troop420-tools

Personal, read-only tools for pulling Troop 420 Bothell data out of
[TroopWebHost](https://www.troopwebhost.org/Troop420Bothell/Index.htm) using
your own logged-in browser session. TroopWebHost has no public API; these
replay the same "Open in Excel" requests your browser makes. Unofficial; the
endpoints can change without notice.

## Setup

```bash
pip install playwright && python3 -m playwright install chromium
```

## Scripts

| Script | What it does |
|---|---|
| `twh_export.py` | Download report(s) as CSV by `Menu_Item_ID`. `--login` opens a window for you to sign in (reCAPTCHA, so always a human). Also importable: `export_reports([...])`. |
| `twh_discover.py` | Work in progress: crawl the logged-in menus and catalog every export (labels, IDs, column names and row counts only). |

```bash
python3 twh_export.py --login 46093        # 46093 = troop calendar of events
python3 twh_export.py --login --preset volunteer-points   # 54040 positions + 53104 events (leaders) + 45935 participation
```

`--preset volunteer-points` pulls what the
[Troop 420 Adult Volunteer Points](https://sfc-gh-dfreriks.github.io/troop420-volunteer-points/) tracker
needs for leadership credit: **54040 Adult Leaders By Position** (Position, Adult, Start) and
**53104 Export Events To Excel** (its `Leaders` column names who led each event) and **45935 Export Event Participation To Excel** (who attended each event: High Adventure, summer camp, Wood Badge, PTC). Upload all three CSVs, plus the
Event Participation Annual Summary XLS, on the tracker's Committee → Import TroopWebHost tab.

Find a report's `Menu_Item_ID` in its "Open in Excel" link:
`javascript:LinkTo('FormReport.aspx?Menu_Item_ID=46093&Stack=1&ReportFormat=XLS','')`.

## How it works

See [docs/troopwebhost-export-skill.md](docs/troopwebhost-export-skill.md). In short:
reports live at the site root (`https://www.troopwebhost.org/FormReport.aspx?...`),
not under `/Troop420Bothell/`; exports are CSV with a UTF-8 BOM; a 302 to the
TroopWebHost home page means not logged in. The login doesn't yet survive a
browser restart.

## Data handling

- Read-only: only GETs exports the logged-in user can already download by hand.
- `exports/` and `.browser-profile/` are git-ignored. Exports contain minors'
  personal information; never commit or share them.
