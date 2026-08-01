import html
import os
import re

symbols = ["🌱", "🐟", "🐔", "🦆", "🐖", "🥩", "🦐", "🔥", "🍄‍🟫"]
polish_alphabet_string = "aĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpQqRrSsŚśTtUuVvWwXxYyZzŹźŻż"

category_colors = {
    "Dania główne": "#ff6b6b",
    "Makarony": "#ffa94d",
    "Zupy": "#4dabf7",
    "Sałatki": "#69db7c",
    "Desery": "#f06595",
    "Przystawki": "#cc44ff",
    "Przetwory": "#ffd43b",
}


def in_path(path):
    """Sprawdza, czy ścieżka zawiera ukryte lub niepożądane foldery."""
    norm_path = path.replace("\\", "/")
    for var in [".git", "static", "scripts"]:
        if f"/{var}" in norm_path or norm_path.startswith(f"./{var}"):
            return True
    return False


def find_last_image(recipe_path):
    try:
        with open(recipe_path, "r", encoding="utf8") as file:
            text = file.read()
    except Exception:
        return None

    sections = re.split(r"(?m)^==\s+Zdjęcia\s*$", text)
    if len(sections) < 2:
        return None

    photos_section = re.split(r"(?m)^==\s+", sections[1])[0]
    matches = re.findall(r"image::([^\[]+)\[", photos_section)
    if matches:
        return matches[-1].strip()

    return None


def get_value(char):
    if char in polish_alphabet_string:
        return polish_alphabet_string.index(char)
    else:
        return len(polish_alphabet_string)


def extract_title_from_adoc(recipe_path, fallback_title):
    try:
        with open(recipe_path, "r", encoding="utf8") as file:
            for line in file:
                if line.startswith("= "):
                    raw_title = line.replace("= ", "").strip()
                    for symbol in symbols:
                        raw_title = raw_title.replace(symbol, "")
                    return re.sub(r"\s+", " ", raw_title).strip()
    except Exception:
        pass
    return fallback_title


def extract_rating_from_adoc(recipe_path, default=0):
    try:
        with open(recipe_path, "r", encoding="utf8") as file:
            for line in file:
                match = re.match(r"^:rating:\s*(\d+)\s*$", line)
                if match:
                    rating = int(match.group(1))
                    return max(0, min(rating, 5))
    except Exception:
        pass
    return default


def build_star_html(rating, max_stars=5):
    stars = "".join("★" if i < rating else "☆" for i in range(max_stars))
    return f'<span class="star-rating">{html.escape(stars)}</span>'


def create_index_adoc():
    with open("index.adoc", "w", encoding="utf8") as file:
        file.write("= Moje przepisy\n\n")
        file.write("++++\n")
        file.write("include::filters.html[]\n")
        file.write("++++\n\n")

    for path, subdirs, files in os.walk("."):
        if in_path(path):
            continue

        files = sorted(files, key=lambda word: [get_value(c) for c in word])
        folder_name = path.split("\\")[-1].replace("_", " ")

        cards = []

        for name in files:
            if name.endswith(".adoc") and name != "index.adoc":
                recipe_full_path = os.path.join(path, name)
                path_to_html = os.path.join(path.replace(".\\", ""), name.replace(".adoc", ".html")).replace("\\", "/")
                fallback_title = name.replace("_", " ").capitalize().replace(".adoc", "")

                title = extract_title_from_adoc(recipe_full_path, fallback_title)

                tags = []
                try:
                    with open(recipe_full_path, "r", encoding="utf8") as recipe_file:
                        recipe_text = recipe_file.read()
                        for symbol in symbols:
                            if symbol in recipe_text:
                                tags.append(symbol)
                except Exception:
                    pass
                emoji_html = " ".join(tags)

                rating = extract_rating_from_adoc(recipe_full_path)
                rating_html = f'<div class="card-rating">{build_star_html(rating)}</div>'

                image_path = find_last_image(recipe_full_path)
                full_image_path = f"/Recipes/static/images/{image_path}" if image_path else None

                if full_image_path:
                    image_html = f'<img class="card-image" src="{html.escape(full_image_path, quote=True)}" alt="{html.escape(title)}">'
                else:
                    image_html = '<div class="card-image card-image-placeholder">Brak zdjęcia</div>'

                top_category = folder_name.split("/")[0] if "/" in folder_name else folder_name

                category_label = (
                    f'<div class="card-category-label" style="background:{category_colors.get(top_category, "#999")}">'
                    f"{html.escape(folder_name)}</div>"
                )

                card_html = (
                    f'<article class="card" data-category="{html.escape(folder_name)}" data-rating="{rating}">'
                    f'<a class="card-main-link" href="{html.escape(path_to_html, quote=True)}">'
                    f"{category_label}"
                    f"{image_html}"
                    f'<div class="card-content">'
                    f'<h3 class="card-title">{html.escape(title)}'
                    f'<span class="card-emoji">{html.escape(emoji_html)}</span></h3>'
                    f"{rating_html}"
                    f"</div>"
                    f"</a>"
                    f"</article>"
                )

                cards.append(card_html)

        # Write section for this folder if it has recipes
        if cards:
            with open("index.adoc", "a+", encoding="utf8") as file:
                file.write("++++\n")
                file.write('<div class="cards-wrapper">\n')
                file.write('<div class="cards-grid">\n')
                for c in cards:
                    file.write(f"{c}\n")
                file.write("</div>\n")
                file.write("</div>\n")
                file.write("++++\n")


if __name__ == "__main__":
    create_index_adoc()
