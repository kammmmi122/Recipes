import re
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from enum import Enum

KW_INGREDIENTS_TAG = (
    "div.field.field-name-field-skladniki.field-type-text-long.field-label-hidden ul"
)
KW_RECIPE_TEXT_TAG = "div.group-przepis.field-group-div div ul"
KW_PORTION = (
    "div.field.field-name-field-ilosc-porcji.field-type-text.field-label-hidden"
)

AG_INGREDIENTS_TAG = "#recipeIngredients ul"
AG_RECIPE_TEXT_TAG = ".article-content-body"
AG_PORTION = "p.recipe_info"

J_INGREDIENTS_TAG = "#RecipeCard > p"
J_RECIPE_TEXT_TAG = "#RecipeCard > div.hyphenate"
J_PORTION = "#RecipeCard > ul"


ZZ_INGREDIENTS_TAG = "div.mg-ingredients__table"
ZZ_RECIPE_TEXT_TAG = " div.mg-recipe-instructions__steps-instructions.bodycopy > span"
ZZ_PORTION = "div.mg-ingredients__title > div > div"


KL_INGREDIENTS_TAG = "div.skladniki ul"
KL_RECIPE_TEXT_TAG = " #opis > p"
KL_PORTION = "#recipe_meta_1 > a > li"

MW_INGREDIENTS_TAG = "div.article__content > ul"
MW_RECIPE_TEXT_TAG = " div.article__content > p"
MW_PORTION = ""


class Webpages(Enum):
    KW = "kwestiasmaku"
    AG = "aniagotuje"
    J = "jadlonomia"
    ZZ = "zakochanewzupach"
    KL = "kuchnialidla"
    MW = "mojewypieki"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"
}


def clear_text(text):
    return text.replace("\u00a0", " ").replace("\u2013", "-").replace("\t", "").strip()


def get_number_of_portions(link):
    potions_text = ""
    selector = get_number_of_portion_selector(link)

    if selector:
        req = Request(url=link, headers=headers)
        with urlopen(req) as response:
            soup = BeautifulSoup(response, "html.parser")

        portions = soup.select_one(selector)
        if portions:
            potions_text = f"* {clear_text(portions.text)}\n"

    return potions_text


def get_number_of_portion_selector(link):
    selector = None
    if Webpages.KW.value in link:
        selector = KW_PORTION
    elif Webpages.AG.value in link:
        selector = AG_PORTION
    elif Webpages.J.value in link:
        selector = J_PORTION
    elif Webpages.ZZ.value in link:
        selector = ZZ_PORTION
    elif Webpages.KL.value in link:
        selector = KL_PORTION
    elif Webpages.MW.value in link:
        selector = MW_PORTION
    return selector


def get_recipe_ingredients(link):
    ingredients_text = ""
    selector = get_recipe_ingredients_selector(link)

    if selector:
        req = Request(url=link, headers=headers)
        with urlopen(req) as response:
            soup = BeautifulSoup(response, "html.parser")

        ingredients_many = soup.select(selector)
        for ingredients in ingredients_many:
            if Webpages.J.value in link:
                list_of_ingredients = [
                    clear_text(ingredient)
                    for ingredient in ingredients.text.split("\n")
                ]
            elif Webpages.ZZ.value in link:
                list_of_ingredients = []

                list_of_ingredients_name = ingredients.select(
                    "div.mg-span.recipe-ingredient-name"
                )

                list_of_ingredients_units = ingredients.select(
                    "div.mg-span.recipe-ingredient-unit"
                )

                for unit, name in zip(
                    list_of_ingredients_units, list_of_ingredients_name
                ):
                    unit_text = "".join(clear_text(unit.text).lower().split("\n"))
                    name_text = "".join(clear_text(name.text).lower().split("\n"))
                    list_of_ingredients.append(unit_text + " " + name_text)

            else:
                list_of_ingredients = [
                    clear_text(ingredient.text)
                    for ingredient in ingredients.select("li")
                ]
            ingredients_text += "\n".join(
                f"* {ingredient}" for ingredient in list_of_ingredients
            )
            ingredients_text += "\n"
    return ingredients_text


def get_recipe_ingredients_selector(link):
    selector = None
    if Webpages.KW.value in link:
        selector = KW_INGREDIENTS_TAG
    elif Webpages.AG.value in link:
        selector = AG_INGREDIENTS_TAG
    elif Webpages.J.value in link:
        selector = J_INGREDIENTS_TAG
    elif Webpages.ZZ.value in link:
        selector = ZZ_INGREDIENTS_TAG
    elif Webpages.KL.value in link:
        selector = KL_INGREDIENTS_TAG
    elif Webpages.MW.value in link:
        selector = MW_INGREDIENTS_TAG
    return selector


def get_recipe_text(link):
    recipe_text = ""
    selector = get_recipe_text_selector(link)

    if selector:
        req = Request(url=link, headers=headers)
        with urlopen(req) as response:
            soup = BeautifulSoup(response, "html.parser")

        texts_many = soup.select(selector)
        for texts in texts_many:
            if Webpages.AG.value or Webpages.ZZ.value or Webpages.KL.value in link:
                list_of_recipe_text = [
                    clear_text(text) for text in texts.text.split("\n")
                ]
            else:
                list_of_recipe_text = [
                    clear_text(text.text) for text in texts.select("li")
                ]
            recipe_text += "\n".join(list_of_recipe_text)
    return recipe_text


def get_recipe_text_selector(link):
    selector = None
    if Webpages.KW.value in link:
        selector = KW_RECIPE_TEXT_TAG
    elif Webpages.AG.value in link:
        selector = AG_RECIPE_TEXT_TAG
    elif Webpages.J.value in link:
        selector = J_RECIPE_TEXT_TAG
    elif Webpages.ZZ.value in link:
        selector = ZZ_RECIPE_TEXT_TAG
    elif Webpages.KL.value in link:
        selector = KL_RECIPE_TEXT_TAG
    elif Webpages.MW.value in link:
        selector = MW_RECIPE_TEXT_TAG
    return selector


def delete_files(dir_name):
    items = os.listdir(dir_name)

    for item in items:
        if item.endswith(".adoc"):
            os.remove(os.path.join(dir_name, item))


def read_file(file_name):
    with open(file_name, "r", encoding="utf8") as file:
        text = file.read()
    return text


def get_link(text, pattern):
    return re.findall(pattern, text)


def create_files(text, should_file_be_created):
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

    if should_file_be_created:
        create_recipe_file(list_of_links, list_of_files, capitalize_case_name)


def create_recipe_file(list_of_links, list_of_files, capitalize_case_name):
    for file, link, cap_title in zip(
        list_of_files, list_of_links, capitalize_case_name
    ):
        ingredients_text = get_recipe_ingredients(link)
        recipe_text = get_recipe_text(link)
        potions_text = get_number_of_portions(link)

        with open(f"Przepisy/{file}.adoc", "w", encoding="utf8") as f:
            f.write(f"= {cap_title} +++ <label class=\"switch\">  <input data-status=\"off\" type=\"checkbox\" >  <span class=\"slider round\"></span></label>+++ \n\n")
            f.write(
                '[cols=".<a,.<a"]\n[frame=none]\n[grid=none]\n|===\n|\n== Szczegóły\n'
            )
            f.write(f"{potions_text}")
            f.write(f"*{link}[link do źródła przepisu]\n")
            f.write("\n== Składniki\n")
            f.write(f"{ingredients_text}\n")
            f.write("\n|\n== Przygotowanie\n")
            f.write(f"{recipe_text}\n")
            f.write("\n|===\n\n[.text-center]\n== Zdjęcia\n")
            print(file, "created")


if __name__ == "__main__":
    delete_files("Przepisy")
    text = read_file("przepisy.txt")
    file_list = get_link(text, "(?P<url>https?://[^\s]+)")
    create_files(text, should_file_be_created=True)
