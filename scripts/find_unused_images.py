import os
from pathlib import Path

# --- KONFIGURACJA ---
# Ścieżka do katalogu z obrazkami (relatywna do głównego folderu)
IMAGES_DIR = Path("static/images")

# Rozszerzenia plików, które uważamy za obrazy (możesz dodać własne, np. '.jpeg')
IMAGE_EXTENSIONS = {'.png', '.jpg', '.gif', '.svg', '.webp'}
# --------------------

def find_unused_images():
    # 1. Sprawdzenie czy katalog z obrazkami istnieje
    if not IMAGES_DIR.exists() or not IMAGES_DIR.is_dir():
        print(f"Błąd: Katalog '{IMAGES_DIR}' nie istnieje. Upewnij się, że uruchamiasz skrypt z głównego folderu projektu.")
        return

    print("🔍 Skanowanie katalogu w poszukiwaniu obrazów...")
    # Pobieramy mapowanie: sama nazwa pliku -> pełna ścieżka (żeby łatwo raportować)
    # Ignorujemy wielkość liter w rozszerzeniach
    image_pool = {
        p.name: p for p in IMAGES_DIR.rglob("*") 
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    }
    
    if not image_pool:
        print("Nie znaleziono żadnych obrazów w podanym katalogu.")
        return

    print(f"Znaleziono obrazów: {len(image_pool)}")
    
    # Zbiór nazw plików, które będziemy usuwać z listy, gdy znajdziemy je w kodzie
    unused_images = set(image_pool.keys())

    print("📄 Przeszukiwanie plików .adoc...")
    # 2. Przeszukiwanie wszystkich plików .adoc w repozytorium
    # rglob("*") przeszukuje też podkatalogi. Przechodzimy po całym repozytorium.
    for adoc_file in Path(".").rglob("*.adoc"):
        # Pomijamy pliki, które mogłyby być wewnątrz samego folderu z obrazkami (jeśli to możliwe)
        if IMAGES_DIR in adoc_file.parents:
            continue
            
        try:
            # Otwieramy plik z kodowaniem utf-8 (ignorując ewentualne błędy dekodowania)
            content = adoc_file.read_text(encoding="utf-8", errors="ignore")
            
            # Sprawdzamy, które z wciąż nieużywanych obrazów znajdują się w treści pliku
            # Robimy kopię zbioru do iteracji, żeby móc modyfikować oryginał w pętli
            for img_name in list(unused_images):
                if img_name in content:
                    unused_images.remove(img_name)
                    
        except Exception as e:
            print(f"Nie można odczytać pliku {adoc_file}: {e}")

        # Jeśli znaleźliśmy już wszystkie, możemy przerwać wcześniej
        if not unused_images:
            break

    # --- WYNIKI ---
    print("\n" + "="*40)
    if unused_images:
        print(f"⚠️ Znaleziono {len(unused_images)} nieużywanych obrazów:")
        print("="*40)
        # Sortujemy wyniki alfabetycznie według ścieżki dla czytelności
        for img_name in sorted(unused_images):
            print(f"- {image_pool[img_name]}")
    else:
        print("🎉 Sukces! Wszystkie obrazy z tego folderu są używane w plikach .adoc.")
        print("="*40)

if __name__ == "__main__":
    find_unused_images()
