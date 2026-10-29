#!/usr/bin/env python3
"""Lot Flip: compact, pinned top bar.
  - Money and goal combined ("$850 / $2200") with a thin progress bar
  - Title row and stats row merged into one row (time, level, sound, pause)
  - Builders / income / percent moved to one small line
  - Bar stays visible while you scroll
  - Slightly smaller 3-star tags
Usage:  python3 patch_compact_hud.py index.html
A backup is saved as index.html.bak first."""
import sys, re, shutil
path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
s = open(path, encoding="utf-8").read()

if 'id="hud"' in s:
    sys.exit("Already applied. Nothing to change.")

NEW_HTML = (
'<div class="hud" id="hud">\n'
'    <div class="hrow">\n'
'      <div class="hm"><b id="money">$0</b><small>/ <span id="goal">$0</span></small></div>\n'
'      <div class="ht"><span id="tl">Time</span><b id="time">0s</b></div>\n'
'      <span id="lvl">Lv 1</span>\n'
'      <button class="pbtn" id="snd" style="min-height:32px;padding:0 8px">\U0001F50A</button>\n'
'      <button class="pbtn" id="bp" style="min-height:32px;padding:0 10px" aria-label="Pause">\u23f8</button>\n'
'    </div>\n'
'    <div class="hsub"><span>Builders <b id="bld">0/0</b></span><span>Income <b id="rent" style="color:var(--acc)">$0/s</b></span><span>Goal <b id="pct">0%</b></span></div>\n'
'    <div class="bar"><i id="gbar"></i></div>\n'
'  </div>\n  ')

NEW_CSS = """
/* compact pinned HUD */
.hud{position:sticky;top:env(safe-area-inset-top,0px);z-index:30;background:var(--bg);display:flex;flex-direction:column;gap:3px;padding:2px 0 4px}
.hrow{display:flex;align-items:center;gap:8px;background:var(--card);border:2px solid var(--line);border-radius:10px;padding:4px 8px}
.hm{display:flex;align-items:baseline;gap:4px;flex:1;min-width:0;white-space:nowrap}
.hm b{font-size:17px;color:var(--gold)}
.hm small{font-size:12px;color:var(--mut);font-weight:700}
.ht{display:flex;flex-direction:column;align-items:center;line-height:1.1}
.ht span{font-size:9px;color:var(--mut);text-transform:uppercase;font-weight:700}
.ht b{font-size:14px}
.hsub{display:flex;justify-content:space-between;font-size:11px;color:var(--mut);font-weight:700;padding:0 4px}
.hsub b{color:var(--text)}
.hud .bar{height:5px}
#bonus{gap:4px}
.chip{font-size:10px;padding:2px 7px}
"""

s, n = re.subn(r'<header>.*?<div class="prog">.*?</div></div>\s*(?=<div id="bonus">)',
               lambda m: NEW_HTML, s, count=1, flags=re.S)
if n != 1:
    sys.exit("Could not find the old header/stats block. Nothing was changed.")
if s.count("</style>") != 1:
    sys.exit("Unexpected stylesheet layout. Nothing was changed.")
s = s.replace("</style>", NEW_CSS + "</style>", 1)

need = ["money","goal","tl","time","bld","rent","pct","gbar","lvl","snd","bp"]
bad = [i for i in need if s.count('id="%s"' % i) != 1]
if bad:
    sys.exit("Check failed for ids: %s. Nothing was changed." % ", ".join(bad))

shutil.copyfile(path, path + ".bak")
open(path, "w", encoding="utf-8").write(s)
print("Done. Backup saved as", path + ".bak")
