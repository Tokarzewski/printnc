"""
Generuje pliki pomocnicze z BOM/BOM.xlsx:

  #3  03_nazwy_din.csv          - proponowane nazwy z numerami DIN (dla lacznikow)
  #6  06_kategorie.csv          - klasyfikacja pozycji wg rodzaju zakupu
  #1  01_zdjecia_nazewnictwo.csv- mapowanie ID -> sugerowana nazwa pliku zdjecia

Uruchom:  py skrypty/enrich_bom.py
Wyniki trafiaja do BOM/generated/.
"""
import csv
import os
import re
import sys

from bom_common import load_bom_rows

OUT = os.path.join("BOM", "generated")


def slug(text):
    """Bezpieczna nazwa pliku: usuwa znaki niedozwolone w Windows, skraca."""
    text = re.sub(r'[\\/:*?"<>|]', "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:60]


# ---------- #3: DIN ----------

def extract_din(link):
    """Wyciaga numer DIN z linku Allegro, jesli jest (np. ...din7985 -> '7985')."""
    m = re.search(r"din(\d+)", link, re.IGNORECASE)
    return m.group(1) if m else ""


# Sugerowany DIN dla lacznikow, gdzie link go nie zawiera (do potwierdzenia recznie).
DIN_HINTS = [
    (re.compile(r"łeb walcowy|leb walcowy", re.I), "", "łeb walcowy — potwierdzić: DIN 912 (imbus) lub DIN 84/ISO1207"),
    (re.compile(r"wkręt dociskowy|wkret dociskowy|grub", re.I), "", "wkręt dociskowy imbus — potwierdzić: DIN 913/914/915/916"),
]


def gen_din(rows):
    path = os.path.join(OUT, "03_nazwy_din.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Nazwa (obecna)", "DIN", "Nazwa proponowana", "Uwaga"])
        for r in rows:
            nazwa = r["nazwa"]
            is_fastener = bool(re.search(r"Śruba|Sruba|Wkręt|Wkret|Nakrętka|Nakretka|Podkładka|Podkladka", nazwa))
            din = extract_din(r["link"])
            uwaga = ""
            if not din:
                for rx, _d, note in DIN_HINTS:
                    if rx.search(nazwa) or rx.search(r["link"]):
                        uwaga = note
                        break
            if din:
                # wstaw "DIN xxxx" po czesci z rozmiarem, przed ewentualnym dopiskiem w nawiasie
                proponowana = f"{nazwa} DIN {din}"
            elif is_fastener and uwaga:
                proponowana = nazwa  # do recznego uzupelnienia
            else:
                proponowana = nazwa  # nie-lacznik: nazwa juz opisowa
            w.writerow([r["id"], nazwa, din, proponowana, uwaga])
    return path


# ---------- #6: rodzaj zakupu ----------

def categorize(r):
    nazwa = r["nazwa"].lower()
    link = r["link"].lower()
    paths = " ".join(r["paths"]).lower()
    if "aliexpress" in link:
        return "Inne strony (AliExpress)"
    if "alumin" in nazwa or "aluminiow" in link:
        return "Frezowane Alu"
    if "profil stalowy" in nazwa:
        return "Profil stalowy (laser/cięcie)"
    if "drukowan" in nazwa or "printed" in paths or "filament" in link or re.search(r"\bpla\b", link):
        return "Druk 3D"
    if "allegro" in link:
        return "Allegro"
    return "Do ustalenia"


def gen_kategorie(rows):
    path = os.path.join(OUT, "06_kategorie.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Nazwa", "Ilość", "Rodzaj zakupu", "Link"])
        for r in rows:
            w.writerow([r["id"], r["nazwa"], r["ilosc"], categorize(r), r["link"]])
    return path


# ---------- #1: nazewnictwo zdjec ----------

def gen_zdjecia(rows):
    path = os.path.join(OUT, "01_zdjecia_nazewnictwo.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Nazwa", "Wymiary (mm)", "Nazwa pliku (krótka)", "Nazwa pliku (opisowa)"])
        for r in rows:
            try:
                pid = f"{int(r['id']):03d}"
            except (TypeError, ValueError):
                pid = str(r["id"])
            w.writerow([r["id"], r["nazwa"], r["wymiary"], f"{pid}.jpg", f"{pid} - {slug(r['nazwa'])}.jpg"])
    return path


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(OUT, exist_ok=True)
    rows = load_bom_rows()
    for fn in (gen_din, gen_kategorie, gen_zdjecia):
        p = fn(rows)
        print("zapisano:", p)
    # Podsumowanie kategorii
    from collections import Counter
    c = Counter(categorize(r) for r in rows)
    print("\nRozkład kategorii:")
    for k, v in c.most_common():
        print(f"  {v:>3}  {k}")


if __name__ == "__main__":
    main()
