import re
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

KW_INGREDIENTS_TAG = (
    "div.field.field-name-field-skladniki.field-type-text-long.field-label-hidden ul"
)
KW_RECIPE_TEXT_TAG = "div.group-przepis.field-group-div div ul"
KW_PORTION = (
    "div.field.field-name-field-ilosc-porcji.field-type-text.field-label-hidden"
)

AG_INGREDIENTS_TAG = "#recipeIngredients ul"
AG_RECIPE_TEXT_TAG = "p"
AG_PORTION = "p.recipe_info"


def get_number_of_portions(link):
    potions_text = ""
    selector = None
    if "kwestiasmaku" in link:
        selector = KW_PORTION
    elif "aniagotuje" in link:
        selector = AG_PORTION

    if selector:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"
        }
        req = Request(url=link, headers=headers)
        with urlopen(req) as response:
            soup = BeautifulSoup(response, "html.parser")
            portions = soup.select_one(selector)
            if portions:
                potions_text = f"* {portions.text.strip()}\n"

    return potions_text


def get_recipe_ingredients(link):
    ingredients_text = ""
    selector = None
    if "kwestiasmaku" in link:
        selector = KW_INGREDIENTS_TAG
    elif "aniagotuje" in link:
        selector = AG_INGREDIENTS_TAG

    if selector:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"
        }
        req = Request(url=link, headers=headers)
        with urlopen(req) as response:
            soup = BeautifulSoup(response, "html.parser")
            ingredients = soup.select_one(selector)
            if ingredients:
                list_of_ingredients = [
                    ingredient.text.strip() for ingredient in ingredients.select("li")
                ]
                ingredients_text = "\n".join(
                    f"* {ingredient}" for ingredient in list_of_ingredients
                )
    return ingredients_text


def get_recipe_text(link):
    recipe_text = ""
    selector = None
    if "kwestiasmaku" in link:
        selector = KW_RECIPE_TEXT_TAG
    elif "aniagotuje" in link:
        selector = AG_RECIPE_TEXT_TAG

    if selector:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"
        }
        req = Request(url=link, headers=headers)
        with urlopen(req) as response:
            soup = BeautifulSoup(response, "html.parser")
            texts = soup.select_one(selector)
            if texts:
                list_of_recipe_text = [text.text.strip() for text in texts.select("li")]
                recipe_text = "\n\n".join(list_of_recipe_text)
    return recipe_text


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


def create_files(text, create_file):
    list_of_recipes = text.split("\n")
    list_of_names = [
        (name.split(";")[0]).split("-")[-1].strip() for name in list_of_recipes
    ]
    list_of_links = [name.split(";")[-1] for name in list_of_recipes]
    list_of_files = [
        name.lower().replace(" ", "_").replace("/", "_").replace(",", "")
        for name in list_of_names
    ]
    capitalize_case_name = [name.capitalize() for name in list_of_names]

    if create_file:
        for file, link, cap_title in zip(
            list_of_files, list_of_links, capitalize_case_name
        ):

            ingredients_text = get_recipe_ingredients(link)
            recipe_text = get_recipe_text(link)
            potions_text = get_number_of_portions(link)

            with open(f"Przepisy/{file}.adoc", "w", encoding="utf8") as f:
                f.write(f"= {cap_title}\n\n")
                f.write(
                    '[cols=".<a,.<a"]\n[frame=none]\n[grid=none]\n|===\n|\n== Szczegóły\n'
                )
                f.write(f"{potions_text}")
                f.write(f"*{link}[link do źródła przepisu]\n")
                f.write("\n== Składniki\n")
                f.write(f"{ingredients_text}")
                f.write("\n|\n== Przygotowanie\n")
                f.write(f"{recipe_text}")
                f.write("\n== Zdjęcia\n|===\n")
                print(file, "created")

        # update_index_adoc(list_of_files, capitalize_case_name)


def update_index_adoc(list_of_files, capitalize_case_name):
    list_of_files = sorted(list_of_files)
    capitalize_case_name = sorted(capitalize_case_name)
    for file, cap_title in zip(list_of_files, capitalize_case_name):
        with open(f"index.adoc", "a+", encoding="utf8") as file2:
            file2.write(f"1. link:Przepisy/{file}.html[{cap_title}]\n")


if __name__ == "__main__":
    delete_files()
    text = read_file()
    file_list = get_link(text)
    create_files(text, True)
