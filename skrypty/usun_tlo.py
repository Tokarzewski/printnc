"""
Wsadowe usuwanie tla ze zdjec elementow (Issue #5).

Uzywa biblioteki `rembg` (sieci U2-Net). Przetwarza wszystkie obrazy z folderu
wejsciowego i zapisuje wersje z przezroczystym tlem (PNG) do folderu wyjsciowego,
ZACHOWUJAC nazwy plikow (czyli numerowanie wg ID z Issue #1).

Instalacja zaleznosci (jednorazowo):
    py -m pip install rembg pillow onnxruntime

Uzycie:
    py skrypty/usun_tlo.py <folder_wejsciowy> [folder_wyjsciowy]

Jesli folder wyjsciowy pominiety, tworzy '<wejsciowy>/bez_tla'.
Domyslnie nie nadpisuje istniejacych wynikow (uzyj --force).
"""
import os
import sys

IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    if not args:
        print(__doc__)
        sys.exit(2)

    in_dir = args[0]
    out_dir = args[1] if len(args) > 1 else os.path.join(in_dir, "bez_tla")
    if not os.path.isdir(in_dir):
        print(f"BŁĄD: folder wejściowy nie istnieje: {in_dir}")
        sys.exit(2)

    try:
        from rembg import remove, new_session
        from PIL import Image
        import io
    except ImportError:
        print("Brak zależności. Zainstaluj:\n    py -m pip install rembg pillow onnxruntime")
        sys.exit(2)

    os.makedirs(out_dir, exist_ok=True)
    session = new_session()  # domyslny model u2net

    files = [f for f in sorted(os.listdir(in_dir)) if os.path.splitext(f)[1].lower() in IMG_EXT]
    if not files:
        print(f"Brak obrazów w {in_dir}")
        sys.exit(1)

    done = skipped = failed = 0
    for f in files:
        src = os.path.join(in_dir, f)
        # wynik zawsze PNG (przezroczystosc), nazwa = ta sama baza (zachowuje ID)
        dst = os.path.join(out_dir, os.path.splitext(f)[0] + ".png")
        if os.path.exists(dst) and not force:
            skipped += 1
            continue
        try:
            with open(src, "rb") as fh:
                data = fh.read()
            result = remove(data, session=session)
            Image.open(io.BytesIO(result)).save(dst)
            done += 1
            print(f"  OK  {f} -> {os.path.basename(dst)}")
        except Exception as e:  # pojedyncza zla grafika nie przerywa calosci
            failed += 1
            print(f"  BŁĄD {f}: {e}")

    print(f"\nGotowe: {done} przetworzonych, {skipped} pominiętych (już istnieją), {failed} błędów.")
    print(f"Wyniki: {out_dir}")


if __name__ == "__main__":
    main()
