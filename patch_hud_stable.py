#!/usr/bin/env python3
"""Lot Flip: stop the top bar from shifting/'waving' as numbers change.
Usage:  python3 patch_hud_stable.py index.html
A backup is saved as index.html.bak first."""
import sys, shutil
path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
s = open(path, encoding="utf-8").read()
if "/* steady HUD numbers */" in s:
    sys.exit("Already applied. Nothing to change.")
if s.count("</style>") != 1:
    sys.exit("Unexpected stylesheet layout. Nothing was changed.")
CSS = """
/* steady HUD numbers */
.hud,.hud b{font-variant-numeric:tabular-nums}
.ht{min-width:46px}
.hsub{display:grid;grid-template-columns:1fr 1fr 1fr}
.hsub span:nth-child(1){text-align:left}
.hsub span:nth-child(2){text-align:center}
.hsub span:nth-child(3){text-align:right}
#money{transform-origin:left center}
@keyframes flash{30%{transform:scale(1.1);color:#fff}}
"""
shutil.copyfile(path, path + ".bak")
open(path, "w", encoding="utf-8").write(s.replace("</style>", CSS + "</style>", 1))
print("Done. Backup saved as", path + ".bak")
