# TroopWebHost export catalog: Troop 420 Bothell

Built 2026-10-10 from the logged-in menu (one admin-level login) plus the official
[user guide](https://www.troopwebhost.org/help.aspx). Menu names and IDs only; no member data.
What you can see depends on your roles. Machine-readable list: [excel_exports.json](excel_exports.json).

## 1. Full database backup (everything)

| Item | Menu | ID | Notes |
|---|---|---|---|
| Database Backup | Administration > Database Backup | 45984 | `BackupUserDatabase.aspx`. Entire troop database as **XML**. Site Administrator only. Can't be restored back into TWH. Big DBs may time out, in which case support copies it to Dropbox etc. ([guide](https://www.troopwebhost.org/help.aspx?ID=190)) |

Photos and documents are not in the XML; they live in Azure storage.

## 2. Special-purpose exports (forms with a download button)

| Export | Menu | ID | Format / notes |
|---|---|---|---|
| Export Orders To Excel | Sales > Export Orders To Excel | 46111 | Per sales campaign: order summary or order detail |
| Export to Scoutbook Plus | Advancement > Recognize Recent Achievements | 53074 | Advancement file for Scoutbook Plus, max 500 records |
| Export Troop Awards Advancement Files | Advancement > Recognize Recent Achievements | 45954 | Blue-card / award-card file; POST then 302 to `FormCSV.aspx` |
| Export Roster to Troop Awards | Membership > Export Membership Data | 45898 | Directory file for TroopAwards software |
| Download Photos | Photo Gallery > Download Photos | 55647 | **zip** of selected photos per event (high-res if archived) |
| Subscribe to Calendar | My Stuff > Subscribe to Calendar | 45908 | Per-user calendar subscription URL (Google/Outlook/iPhone) |
| Export Inventory (upload format) | Inventory > Maintain Inventory | - | CSV in re-upload layout ([guide](https://www.troopwebhost.org/help.aspx?ID=102)) |
| Forms & Documents | Resources > Forms & Documents | - | Download files one at a time; no bulk option |

These are forms, not plain GETs: they need the page's own form posted (the gammann
Troop Awards tool shows the pattern). `twh_export.py` does not do these yet.

## 3. Reports with "Open in Excel" (118)

Each is listed with its ID. Plain `FormReport` IDs work with `twh_export.py <ID>` today.
`FormReportMultiSection` ones use a different page name, which the script doesn't handle yet.

Fetch URL: `https://www.troopwebhost.org/<page>?Menu_Item_ID=<ID>&Stack=1&ReportFormat=XLS`. Every item also has a PDF version.

### Administration (7)

| ID | Report | Page |
|---|---|---|
| 45974 | Security Reports > Menu Security Report | FormReport |
| 46072 | Security Reports > Role Task Report | FormReport |
| 46074 | Security Reports > Task Menu Items Report | FormReport |
| 46073 | Security Reports > Task Role Report | FormReport |
| 53188 | Security Reports > User Activity Report | FormReportMultiSection |
| 45973 | Security Reports > User Permissions Report | FormReport |
| 45975 | Security Reports > User Role Menu Report | FormReport |

### Advancement (50)

| ID | Report | Page |
|---|---|---|
| 46091 | Advancement Reports by Patrol > Eagle Merit Badge Status By Patrol | FormReport |
| 46090 | Advancement Reports by Patrol > Eagle Rank Requirements By Patrol | FormReportMultiSection |
| 46089 | Advancement Reports by Patrol > First Class Outdoor Requirements By Patrol | FormReportMultiSection |
| 46088 | Advancement Reports by Patrol > First Class Requirements By Patrol | FormReportMultiSection |
| 46085 | Advancement Reports by Patrol > Rank Status By Patrol | FormReport |
| 46087 | Advancement Reports by Patrol > Second Class Requirements By Patrol | FormReportMultiSection |
| 46086 | Advancement Reports by Patrol > Tenderfoot Requirements By Patrol | FormReportMultiSection |
| 46057 | Advancement Status Reports > Eagle Roll Call | FormReport |
| 56428 | Advancement Status Reports > Merit Badge Counts By Scout | FormReport |
| 52388 | Advancement Status Reports > Merit Badge History By Scout By Badge Name | FormReport |
| 46045 | Advancement Status Reports > Merit Badge History By Scout By Date Earned | FormReport |
| 52218 | Advancement Status Reports > Merit Badges In Progress By Badge | FormReport |
| 55502 | Advancement Status Reports > Merit Badges In Progress By Counselor | FormReport |
| 52217 | Advancement Status Reports > Merit Badges In Progress By Scout | FormReport |
| 46044 | Advancement Status Reports > Rank Advancement History By Scout | FormReport |
| 46042 | Advancement Status Reports > Rank Status by Age of Scout | FormReport |
| 46043 | Advancement Status Reports > Rank Status by Date of Current Rank | FormReport |
| 46033 | Advancement Status Reports > Scouts Ready For SM Conference or Board Of Review | FormReport |
| 55741 | Advancement Status Reports > Sign Off Requests | FormReport |
| 55384 | Maintain Advancement > Export Rank Requirement Status To Excel | FormReport |
| 51192 | Maintain Advancement > Export Rank Requirements Earned To Excel | FormReport |
| 51745 | National Outdoor Awards Reports > Adventure Segment | FormReport |
| 51742 | National Outdoor Awards Reports > Aquatics Segment | FormReport |
| 51740 | National Outdoor Awards Reports > Camping Segment | FormReport |
| 51743 | National Outdoor Awards Reports > Conservation Segment | FormReport |
| 51741 | National Outdoor Awards Reports > Hiking Segment | FormReport |
| 51744 | National Outdoor Awards Reports > Riding Segment | FormReport |
| 51771 | National Outdoor Awards Reports > World Conservation Award Report | FormReport |
| 46053 | Order of the Arrow Reports > Order of the Arrow Advancement Dates | FormReport |
| 53249 | Order of the Arrow Reports > Order of the Arrow Roster | FormReport |
| 46050 | Requirement Reports > Camping Merit Badge Camping Nights | FormReport |
| 46039 | Requirement Reports > Eagle Merit Badge Status By Scout | FormReport |
| 46040 | Requirement Reports > Eagle Outdoor Merit Badge Status By Scout | FormReport |
| 46038 | Requirement Reports > Eagle Rank Requirements By Scout | FormReportMultiSection |
| 46036 | Requirement Reports > First Class Requirements By Scout | FormReportMultiSection |
| 46041 | Requirement Reports > Leadership Rank Requirement Status | FormReport |
| 46037 | Requirement Reports > Outdoor Requirements Thru First Class By Scout | FormReportMultiSection |
| 51227 | Requirement Reports > Scout Requirements By Scout | FormReportMultiSection |
| 57468 | Requirement Reports > Sea Scout Requirements By Scout | FormReportMultiSection |
| 46035 | Requirement Reports > Second Class Requirements By Scout | FormReportMultiSection |
| 46034 | Requirement Reports > Tenderfoot Requirements By Scout | FormReportMultiSection |
| 46049 | Requirement Reports > Uncompleted Merit Badge Requirements By Requirement | FormReport |
| 46048 | Requirement Reports > Uncompleted Merit Badge Requirements By Scout | FormReport |
| 46047 | Requirement Reports > Uncompleted Rank Requirements By Requirement | FormReport |
| 46046 | Requirement Reports > Uncompleted Rank Requirements By Scout | FormReport |
| 57464 | Requirement Reports > Uncompleted Sea Scout Requirements By Scout | FormReport |
| 57465 | Requirement Reports > Uncompleted Sea Scout Requirements Summary | FormReport |
| 46055 | Requirement Reports > Uncompleted Venturing Requirements Report | FormReport |
| 46056 | Requirement Reports > Uncompleted Venturing Requirements Summary | FormReport |
| 46054 | Requirement Reports > Venturing Requirements By Scout | FormReportMultiSection |

### Calendar (14)

| ID | Report | Page |
|---|---|---|
| 59151 | Event Reports > Event Compliance | FormReport |
| 46095 | Event Reports > Event Participation Annual Summary | FormReportMultiSection |
| 46096 | Event Reports > Event Participation Cumulative Summary | FormReportMultiSection |
| 55472 | Event Reports > Most Recent Event Participation By Scout | FormReport |
| 57568 | Event Reports > Permission Needed By Event | FormReport |
| 57569 | Event Reports > Permission Needed By Scout | FormReport |
| 62573 | Event Reports > Permissions for Past Events | FormReport |
| 59976 | Event Reports > Planned Participation In Future Events | FormReport |
| 59836 | Event Reports > Shift Compliance | FormReport |
| 46093 | Event Reports > Upcoming Events Details | FormReport |
| 51898 | Event Reports > Upcoming Events Summary | FormReport |
| 62731 | Export Drivers Not Attending To Excel | FormReport |
| 45935 | Export Event Participation To Excel | FormReport |
| 53104 | Export Events To Excel | FormReport |

### Inventory (2)

| ID | Report | Page |
|---|---|---|
| 52370 | Inventory Report - All Items | FormReport |
| 52371 | Inventory Report - Checked Out Items | FormReport |

### Membership (39)

| ID | Report | Page |
|---|---|---|
| 53747 | Export Membership Data > Export Active Roster To Excel | FormReport |
| 45897 | Export Membership Data > Export Roster to Excel | FormReport |
| 61096 | Medical Form Reports > Expired Medical Forms | FormReport |
| 46024 | Medical Form Reports > Medical Form Expiration Dates - All Adults | FormReport |
| 46023 | Medical Form Reports > Medical Form Expiration Dates - All Scouts | FormReport |
| 46022 | Medical Form Reports > Medical Form Submission Dates - All Adults | FormReport |
| 46021 | Medical Form Reports > Medical Form Submission Dates - All Scouts | FormReport |
| 46025 | Training Reports > Adult Leaders Who Need SYT | FormReport |
| 46026 | Training Reports > Expired Training By Course | FormReport |
| 46027 | Training Reports > Expired Training By Person | FormReport |
| 46028 | Training Reports > Required Training By Course | FormReport |
| 46029 | Training Reports > Required Training By Person | FormReport |
| 46013 | Troop Directories > Adult Directory | FormReport |
| 56055 | Troop Directories > Adult Directory - Names Only | FormReport |
| 57107 | Troop Directories > Adult Involvement | FormReport |
| 46014 | Troop Directories > Adult Leader Directory | FormReport |
| 54040 | Troop Directories > Adult Leaders By Position | FormReport |
| 46032 | Troop Directories > Birthday List - Adults | FormReport |
| 46031 | Troop Directories > Birthday List - Scouts | FormReport |
| 59262 | Troop Directories > BSA Registrations | FormReport |
| 46016 | Troop Directories > Emergency Contact List | FormReport |
| 55386 | Troop Directories > Members with Allergies or Dietary Restrictions | FormReport |
| 52030 | Troop Directories > Merit Badge Counselors By Badge | FormReport |
| 52029 | Troop Directories > Merit Badge Counselors By Name | FormReport |
| 52055 | Troop Directories > Parent Scout Cross Reference | FormReport |
| 46017 | Troop Directories > Patrol Roster | FormReport |
| 46018 | Troop Directories > Patrol Roster w/Contact Info | FormReport |
| 46012 | Troop Directories > Scout Directory | FormReport |
| 51241 | Troop Directories > Scout Directory - Names Only | FormReport |
| 52344 | Troop Directories > Scout Directory - Names Only, By Patrol | FormReport |
| 57589 | Troop Directories > Scout Last Affirmation Dates | FormReport |
| 50808 | Troop Directories > Scout Leader Directory | FormReport |
| 46030 | Troop Directories > Scout Parent Cross Reference | FormReport |
| 52053 | Troop Directories > Scout Parent Cross Reference With Contact Info | FormReport |
| 52054 | Troop Directories > Scouts By Age | FormReport |
| 52746 | Troop Directories > Shirt Sizes | FormReportMultiSection |
| 46020 | Troop Directories > Swim Test Results | FormReport |
| 46015 | Troop Directories > Troop Contact List | FormReport |
| 59261 | Troop Directories > Upcoming BSA Registration Renewals | FormReport |

### Money (6)

| ID | Report | Page |
|---|---|---|
| 46004 | Export All Transactions to Excel | FormReport |
| 46061 | Financial Reports > Fund Balances By Fiscal Year | FormReport |
| 46060 | Financial Reports > Fund Balances Report | FormReport |
| 46058 | Financial Reports > Report Account Balances | FormReportMultiSection |
| 52178 | Financial Reports > Scout Account Balances | FormReport |
| 59943 | Financial Reports > Scout Account Balances By Gender | FormReport |

## 4. Not available

- No API, RSS, webhook, vCard or e-mail-list export (per the user guide).
- No QuickBooks/accounting export. Use **Money > Export All Transactions to Excel (46004)** or the XML backup.
- The mobile app syncs a full copy of the data, but only into the app.

## Sensitivity

Membership, medical, emergency-contact, allergy, swim and financial reports hold personal
data about minors. Keep exports local; `exports/` is git-ignored.
