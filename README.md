# Traffic Data Intake

Count request, Form 7 cost estimate and Appendix A §2.H footage conformance checking for
City of Charlotte task orders under **RFP 269-2027-027 — Traffic Data Collection and
Processing Services**.

ChiResearch Technologies, LLC bids the processing branch of the scope stated at RFP §3.1,
"collect and/or process." This page covers the intake side of that service.

## What is operational

- **Count-type selection and cost estimate.** Prices are the firm unit prices submitted on
  Form 7, including the Appendix A §4.G.ii classification surcharge entered under Form 7
  Section 5. Lines Form 7 marks NOT BID return the reason rather than a price.
- **Count-number assignment**, so every submittal can be labeled as Appendix A §2.B requires.
- **The 72-hour processing clock** from receipt of conforming video, per Appendix A §1.D.
- **Appendix A §2.H footage conformance check.** Resolution, duration, file size and average
  bitrate are measured against the §2.H minimum (color, 30 fps, 720 × 480, 1.5 Mbps), and a
  SHA-256 hash is computed over the whole file. The check runs in the browser on a local
  file, so a 30 GB recording is validated without being uploaded anywhere. Frame rate and
  color are not measurable in a browser; both are reported as such and confirmed during
  processing rather than asserted here.

## Demonstration and completed work

Below the intake panels the page carries three further sections:

- **Processing demonstration.** The annotated sixty-second run, with the measured output beside it:
  110 northbound, 108 southbound, 218 total against the engine's reported 221, and the twenty-one trucks
  whose FHWA class the engine left unresolved. The run is labeled as internal validation on licensed
  source footage — not a client engagement and not a Charlotte location.
- **What the City receives for a count.** The report, raw data, exchange formats, verification log and
  database upload, each against the clause that requires it.
- **Other completed work.** The Washington DES award, BabyDay and the two academic engagements, each
  carrying a label saying what it is and what it is not.

## What is specified and not built

Authenticated, resumable multi-gigabyte transfer into immutable storage. Until that is in
service, video is received by online file transfer service — Appendix A §15.C.iv and
§16.E.iii name that medium as preferred where video is supplied electronically — and
task-order coordination runs by email, which Addendum 1, Item 6 states is acceptable.

## Build

`index.html` is generated, not hand-edited. `src/intake.html` is the source; it is also what
is published on the Claude Artifacts platform, where the count register is backed by a shared
database. On a static host there is no such database, so the register falls back to
`localStorage` and is per-browser.

```
cd src && python3 -I build_standalone.py
```

That writes `standalone/index.html`; copy it to the repository root. Keeping one source means a
price change cannot leave the two builds disagreeing.

## Hosting

Served by GitHub Pages from the repository root. No build step and no server-side code: a
single self-contained HTML file whose only external dependencies are Google Fonts and
`js-sha256` from cdnjs.

## Prices

Unit prices here are the firm prices submitted on Form 7 for RFP 269-2027-027 and are
effective for the Initial Term and Renewal Terms. They are reproduced from the submitted
workbook; the workbook governs.
