"""
Dzieli pozycje BOM na ~10 sekcji montazowych (do instrukcji skladania / plakatu).
Generuje BOM/generated/04_sekcje_montazowe.md.

Sekcje wynikaja z hierarchii 'Path' w BOM oraz z nazw pozycji.
"""
import os
import re
import sys
from collections import OrderedDict

from bom_common import load_bom_rows

OUT = os.path.join("BOM", "generated", "04_sekcje_montazowe.md")

# Kolejnosc = kolejnosc montazu / ukladu na plakacie
SECTIONS = [
    "1. Rama stalowa",
    "2. Wasteboard (blat)",
    "3. Prowadnice liniowe i śruby kulowe",
    "4. Oś X – napęd",
    "5. Oś Y – napęd",
    "6. Oś Y2 – napęd",
    "7. Oś Z – napęd",
    "8. Zespół 2Z (karetka wrzeciona)",
    "9. Wrzeciono i uchwyt",
    "10. Złączność i drobnica",
]


def classify(r):
    nazwa = r["nazwa"]
    nl = nazwa.lower()
    p1 = r["paths"][0] if len(r["paths"]) > 0 else ""
    p2 = r["paths"][1] if len(r["paths"]) > 1 else ""

    if "uchwyt wrzeciona" in nl or "wrzeciono" in nl:
        return SECTIONS[8]
    if nl.startswith("profil") or (p1 == "Structure" and "drewn" not in nl):
        return SECTIONS[0]
    if "drewn" in nl or "Wasteboard" in r["paths"]:
        return SECTIONS[1]
    if nl.startswith("szyna") or "śruba kulowa" in nl:
        return SECTIONS[2]
    if p1.startswith("Zaxis Dual Carriage"):
        return SECTIONS[7]
    if p2 == "XAxis Hardware":
        return SECTIONS[3]
    if p2 == "YAxis Hardware":
        return SECTIONS[4]
    if p2 == "Y2Axis Hardware":
        return SECTIONS[5]
    if p2 == "ZAxis Hardware":
        return SECTIONS[6]
    # śruby, nakrętki, pręty, podkładki, wkręty bez przypisania osi
    return SECTIONS[9]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rows = load_bom_rows()
    buckets = OrderedDict((s, []) for s in SECTIONS)
    for r in rows:
        buckets[classify(r)].append(r)

    lines = [
        "# #4 — Sekcje montażowe PrintNC V4 (≈10 sekcji)",
        "",
        "Podział wszystkich pozycji BOM na sekcje — do instrukcji składania oraz jako układ",
        "rozłożonego modelu 3D (styl plakatu). Kolejność = sugerowana kolejność montażu.",
        "",
        "![Model PrintNC V4 – widok izometryczny](model_iso.png)",
        "",
        "> **Rozłożony model 3D (plakat „Golf II”):** ten dokument to gotowy podział na sekcje.",
        "> Samo rozłożenie/eksplozja części obok siebie wymaga ręcznej pracy w CAD (Fusion/Rhino) —",
        "> nie da się tego w pełni zautomatyzować. Każdą sekcję poniżej rozkłada się jako osobny",
        "> moduł, a render `model_iso.png` służy jako pogląd całości.",
        "",
    ]
    for s in SECTIONS:
        items = buckets[s]
        n = sum((r["ilosc"] if isinstance(r["ilosc"], (int, float)) else 0) for r in items)
        lines.append(f"## {s}  \n_{len(items)} pozycji, ~{int(n)} szt._\n")
        lines.append("| ID | Nazwa | Ilość | Wymiary (mm) |")
        lines.append("|---:|---|---:|---|")
        for r in items:
            lines.append(f"| {r['id']} | {r['nazwa']} | {r['ilosc']} | {r['wymiary']} |")
        lines.append("")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))
    print("zapisano:", OUT)
    for s in SECTIONS:
        print(f"  {len(buckets[s]):>2} poz.  {s}")


if __name__ == "__main__":
    main()
