import re
import os

def delete_files():
    dir_name = "Przepisy"
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".adoc"):
            os.remove(os.path.join(dir_name, item))

def read_file():
    with open("przepisy.txt", "r", encoding="utf8") as f:
        text = f.read()
    return text

def get_link(text):
    return re.findall("(?P<url>https?://[^\s]+)", text)

def create_files(text):

    list_of_recipes = text.split("\n")
    list_of_names = [(name.split(";")[0]).split('-')[-1].strip() for name in list_of_recipes]
    list_of_links = [name.split(";")[-1] for name in list_of_recipes]
    list_of_files = [name.lower().replace(" ", "_").replace("/", "_").replace(",", "") for name in list_of_names]
    capitalize_case_name = [name.capitalize() for name in list_of_names]
    print(capitalize_case_name)

    for file, link, cap_title in zip(list_of_files, list_of_links, capitalize_case_name):
        with open(f"Przepisy/{file}.adoc", "w", encoding="utf8") as f:
            f.write(f"= {cap_title}\n\n")
            f.write('[cols=".<a,.<a"]\n[frame=none]\n[grid=none]\n|===\n|\n== Szczegóły\n')
            f.write(f"*{link} [link do źródła przepisu]\n")
            f.write("\n== Składniki\n")
            f.write("\n|\n== Przygotowanie\n")
            f.write("\n== Zdjęcia\n|===\n")
            print (file, "created")

if __name__ == "__main__":
    delete_files()
    text = read_file()
    file_list = get_link(text)
    create_files(text)
