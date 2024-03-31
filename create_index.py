import os


def create_index_adoc():
    with open(f"index.adoc", "w", encoding="utf8") as file2:
        file2.write("= Lista przepisów\n\n")
        file2.write("== Przepisy\n\n")

    for path, subdirs, files in os.walk("."):
        for name in files:
            if name.endswith("adoc") and name != "index.adoc":
                path_to_html = os.path.join(
                    path.replace(".\\", ""), name.replace("adoc", "html")
                ).replace("\\", "/")
                with open(f"index.adoc", "a+", encoding="utf8") as file2:
                    file2.write(
                        f"1. link:{path_to_html}[{name.replace('_', ' ').capitalize().replace('.adoc', '')}]\n"
                    )


if __name__ == "__main__":
    create_index_adoc()
