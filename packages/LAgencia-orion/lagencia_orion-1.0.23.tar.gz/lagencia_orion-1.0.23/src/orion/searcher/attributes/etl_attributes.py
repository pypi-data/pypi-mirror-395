import os
from pathlib import Path

import pandas as pd

from orion.databases.db_empatia.repositories.querys_searcher import QuerysAttributes
from orion.tools import df_to_dicts

"""_summary_: Carga los atributos predefinidos en un archivo xlsx
    a latabla attributes"""


def load_attributes() -> bool:
    """
    Actualiza la tabla `attributes` en la base de datos con los datos
    predefinidos de un archivo Excel.

    La función lee un archivo `attributes.xlsx` ubicado en la carpeta
    `outputs/searcher`, lo carga como un DataFrame de pandas, y luego
    inserta los registros en la tabla `attributes` usando la operación
    de inserción masiva.

    Returns:
        bool:
            True si la operación de inserción fue exitosa.
            False si ocurrió un error durante el proceso.
    """
    try:
        path_read= Path("sample_data") / "attributes.xlsx"
        attributes = pd.read_excel(path_read)
        records = df_to_dicts(attributes)
        QuerysAttributes.bulk_insert(records)
        return True
    except Exception as ex:
        print(ex)
        return False
