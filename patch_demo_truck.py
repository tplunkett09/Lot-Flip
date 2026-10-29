#!/usr/bin/env python3
"""Adds the demolition truck to Lot Flip's traffic system.
Usage:  python3 patch_demo_truck.py YourGameFile.html
Creates YourGameFile_truck.html next to it. Your original is not touched."""
import sys, os
if len(sys.argv) < 2:
    sys.exit("Usage: python3 patch_demo_truck.py YourGameFile.html")
src = sys.argv[1]
out = os.path.splitext(src)[0] + "_truck.html"
s = open(src, encoding="utf-8").read()

EDITS = [
# 1. hide the old in-lot truck
(r""".tk{animation:tk linear both}""",
 r""".tk{display:none}"""),
# 2a. truck artwork + makeVehicle accepts a truck flag
(r"""function makeVehicle(color,cls){""",
 r"""function truckMarkup(){
  return '<svg viewBox="0 0 32 18" aria-hidden="true"><rect x="1" y="2.5" width="19" height="13" rx="1.5" fill="#f9a825" stroke="#263238" stroke-width="1.1"/><g class="ld"><rect x="3.5" y="5" width="6" height="4.5" fill="#8d6e63"/><rect x="10" y="8.5" width="7" height="5" fill="#6d4c41"/><rect x="11" y="4.5" width="5" height="3" fill="#a1887f"/></g><rect x="21" y="3.5" width="10" height="11" rx="2.5" fill="#f57f17" stroke="#263238" stroke-width="1.1"/><rect x="25.5" y="4.7" width="4" height="8.6" rx="1" fill="#bde3f5" stroke="#38505a" stroke-width=".6"/><rect x="3" y="0" width="5" height="3" rx="1" fill="#1f2933"/><rect x="3" y="15" width="5" height="3" rx="1" fill="#1f2933"/><rect x="23" y="1" width="5" height="3" rx="1" fill="#1f2933"/><rect x="23" y="14" width="5" height="3" rx="1" fill="#1f2933"/><rect x="30" y="4.5" width="1.3" height="2" fill="#fff7b0"/><rect x="30" y="11.5" width="1.3" height="2" fill="#fff7b0"/></svg>';
}
function makeVehicle(color,cls,truck){"""),
# 2b.
(r"""el.innerHTML=vehicleMarkup(color);return el;""",
 r"""el.innerHTML=truck?truckMarkup():vehicleMarkup(color);return el;"""),
# 3. render trucks with the truck sprite, load fills as the house comes down
(r"""if(!tr.el||!tr.el.isConnected){tr.el=makeVehicle(tr.color,"traffic-car");sc.appendChild(tr.el)}""",
 r"""if(!tr.el||!tr.el.isConnected){tr.el=makeVehicle(tr.color,"traffic-car",tr.truck);sc.appendChild(tr.el)}
    if(tr.truck){const ld=tr.el.querySelector(".ld"),L=lots[i];if(ld&&L)ld.style.opacity=L.st==="demo"?Math.min(1,L.dp*1.4):1}"""),
# 4. start a demolition truck
(r"""function beginTrafficDeparture(i,tr,g){""",
 r"""function startDemoTruck(i){
  const g=trafficGeometry(i);if(!g)return;
  const cur=traffic[i];if(cur&&cur.el)cur.el.remove();
  const dir=nearSideLaneDirection(g);
  traffic[i]={kind:"arrive",t:0,dur:trafficDuration(g,dir,"arrive"),dir,color:"#f9a825",truck:true,speedFactor:1,actualSpeed:0};
}
function beginTrafficDeparture(i,tr,g){"""),
# 5. demolition only runs while the truck is parked; truck leaves when done
(r"""else if(l.st==="demo"){l.dp+=dt/l.dd;if(l.dp>=1){reset(l);l.st="owned";fx(i,"done");toast("Demolition finished on Lot "+(i+1)+". You still own the lot.")}}""",
 r"""else if(l.st==="demo"){const tr=traffic[i];if(!tr||!tr.truck)startDemoTruck(i);else if(tr.kind==="parked"){l.dp+=dt/l.dd;if(l.dp>=1){beginTrafficDeparture(i,tr,trafficGeometry(i));reset(l);l.st="owned";fx(i,"done");toast("Demolition finished on Lot "+(i+1)+". You still own the lot.")}}}"""),
]

for n, (old, new) in enumerate(EDITS, 1):
    c = s.count(old)
    if c != 1:
        sys.exit("Edit %d: expected 1 match but found %d. Nothing was changed. "
                 "Make sure this is the driveway/traffic version of the game." % (n, c))
    s = s.replace(old, new)
open(out, "w", encoding="utf-8").write(s)
print("Done. Wrote", out)
