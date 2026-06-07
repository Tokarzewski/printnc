# #2 — Bodies vs Ilość (raport z żywego modelu)

Model: `20260527 PrintNC V4 Metalcutter V4.0.36 Beta4` · wygenerowano z żywego modelu przez Fusion MCP.

## Wniosek

**Liczba bodies w Fusion ≠ ilość do kupienia** — i dla śrub różnica jest dramatyczna.
W modelu śruby są rozmieszczone **reprezentatywnie** (nie każda sztuka jest wstawiona),
natomiast nakrętki, pręty gwintowane i wkręty dociskowe są wstawione w pełnej liczbie.
Dlatego ktoś ręcznie poprawił kolumnę `Ilość` w `BOM/BOM.xlsx` — i to ona jest źródłem prawdy do zakupów.

Dwie dodatkowe rzeczy potwierdzone na modelu:
- **0 bodies** zawiera w nazwie „mirror" → lustrzane duplikaty z Excela (`X HGW20CC(Mirror)`,
  `M6 Flush Grease Fitting(Mirror)`) są na poziomie **komponentu/wystąpienia**, nie body.
- **729** widocznych bodies łącznie; **483** nierozpoznanych (głównie części drukowane —
  pomijane celowo, „usually ignored").

## Porównanie: śruby i łączniki

| Część | Bodies (Fusion) | Ilość do kupienia (Excel) | Różnica |
|---|---:|---:|---:|
| Śruba M6x12 | 18 | 142 | **+124** |
| Śruba M5x20 | 10 | 112 | **+102** |
| Śruba M6x20 | 7 | 66 | **+59** |
| Śruba M6x30 | 6 | 32 | +26 |
| Śruba M4x16 | 6 | 28 | +22 |
| Śruba M6x50 | 6 | 24 | +18 |
| Śruba M4x12 | 2 | 22 | +20 |
| Śruba M5x12 | 1 | 4 | +3 |
| Śruba M8x45 | 1 | 3 | +2 |
| Śruba M4x8 łeb walcowy | 4 | 4 | 0 ✓ |
| Wkręt dociskowy M8x8 | 4 | 4 | 0 ✓ |
| Nakrętka M5 | 54 | 54 | 0 ✓ |
| Pręt gwintowany M5 (oś X) | 6 | 6 | 0 ✓ |
| Pręt gwintowany M5 (oś Y) | 12 | 12 | 0 ✓ |

## Przyczyny rozjazdu bodies ↔ ilość

1. **Reprezentatywne modelowanie śrub** — w CAD wstawiono tylko część śrub (po to, by pokazać
   złącze), a nie wszystkie fizyczne sztuki. To największe źródło różnicy.
2. **Zestawy (`... Ballscrew Set`)** — jeden zakup, ale wiele bodies w środku (śruba kulowa,
   nakrętka SFU, BF12, sprzęgło, mocowanie silnika). Skrypt liczy je osobno jako pojedyncze sztuki.
3. **Lustrzane wystąpienia** — na poziomie komponentu, nie body; w obecnym modelu nie powodują
   podwojenia body-count, ale w Excelu są osobnymi wierszami (np. smarowniczki `(mirror)`).
4. **`override_quantity`** w skrypcie już naprawia szyny (np. `X HGR20 Rail` = 2) — to istniejący
   mechanizm na przypadki bodies ≠ ilość.

## Rekomendacja

- **Kolumna `Ilość` w `BOM/BOM.xlsx` pozostaje źródłem prawdy do zakupów** — nie nadpisywać jej
  surowym body-count ze skryptu.
- Skrypt BOM traktować jako **listę pozycji + wymiary + ścieżki**, a nie jako licznik sztuk dla śrub.
- Opcjonalnie: dodać do `CUSTOM_PARTS` mnożnik/`override_quantity` dla śrub, żeby eksport ze skryptu
  od razu dawał realne ilości. Lista różnic powyżej to gotowa lista do uzupełnienia.

## Pełny body-count rozpoznanych części (Fusion)

```
  54  M5 Nut                  6  M6x50                   2  Steel: Y Roller Tubing
  18  M6x12                   6  X M5 Threaded Rod       2  X HGR20 Rail
  12  Y M5 Threaded Rod       4  HGH15CA slider block    1  80mm Spindle Clamp
  10  M5x20                   4  M4x8 Pan Head           1  M5x12
   8  HGW20CC slider block    4  M8x8 Grub               1  M8x45
   7  M6x20                   4  Steel: X Frame Tubing   1  X 1610 Ballscrew
   6  M4x16                   2  2Z HGR15 Rail           1  Y 1610 Ballscrew
   6  M6x30                   2  M4x12                   1  Y HGR20 Rail
   2  Steel: Y Frame Tubing   2  Steel: Y Roller Brace   1  Y2 1610 Ballscrew
   1  Steel: X Gantry Tubing  1  Steel: X Roller Angle   1  Y2 HGR20 Rail
   1  Steel: X Roller Tubing  1  Z 1204 Ballscrew
```
