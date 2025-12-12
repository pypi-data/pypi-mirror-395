import unicodedata as ud


def format_string(input_string: str):
    """
    Esta función recibe una cadena de texto, la convierte a minúsculas, elimina los espacios y
    cualquier carácter especial (solo se conservan letras y números).

    Parámetros:
    input_string (str): La cadena de texto que será procesada.

    Retorna:
    str: La cadena formateada en minúsculas, sin espacios ni caracteres especiales.
    """
    # Convert to lowercase, remove spaces and special characters
    # formatted_string = re.sub(r"[^a-z0-9]", "", input_string.lower())
    # return formatted_string

    if input_string is None:
        return ""
    s = " ".join(str(input_string).strip().split())  # colapsa espacios
    s = ud.normalize("NFD", s)
    s = "".join(ch for ch in s if ud.category(ch) != "Mn")  # quita acentos
    return s.casefold()
