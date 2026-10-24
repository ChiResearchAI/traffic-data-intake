#!/usr/bin/env python3
"""Generate the deployable build of the intake page from the artifact source.

One source of truth: portal/intake.html is what gets published to claude.ai (the
Artifact platform wraps it in a document skeleton). This script wraps that same
markup in a real HTML document and swaps the persistence block so the page keeps
its count register in localStorage when the Claude runtime is absent, which is the
case on any ordinary static host.

Run:  python3 -I build_standalone.py
Out:  portal/standalone/index.html
"""
import io
import os
import re

SRC = "intake.html"
OUT = os.path.join("standalone", "index.html")

SKELETON_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Count request, Form 7 cost estimate and Appendix A 2.H footage conformance checking for City of Charlotte task orders under RFP 269-2027-027.">
<meta name="robots" content="noindex">
<style>
:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px system-ui,-apple-system,sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>
</head>
<body>
"""

SKELETON_TAIL = "\n</body>\n</html>\n"

# The artifact build reaches for the platform database. The deployable build keeps
# the same call first — so this file also works if it is ever published as an
# artifact — and falls back to per-browser storage when the runtime is absent.
OLD_PERSIST_HEAD = "// ---- persistence; the page works without it ----"

NEW_PERSIST = r"""// ---- persistence: platform database when present, this browser otherwise ----
var LS_KEY = "chiresearch.intake.counts.v1";
function localLoad(){
  try{ var raw = window.localStorage.getItem(LS_KEY); return raw ? JSON.parse(raw) : []; }
  catch(e){ return []; }
}
function localSave(){
  try{ window.localStorage.setItem(LS_KEY, JSON.stringify(rows)); }catch(e){}
}
function markLocalOnly(){
  var e = document.getElementById("regempty");
  if(e) e.textContent = "No counts requested yet. Assigning a count number above records it here with "
    + "its Form 7 estimate and its 72-hour processing deadline. On this host the register is kept in this "
    + "browser only; it is not shared between devices.";
}
(async function(){
  var ok = false;
  try{
    if(window.claude && window.claude.use){
      var u = await window.claude.use("user");
      uid = u ? await u.id().catch(function(){return null}) : null;
      db = await window.claude.use("db");
      if(db){
        ok = true;
        var snap = await db.collection("counts").get();
        var got=[]; snap.forEach ? snap.forEach(function(d){got.push(d.data?d.data():d)})
                                 : (got = snap.docs ? snap.docs.map(function(d){return d.data()}) : []);
        if(got.length){ rows=got; render(); }
        db.collection("counts").onSnapshot(function(s){
          var r=[]; s.forEach ? s.forEach(function(d){r.push(d.data?d.data():d)})
                              : (r = s.docs ? s.docs.map(function(d){return d.data()}) : []);
          rows=r; render();
        });
      }
    }
  }catch(e){ ok = false; }
  if(!ok){
    db = null;
    markLocalOnly();
    rows = localLoad();
    render();
  }
})();"""


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)
    src = io.open(SRC, encoding="utf-8").read()

    # Replace the whole trailing persistence IIFE with the fallback-aware version.
    i = src.index(OLD_PERSIST_HEAD)
    j = src.index("</script>", i)
    body = src[:i] + NEW_PERSIST + "\n" + src[j:]

    # Also persist locally on every write, without disturbing the platform path.
    needle = "  rows.push(rec); render();"
    assert body.count(needle) == 1, "submit handler not found"
    body = body.replace(needle, "  rows.push(rec); render();\n  if(!db) localSave();")

    # The deployable document carries its own <title>; the artifact skeleton supplies one.
    assert "<title>" in body, "title missing"

    os.makedirs("standalone", exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(SKELETON_HEAD + body + SKELETON_TAIL)

    n = len(io.open(OUT, encoding="utf-8").read())
    print("wrote %s  (%d bytes)" % (OUT, n))
    print("external dependencies: fonts.googleapis.com, cdnjs.cloudflare.com (js-sha256)")
    print("everything else is inline; no build step, no server code")


if __name__ == "__main__":
    main()
