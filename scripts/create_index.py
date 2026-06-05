import html
import os
import re

symbols = ["🌱", "🐟", "🐔", "🦆", "🐖", "🥩", "🦐", "🔥"]
polish_alphabet_string = "aĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpQqRrSsŚśTtUuVvWwXxYyZzŹźŻż"


def in_path(path):
    in_path_var = False
    for var in [".git", "static", "scripts"]:
        if var in path:
            in_path_var = True
    return in_path_var


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


def create_keep_note():
    with open(f"keep_note.txt", "w", encoding="utf8") as file:
        pass

    for path, subdirs, files in os.walk("."):
        folder_name = path.split("\\")[-1]
        if ".\\" in path and not in_path(path):
            with open(f"keep_note.txt", "a+", encoding="utf8") as file:
                file.write(f"\n{folder_name}\n\n")
        for name in files:
            if name.endswith("adoc") and name != "index.adoc":
                path_to_html = os.path.join(path.replace(".\\", ""), name.replace("adoc", "html")).replace("\\", "/")
                title = name.replace("_", " ").capitalize().replace(".adoc", "")
                link = f"https://kammmmi122.github.io/Recipes/{path_to_html}"

                with open(f"keep_note.txt", "a+", encoding="utf8") as file:
                    file.write(f"nowe - {title}; {link}\n")


def get_value(char):
    if char in polish_alphabet_string:
        return polish_alphabet_string.index(char)
    else:
        return len(polish_alphabet_string)


def create_index_adoc():

    # HEADER
    with open(f"index.adoc", "w", encoding="utf8") as file:
        file.write("= Moje przepisy\n")
        file.write("\n++++\ninclude::filters.html[]\n++++\n")

    # WALK THROUGH FOLDERS
    for path, subdirs, files in os.walk("."):
        files = sorted(files, key=lambda word: [get_value(c) for c in word])
        folder_name = path.split("\\")[-1].replace("_", " ")

        cards = []

        # BUILD CARDS
        for name in files:
            if name.endswith("adoc") and name != "index.adoc":

                # URL
                path_to_html = os.path.join(
                    path.replace(".\\", ""), name.replace("adoc", "html")
                ).replace("\\", "/")

                # TITLE
                title = name.replace("_", " ").capitalize().replace(".adoc", "")

                # EMOJI TAGS
                tags = []
                try:
                    with open(os.path.join(path, name), "r", encoding="utf8") as recipe_file:
                        recipe_text = recipe_file.read()
                        for symbol in symbols:
                            if symbol in recipe_text:
                                tags.append(symbol)
                except Exception:
                    recipe_text = ""
                emoji_html = " ".join(tags)

                # IMAGE
                image_path = find_last_image(os.path.join(path, name))
                if image_path:
                    image_html = (
                        f'<img class="card-image" src="{html.escape(image_path, quote=True)}" '
                        f'alt="{html.escape(title)}">'
                    )
                else:
                    image_html = '<div class="card-image card-image-placeholder">Brak zdjęcia</div>'

                # CATEGORY LABEL (colored in CSS/JS)
                category_label = (
                    f'<div class="card-category-label">{html.escape(folder_name)}</div>'
                )

                # NEW CARD HTML — MATCHES YOUR NEW CSS
                card_html = (
                    f'<article class="card" '
                    f'data-category="{html.escape(folder_name)}" '
                    f'data-title="{html.escape(title.lower())}" '
                    f'data-emoji="{html.escape(emoji_html, quote=True)}">'
                    f'{category_label}'
                    f'{image_html}'
                    f'<div class="card-content">'
                    f'<h3 class="card-title">{html.escape(title)}</h3>'
                    f'<span class="card-emoji">{html.escape(emoji_html)}</span>'
                    f'<a class="card-link" href="{html.escape(path_to_html, quote=True)}">'
                    f'Zobacz przepis ></a>'
                    f'</div>'
                    f'</article>'
                )

                cards.append(card_html)

        # WRITE CARDS FOR THIS CATEGORY
        if cards:
            with open(f"index.adoc", "a+", encoding="utf8") as file:
                file.write("++++\n")
                file.write('<div class="cards-wrapper">\n')
                file.write('<div class="cards-grid">\n')
                for c in cards:
                    file.write(c + "\n")
                file.write('</div>\n')
                file.write('</div>\n')
                file.write("++++\n")


if __name__ == "__main__":
    create_index_adoc()
    create_keep_note()
