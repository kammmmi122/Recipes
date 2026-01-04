import os

symbols = ["🌱", "🐟", "🐔", "🦆", "🐖", "🥩", "🦐", "🔥"]
polish_alphabet_string = "aĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpQqRrSsŚśTtUuVvWwXxYyZzŹźŻż"


def in_path(path):
    in_path_var = False
    for var in [".git", "static", "scripts"]:
        if var in path:
            in_path_var = True

    return in_path_var


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

    with open(f"index.adoc", "w", encoding="utf8") as file:
        file.write("= Lista przepisów\n")
        file.write("\n++++\ninclude::filters.html[]\n++++\n")

    for path, subdirs, files in os.walk("."):
        files = sorted(files, key=lambda word: [get_value(c) for c in word])
        index = 0
        folder_name = path.split("\\")[-1].replace("_", " ")
        if ".\\" in path and not in_path(path):
            with open(f"index.adoc", "a+", encoding="utf8") as file:
                file.write(f"\n== {folder_name}\n\n")

        for name in files:
            if name.endswith("adoc") and name != "index.adoc":
                index += 1
                path_to_html = os.path.join(path.replace(".\\", ""), name.replace("adoc", "html")).replace("\\", "/")

                title = name.replace("_", " ").capitalize().replace(".adoc", "")
                tags = [""]
                with open(os.path.join(path, name), "r+", encoding="utf8") as ascii_file:
                    ascii_text = ascii_file.read()

                    for symbol in symbols:
                        if ascii_text.find(symbol) != -1:
                            tags.append(symbol)

                with open(f"index.adoc", "a+", encoding="utf8") as file:
                    file.write(f"{index}. link:{path_to_html}[{title}]{' '.join(tags)}\n")


if __name__ == "__main__":
    create_index_adoc()
    create_keep_note()
