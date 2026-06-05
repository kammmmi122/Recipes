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


def find_first_image(recipe_path):
    try:
        with open(recipe_path, "r", encoding="utf8") as file:
            text = file.read()
    except Exception:
        return None

    sections = re.split(r"(?m)^==\s+Zdjęcia\s*$", text)
    if len(sections) < 2:
        return None

    photos_section = re.split(r"(?m)^==\s+", sections[1])[0]
    match = re.search(r"image::([^\[]+)\[", photos_section)
    if match:
        return match.group(1).strip()

    return None

def get_value(char):
    if char in polish_alphabet_string:
        return polish_alphabet_string.index(char)
    else:
        return len(polish_alphabet_string)

def create_index_adoc():

    with open(f"index.adoc", "w", encoding="utf8") as file:
        file.write("= Lista przepisów\n")
        file.write("\n++++\ninclude::filters.html[]\n++++\n")

    for path, subdirs, files in os.walk("."):
        files = sorted(files, key=lambda word: [get_value(c) for c in word])
        folder_name = path.split("\\")[-1].replace("_", " ")
        if ".\\" in path and not in_path(path):
            with open(f"index.adoc", "a+", encoding="utf8") as file:
                file.write(f"\n== {folder_name}\n\n")

        # Build an HTML grid for this folder using passthrough block
        cards = []
        for name in files:
            if name.endswith("adoc") and name != "index.adoc":
                path_to_html = os.path.join(path.replace(".\\", ""), name.replace("adoc", "html")).replace("\\", "/")
                title = name.replace("_", " ").capitalize().replace(".adoc", "")
                tags = []
                try:
                    with open(os.path.join(path, name), "r", encoding="utf8") as ascii_file:
                        ascii_text = ascii_file.read()
                        for symbol in symbols:
                            if symbol in ascii_text:
                                tags.append(symbol)
                except Exception:
                    ascii_text = ""

                # determine thumbnail or placeholder
                image_path = find_first_image(os.path.join(path, name))
                if image_path:
                    image_html = f'<div class="card-image" style="background-image:url(\'{html.escape(image_path, quote=True)}\')"></div>'
                else:
                    image_html = '<div class="card-image card-image-placeholder">Brak zdjęcia</div>'

                emoji_html = " ".join(tags)
                category_attr = html.escape(folder_name)
                title_attr = html.escape(title.lower())
                card_html = (
                    f'<article class="card" data-category="{category_attr}" data-title="{title_attr}">'
                    f'<a href="{html.escape(path_to_html, quote=True)}">'
                    f'{image_html}'
                    f'<div class="card-content">'
                    f'<div class="card-meta">'
                    f'<span class="card-category">{html.escape(folder_name)}</span>'
                    f'</div>'
                    f'<div class="card-title">{html.escape(title)}</div>'
                    f'<div class="card-emoji">{html.escape(emoji_html)}</div>'
                    f'</div>'
                    f'</a></article>'
                )
                cards.append(card_html)

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
