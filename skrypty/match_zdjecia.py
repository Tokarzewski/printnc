"""
#1 - Przypisuje zdjecia (transparentne rendery) do wierszy skuratowanego BOM (BOM/BOM.xlsx)
i kopiuje je pod nazwami = ID, do folderu BOM/zdjecia/  (np. 006.png dla pozycji ID 6).

Zrodlo renderow: manifest + thumbs z eksportu Stage 1
    C:/Users/model/Desktop/PrintNC_BOM_export/{bom_data.json, thumbs/}

Dopasowanie:
  1) ALIAS (recznie potwierdzone, wysoka pewnosc) - lacznik/profil/szyna/sruba kulowa,
  2) auto: dokladne dopasowanie znormalizowanej nazwy / ostatniego elementu Path.

Pozycje bez pewnego dopasowania sa raportowane (do recznego uzupelnienia zdjeciem).

Uruchom:  py -3.14 skrypty/match_zdjecia.py
"""
import csv
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from bom_common import load_bom_rows

EXPORT = r"C:/Users/model/Desktop/PrintNC_BOM_export"
THUMBS = os.path.join(EXPORT, "thumbs")
OUT_DIR = os.path.join("BOM", "zdjecia")
REPORT = os.path.join("BOM", "generated", "01_dopasowanie_zdjec.csv")

# curated ID -> (render component name, variant 'set'|'detail')
# 'detail' = pojedyncza, wyizolowana bryla (np. jedna sruba); 'set' = caly komponent.
ALIAS = {
    1: ("M4x8 Pan Head", "detail"),
    2: ("M4x12 2Z Carriages", "detail"),
    3: ("M4x16", "detail"),
    4: ("M5x12 Ballscrew Nut Block", "detail"),
    5: ("M5x20", "detail"),
    6: ("M6x12", "detail"),
    7: ("M6x20", "detail"),
    8: ("M6x30", "detail"),
    9: ("M6x50", "detail"),
    10: ("M8x8 Grub Screw", "detail"),
    # 11 Śruba M8x45 - brak renderu w modelu
    12: ("M5 Threaded Rod and Nuts", "set"),
    13: ("M5 Threaded Rod and Nuts", "set"),
    14: ("M5 Threaded Rod and Nuts", "detail"),
    15: ("X HGR20", "set"),
    18: ("2Z HGR15", "set"),
    21: ("Y 1610 Ballscrew", "set"),
    22: ("X 1610 Ballscrew", "set"),
    23: ("Y2 1610 Ballscrew", "set"),
    24: ("Z 1204 Ballscrew", "set"),
    25: ("Extruded 80mm Spindle Clamp", "set"),
    26: ("XFrame", "set"),            # profil: rama oś X
    28: ("YRoller", "set"),           # profil: wózek oś Y
    29: ("YRollerBrace", "set"),      # profil: usztywnienie wózka Y
    33: ("Wasteboard", "set"),        # płyta drewniana
    35: ("XRollerShim", "set"),       # podkładka dystansowa wózka X
    36: ("M6 Flush Grease Fitting", "detail"),
    49: ("M6 Flush Grease Fitting", "detail"),
    51: ("M6 Flush Grease Fitting", "detail"),
}


def norm(s):
    return re.sub(r"[^0-9a-z]", "", (s or "").lower())


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    manifest = json.load(open(os.path.join(EXPORT, "bom_data.json"), encoding="utf-8"))
    by_name = {}
    for it in manifest["items"]:
        by_name[it["name"]] = it
        by_name.setdefault(norm(it["name"]), it)

    rows = load_bom_rows()
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)

    report = []
    copied = 0
    for r in rows:
        rid = r["id"]
        pid = f"{int(rid):03d}" if isinstance(rid, (int, float)) else str(rid)
        item = None
        variant = "set"
        conf = ""
        if rid in ALIAS:
            rn, variant = ALIAS[rid]
            item = by_name.get(rn) or by_name.get(norm(rn))
            conf = "alias"
        if item is None:
            for cand in ([r["paths"][-1]] if r["paths"] else []) + [r["nazwa"]]:
                item = by_name.get(norm(cand))
                if item:
                    conf = "auto"
                    break
        img_field = "image2" if variant == "detail" else "image"
        fname = (item or {}).get(img_field) or (item or {}).get("image") or ""
        src = os.path.join(THUMBS, fname) if fname else ""
        if src and os.path.isfile(src):
            shutil.copy2(src, os.path.join(OUT_DIR, pid + ".png"))
            copied += 1
            report.append([rid, r["nazwa"], item["name"], variant, conf, pid + ".png"])
        else:
            report.append([rid, r["nazwa"], "", "", "BRAK", ""])

    with open(REPORT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Nazwa", "Render", "Wariant", "Pewność", "Plik"])
        w.writerows(report)

    miss = [r for r in report if r[4] == "BRAK"]
    print(f"Dopasowano i skopiowano: {copied}/{len(rows)} -> {OUT_DIR}")
    print(f"Raport: {REPORT}")
    if miss:
        print(f"\nBez dopasowania ({len(miss)}) - do ręcznego zdjęcia:")
        for m in miss:
            print(f"  ID {m[0]}: {m[1]}")


if __name__ == "__main__":
    main()
