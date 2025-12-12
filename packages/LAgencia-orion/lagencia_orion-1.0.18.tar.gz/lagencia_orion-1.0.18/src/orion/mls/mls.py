from datetime import datetime, timedelta
from typing import Dict

import pandas as pd
from loguru import logger

from orion.definition_ids import ID_BASE_MLS
from orion.mls.ftp import FTPMLS
from orion.mls.permitted_neighborhoods import CASTILLO as regions_castillo
from orion.mls.permitted_neighborhoods import ESTRELLA as regions_estrella
from orion.mls.permitted_neighborhoods import LIVIN as regions_livin
from orion.mls.permitted_neighborhoods import VILLACRUZ as regions_villacruz
from orion.tools import clean_text, cut_date_str, format_column_name  # noqa: F401


def filter_df_by_regions(df: pd.DataFrame, regions: Dict[str, str]) -> pd.DataFrame:
    logger.debug(f"Iniciando filtrado por regiones. Total registros iniciales: {len(df)}")
    df = df.copy()

    # Filtrar por municipios válidos
    df = df[df["district"].isin(regions.keys())]
    logger.debug(f"Filtrado por municipios válidos completado. Registros restantes: {len(df)}")

    # Filtrar por barrios válidos dentro de sus municipios
    valid_combinations = [(district, map_area) for district, map_areas in regions.items() for map_area in map_areas]
    df = df[df.apply(lambda x: (x["district"], x["map_area"]) in valid_combinations, axis=1)]
    logger.debug(f"Filtrado por barrios válidos completado. Registros restantes: {len(df)}")

    # Calcular sqft_total
    df["sqft_total"] = df.apply(lambda x: x["sqft_total"] if x["sqft_total"] > 0 else x["lot_sqft"], axis=1)
    logger.debug("Campo 'sqft_total' calculado correctamente.")

    logger.info(f"Filtrado por regiones finalizado. Total registros finales: {len(df)}")
    return df


def get_full_data_mls(date: str) -> pd.DataFrame:
    logger.info(f"Iniciando extracción completa MLS para la fecha {date}")
    service_ftp = FTPMLS()

    try:
        df_com, df_res = service_ftp.extract_files_com_and_res_from_server_ftp(date=date)
        print(df_com)
        print(df_res)
        logger.info(f"Archivos 'com' y 'res' extraídos correctamente. Registros: com={len(df_com)}, res={len(df_res)}")
    except Exception as e:
        logger.exception(f"Error al extraer archivos desde el servidor FTP para la fecha {date}: {e}")
        raise

    full_data = pd.concat([df_com, df_res])
    logger.info(f"Data MLS combinada exitosamente. Total de registros: {len(full_data)}")
    return full_data


def filter_mls_for_villacruz(full_data: pd.DataFrame) -> pd.DataFrame:
    logger.info("Iniciando filtrado MLS para Villacruz")
    result_filter_by_regions = filter_df_by_regions(df=full_data, regions=regions_villacruz)
    logger.info(f"Filtrado Villacruz completado. Registros: {len(result_filter_by_regions)}")
    return result_filter_by_regions


def filter_mls_for_estrella(full_data: pd.DataFrame) -> pd.DataFrame:
    logger.info("Iniciando filtrado MLS para Estrella")
    result_filter_by_regions = filter_df_by_regions(df=full_data, regions=regions_estrella)
    logger.info(f"Filtrado Estrella completado. Registros: {len(result_filter_by_regions)}")
    return result_filter_by_regions


def filter_mls_for_livin(full_data: pd.DataFrame) -> pd.DataFrame:
    logger.info("Iniciando filtrado MLS para Livin")
    result_filter_by_regions = filter_df_by_regions(df=full_data, regions=regions_livin)
    logger.info(f"Filtrado Livin completado. Registros: {len(result_filter_by_regions)}")
    return result_filter_by_regions


def filter_mls_for_castillo(full_data: pd.DataFrame) -> pd.DataFrame:
    logger.info("Iniciando filtrado MLS para Castillo")
    result_filter_by_regions = filter_df_by_regions(df=full_data, regions=regions_castillo)
    logger.info(f"Filtrado Castillo completado. Registros: {len(result_filter_by_regions)}")
    return result_filter_by_regions


def generate_url_first_image(unique_id: str):
    """Genera la URL de la primera imagen para un ID único."""
    url = f"http://images.realtyserver.com/photo_server.php?btnSubmit=GetPhoto&board=colombia&failover=clear.gif&name={unique_id}.L01"
    return url


def get_all_mls() -> pd.DataFrame:
    """Obtiene y procesa la información MLS consolidada."""
    logger.info("Iniciando la extracción completa de datos MLS...")

    # 1️⃣ Descarga de datos base
    try:
        date = datetime.now().strftime("%Y%m%d")
        mls_full = get_full_data_mls(date=date)
        logger.info("Datos MLS base obtenidos correctamente.")
    except Exception:
        logger.exception("Error al obtener datos MLS desde las fuentes.")
        raise

    if mls_full.empty:
        logger.warning("df vacio, parece que el servidor FTP no esta retornando data")
        return pd.DataFrame()

    # 2️⃣ Filtros por inmobiliaria
    logger.info("Aplicando filtros por inmobiliaria...")
    mls_villacruz = filter_mls_for_villacruz(full_data=mls_full)
    mls_estrella = filter_mls_for_estrella(full_data=mls_full)
    mls_livin = filter_mls_for_livin(full_data=mls_full)
    mls_castillo = filter_mls_for_castillo(full_data=mls_full)
    logger.debug("Filtros individuales aplicados correctamente.")

    # mls_villacruz.to_excel("mls_villacruz.xlsx", index=False)
    # mls_estrella.to_excel("mls_estrella.xlsx", index=False)
    # mls_livin.to_excel("mls_livin.xlsx", index=False)
    # mls_castillo.to_excel("mls_castillo.xlsx", index=False)



    # 3️⃣ Añadir columnas de control
    logger.debug("Agregando columnas de control para cada inmobiliaria.")
    mls_villacruz["show_villacruz"] = True
    mls_villacruz["source"] = "mls"

    mls_castillo["show_castillo"] = True
    mls_castillo["source"] = "mls"

    mls_estrella["show_estrella"] = True
    mls_estrella["source"] = "mls"

    mls_livin["show_livin"] = True
    mls_livin["source"] = "mls"

    # # 4️⃣ Consolidación de datos
    # logger.info("Concatenando dataframes de todas las fuentes MLS.")
    # mls_full = pd.concat([mls_villacruz, mls_castillo, mls_estrella, mls_livin])
    # mls_full.columns = list(map(format_column_name, mls_full.columns))

    # 4️⃣ Consolidación de datos
    logger.info("Concatenando dataframes de todas las fuentes MLS.")

    # Asegurar que todos los dataframes tengan todas las columnas show_* como False por defecto
    for df in [mls_villacruz, mls_castillo, mls_estrella, mls_livin]:
        for col in ["show_villacruz", "show_castillo", "show_estrella", "show_livin"]:
            if col not in df.columns:
                df[col] = False

    mls_full = pd.concat([mls_villacruz, mls_castillo, mls_estrella, mls_livin], ignore_index=True)

    # Agrupar por 'id' y combinar los campos show_* usando max()
    logger.info("Agrupando registros duplicados por 'id'...")

    # Identificar columnas show_* para agregar con max
    show_columns = ["show_villacruz", "show_castillo", "show_estrella", "show_livin"]

    # Crear diccionario de agregación
    agg_dict = dict.fromkeys(show_columns, "max")

    # Para las demás columnas, tomar el primer valor (ya que son iguales en duplicados)
    other_columns = [col for col in mls_full.columns if col not in show_columns + ["id"]]
    for col in other_columns:
        agg_dict[col] = "first"

    # Agrupar y agregar
    mls_full = mls_full.groupby("id", as_index=False).agg(agg_dict)

    logger.info(f"Registros consolidados: {len(mls_full)}")

    mls_full.columns = list(map(format_column_name, mls_full.columns))

    # 5️⃣ Limpieza y normalización de texto
    logger.info("Iniciando limpieza de textos y campos.")
    mls_full["active"] = True
    mls_full["remarks"] = mls_full["remarks"].apply(clean_text)
    mls_full["remarks_es"] = mls_full["remarks_es"].apply(clean_text)
    mls_full["web_title"] = mls_full["web_title"].apply(clean_text)
    mls_full["web_title_es"] = mls_full["web_title_es"].apply(clean_text)

    # 6️⃣ Manejo de duplicados
    logger.debug("Eliminando registros duplicados por ID.")
    duplicated_df = mls_full[mls_full.duplicated(subset="id", keep=False)]
    unique_df = mls_full[~mls_full.duplicated(subset="id", keep=False)]
    cleaned_duplicates = duplicated_df.drop_duplicates(subset="id", keep="first").copy()
    cleaned_duplicates["show_villacruz"] = True
    cleaned_duplicates["show_castillo"] = True
    cleaned_duplicates["show_livin"] = True
    mls_full = pd.concat([unique_df, cleaned_duplicates], ignore_index=True)

    # 7️⃣ Conversión de tipos y cálculo de campos
    logger.debug("Ajustando tipos de datos y agregando columnas calculadas.")
    mls_full["code"] = mls_full["id"].copy()
    mls_full["id"] = mls_full["id"].astype(int)
    mls_full["id"] = ID_BASE_MLS + mls_full["id"]
    mls_full["management"] = "Venta"
    mls_full["price_current"] = mls_full["price_current"].astype(float)
    mls_full["image"] = mls_full["unique_id"].apply(generate_url_first_image)

    # 8️⃣ Procesamiento de fechas
    logger.debug("Reemplazando y formateando fechas vacías.")
    mls_full["modification_date"] = mls_full["modification_date"].fillna("1900-01-01 00:00:00")
    mls_full["modification_date"] = mls_full["modification_date"].apply(cut_date_str)
    mls_full["modification_date"] = pd.to_datetime(mls_full["modification_date"])

    # 9️⃣ Filtrado de registros inválidos o duplicados entre agencias
    logger.info("Filtrando registros duplicados o no válidos.")
    codes_asesor_livin = [2188, 2189, 2191]
    codes_asesor_villacruz = [2485]
    codes = codes_asesor_livin + codes_asesor_villacruz
    # !


    before_filter = len(mls_full)
    mls_full = mls_full[mls_full["latitude"].notnull()]
    mls_full = mls_full[mls_full["longitude"].notnull()]
    mls_full = mls_full[~mls_full["listing_agent_id"].isin(codes)].copy()
    mls_full = mls_full[mls_full["property_type"].notnull()]
    mls_full = mls_full[mls_full["management"].notnull()]
    after_filter = len(mls_full)
    logger.info(f"Filtrado de registros completado. {before_filter - after_filter} registros eliminados.")

    # 🔟 Limpieza final de columnas innecesarias
    logger.debug("Eliminando columnas no requeridas.")
    mls_full.drop(columns=["tax_classification", "showcase_url", "iguide_url", "video_tour_url"], inplace=True)
    logger.info(f"Proceso de consolidación MLS completado exitosamente. Total de registros: {len(mls_full)}")
    return mls_full
