import os


def create_keep_note():
    with open(f"keep_note.txt", "w", encoding="utf8") as file:
        pass

    for path, subdirs, files in os.walk("."):
        folder_name = path.split("\\")[-1]
        if ".\\" in path and ".git" not in path:
            with open(f"keep_note.txt", "a+", encoding="utf8") as file:
                file.write(f"\n{folder_name}\n\n")
        for name in files:
            if name.endswith("adoc") and name != "index.adoc":
                path_to_html = os.path.join(
                    path.replace(".\\", ""), name.replace("adoc", "html")
                ).replace("\\", "/")
                title = name.replace("_", " ").capitalize().replace(".adoc", "")
                link = f"https://kammmmi122.github.io/Recipes/{path_to_html}"

                with open(f"keep_note.txt", "a+", encoding="utf8") as file:

                    file.write(f"nowe - {title}; {link}\n")


def create_index_adoc():

    with open(f"index.adoc", "w", encoding="utf8") as file:
        file.write("= Lista przepisów\n")

    for path, subdirs, files in os.walk("."):
        index = 0
        folder_name = path.split("\\")[-1]
        if ".\\" in path and ".git" not in path:
            with open(f"index.adoc", "a+", encoding="utf8") as file:
                file.write(f"\n== {folder_name}\n\n")
        for name in files:
            if name.endswith("adoc") and name != "index.adoc":
                index += 1
                path_to_html = os.path.join(
                    path.replace(".\\", ""), name.replace("adoc", "html")
                ).replace("\\", "/")
                title = name.replace("_", " ").capitalize().replace(".adoc", "")

                with open(f"index.adoc", "a+", encoding="utf8") as file:
                    file.write(f"{index}. link:{path_to_html}[{title}]\n")


if __name__ == "__main__":
    create_index_adoc()
    create_keep_note()
