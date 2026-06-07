"""
Sprawdza spojnosc folderu ze zdjeciami elementow z BOM.

Reguly:
  - kazda pozycja BOM (ID) powinna miec dokladnie jedno zdjecie,
    ktorego nazwa pliku zaczyna sie od 3-cyfrowego ID (np. '006...jpg' dla ID 6),
  - zglasza brakujace ID, duplikaty oraz pliki-sieroty (bez pasujacego ID).

Uzycie:
  py skrypty/validate_photos.py <folder_ze_zdjeciami>

Kod wyjscia: 0 = OK, 1 = znaleziono problemy.
"""
import os
import re
import sys

from bom_common import load_bom_rows

IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp", ".heic"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(f"BŁĄD: folder nie istnieje: {folder}")
        sys.exit(2)

    rows = load_bom_rows()
    expected = {}
    for r in rows:
        try:
            expected[f"{int(r['id']):03d}"] = r["nazwa"]
        except (TypeError, ValueError):
            pass

    # zmapuj pliki -> prefiks ID
    files = [f for f in os.listdir(folder) if os.path.splitext(f)[1].lower() in IMG_EXT]
    by_id = {}
    orphans = []
    for f in files:
        m = re.match(r"(\d{3})", f)
        if m and m.group(1) in expected:
            by_id.setdefault(m.group(1), []).append(f)
        else:
            orphans.append(f)

    missing = sorted(set(expected) - set(by_id))
    dups = {k: v for k, v in by_id.items() if len(v) > 1}

    print(f"Pozycji BOM: {len(expected)} | plików-zdjęć: {len(files)} | dopasowanych ID: {len(by_id)}")
    ok = True
    if missing:
        ok = False
        print(f"\n[BRAK ZDJĘCIA] {len(missing)} pozycji:")
        for mid in missing:
            print(f"  {mid} - {expected[mid]}")
    if dups:
        ok = False
        print(f"\n[DUPLIKATY] {len(dups)} ID ma wiele plików:")
        for k, v in sorted(dups.items()):
            print(f"  {k}: {', '.join(v)}")
    if orphans:
        ok = False
        print(f"\n[SIEROTY] {len(orphans)} plików bez pasującego ID:")
        for f in sorted(orphans):
            print(f"  {f}")

    if ok:
        print("\nOK — każda pozycja ma dokładnie jedno zdjęcie, brak sierot.")
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
