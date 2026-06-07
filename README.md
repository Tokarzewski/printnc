# PrintNC V4 — MetalCutter

Pliki projektowe, BOM i skrypty pomocnicze do budowy frezarki CNC **PrintNC V4 (MetalCutter)**
w wersji stalowo-aluminiowej, pole robocze **1000 × 1000 mm**.

Model bazowy: `PrintNC V4 Metalcutter V4.0.36 Beta4`.

## Struktura repozytorium

| Katalog | Zawartość |
|---|---|
| `FUSION360/` | Modele Fusion 360 (`.f3d`) — maszyna i obudowa |
| `Metalowa Paczka 16/` | Pliki `.step` części do cięcia (stal) i frezowania (aluminium) |
| `BOM/` | Lista materiałowa (Excel) — patrz niżej |
| `BOM/generated/` | Pliki generowane ze skryptów (DIN, kategorie, sekcje, nazewnictwo zdjęć) |
| `skrypty/` | Skrypty Pythona (generator BOM dla Fusion + narzędzia pomocnicze) |
| `Notatki/` | Notatki, linki, sklepy, workflow |
| `OLD/` | Starsze wersje (do usunięcia — patrz Issue #9) |

## Pipeline BOM

Lista materiałowa powstaje w trzech krokach:

1. **Fusion 360 → CSV.** Skrypt [`skrypty/generate_printnc_bom.py`](skrypty/generate_printnc_bom.py)
   uruchamiany w Fusion (Utilities → Scripts and Add-Ins) przechodzi po widocznych bryłach
   modelu, rozpoznaje je wg słownika `CUSTOM_PARTS`, liczy ilości oraz wymiary i eksportuje CSV.
2. **CSV → Excel (wzbogacony).** Dane są ręcznie wzbogacane w `BOM/BOM.xlsx`: polskie nazwy,
   linki Allegro, ceny, kolumny `ID / Nazwa / Ilość / Wymiary / Path 1..4`.
3. **Skrypty pomocnicze** generują z `BOM.xlsx` dodatkowe pliki (patrz niżej).

> **Uwaga (Issue #2):** liczba brył w Fusion **nie jest** liczbą sztuk do kupienia — zwłaszcza
> dla śrub (modelowane reprezentatywnie). Źródłem prawdy do zakupów jest kolumna `Ilość`
> w `BOM.xlsx`. Szczegóły: [`BOM/generated/02_bodies_vs_ilosc.md`](BOM/generated/02_bodies_vs_ilosc.md).

## Skrypty (`skrypty/`)

| Skrypt | Opis |
|---|---|
| `generate_printnc_bom.py` | Generator BOM uruchamiany **w Fusion 360** (eksport CSV) |
| `bom_common.py` | Loader `BOM.xlsx` (naprawia uszkodzony arkusz stylów, zwraca wiersze) |
| `enrich_bom.py` | Generuje: nazwy z DIN (#3), kategorie zakupów (#6), nazewnictwo zdjęć (#1) |
| `sekcje_montazowe.py` | Dzieli BOM na ~10 sekcji montażowych (#4) |
| `validate_photos.py` | Sprawdza spójność folderu zdjęć z BOM (#1) |
| `usun_tlo.py` | Wsadowe usuwanie tła ze zdjęć przez `rembg` (#5) |

### Wymagania

```
py -m pip install openpyxl                   # loader BOM + skrypty pomocnicze
py -m pip install rembg pillow onnxruntime   # tylko dla usun_tlo.py
```

Skrypty pomocnicze uruchamiaj z katalogu głównego repo, np.:

```
py skrypty/enrich_bom.py
py skrypty/sekcje_montazowe.py
py skrypty/validate_photos.py <folder_ze_zdjeciami>
```

`generate_printnc_bom.py` działa wyłącznie wewnątrz Fusion 360 (wymaga API `adsk`).

## Status prac

Zadania śledzone są jako [GitHub Issues](https://github.com/Tokarzewski/printnc/issues) (#1–#10).
