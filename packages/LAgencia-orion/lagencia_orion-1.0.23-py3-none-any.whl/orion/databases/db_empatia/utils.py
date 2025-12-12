from enum import Enum

from slugify import slugify

from orion.utils.formaters_string import format_string


class OrderBySector(int, Enum):
    MUNICIPIO: int = 0
    BARRIO: int = 1
    VEREDA: int = 2
    COMUNA: int = 3
    CORREGIMIENTO: int = 4
    LUGAR: int = 5


def generate_slug(type_sector: str, name_sector: str):
    # formatted_text = format_string(type_sector) + " en " + format_string(name_sector)
    # formatted_text= formatted_text.replace(" ", "-")
    return slugify(type_sector) + "-en-" + slugify(name_sector)


def generate_searcher(text: str):
    if not isinstance(text, str):
        return text
    text = format_string(text)
    key_words = ["el", "del", "la", "los", "las", "de", "y"]

    words = text.lower().strip().split(" ")
    words_ = words.copy()
    state = False
    for word in words:
        if word in key_words:
            words_.remove(word)
            state = True
    if state:
        new_text = text + "|" + " ".join(words_)
        return new_text
    return text
