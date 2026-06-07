"""
Wspólny loader dla BOM/BOM.xlsx.

Plik BOM.xlsx ma uszkodzony arkusz stylów (nieprawidlowa wartosc koloru), przez co
openpyxl nie otwiera go bezposrednio. Ten modul naprawia styles.xml w locie
(w pamieci, bez modyfikacji oryginalu) i zwraca wiersze BOM jako liste slownikow.

Kolumny BOM:
    Link Allegro | ID | Nazwa | Ilość | Cena jedn. (PLN) | Cena [PLN] | Wymiary (mm) | Path 1..4
"""
import io
import re
import zipfile

import openpyxl

HEADER_ROW = 4  # wiersz z naglowkami; dane zaczynaja sie od wiersza 5


def _repaired_xlsx_bytes(path):
    """Zwraca bajty xlsx z naprawionym styles.xml (usuniete bledne wartosci rgb)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "xl/styles.xml":
                text = data.decode("utf-8")
                # Usun rgb="..." ktore nie sa 8-cyfrowym aRGB hex
                text = re.sub(
                    r'rgb="([^"]*)"',
                    lambda m: "" if not re.fullmatch(r"[0-9A-Fa-f]{8}", m.group(1)) else m.group(0),
                    text,
                )
                data = text.encode("utf-8")
            zout.writestr(item, data)
    buf.seek(0)
    return buf


def load_bom_rows(path="BOM/BOM.xlsx"):
    """Wczytuje BOM i zwraca liste slownikow (po jednym na pozycje z wypelnionym ID/Nazwa)."""
    wb = openpyxl.load_workbook(_repaired_xlsx_bytes(path), data_only=True)
    ws = wb.active
    rows = []
    for r in ws.iter_rows(min_row=HEADER_ROW + 1, values_only=True):
        r = list(r) + [None] * (11 - len(r))
        link, pid, nazwa, ilosc, cena_j, cena, wymiary = r[0], r[1], r[2], r[3], r[4], r[5], r[6]
        paths = [str(x) for x in r[7:11] if x not in (None, "")]
        if not nazwa or pid in (None, ""):
            continue
        rows.append(
            {
                "id": int(pid) if isinstance(pid, (int, float)) else pid,
                "nazwa": str(nazwa).strip(),
                "ilosc": ilosc,
                "link": str(link).strip() if link else "",
                "wymiary": str(wymiary).strip() if wymiary else "",
                "paths": paths,
            }
        )
    wb.close()
    return rows


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    data = load_bom_rows()
    print(f"Wczytano {len(data)} pozycji BOM")
    for row in data[:5]:
        print(row)
