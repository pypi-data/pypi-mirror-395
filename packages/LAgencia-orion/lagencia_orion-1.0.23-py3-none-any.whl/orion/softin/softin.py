import asyncio
import os
import re
import unicodedata
from typing import Any, Dict, List

import httpx
import pandas as pd
from loguru import logger

from orion.definition_ids import ID_BASE_SOFTIN_CASTILLO, ID_BASE_SOFTIN_ESTRELLA, ID_BASE_SOFTIN_VILLACRUZ, MARGIN_FOR_DUPLICATE_CONTROL

"""orion.softin.softin
Módulo responsable de obtener y procesar inmuebles desde el API de Softin

Este módulo contiene:
 - Utilidades para normalizar nombres de columnas
 - Clases que representan compañías configuradas vía variables de entorno
 - Cliente asíncrono `Softin` para paginar y obtener inmuebles
 - Funciones para obtener y procesar datos para Villacruz, Castillo y Estrella

"""


# from src.tools import format_column_name
def format_column_name(column_name: str) -> str:
    """Normaliza un nombre de columna para uso en DataFrames.

    Transformaciones realizadas:
    - Se normaliza Unicode para eliminar acentos y diacríticos.
    - Se convierte a ASCII ignorando caracteres no representables.
    - Se pasa a minúsculas.
    - Se reemplaza 'ñ' por 'n'.
    - Se sustituyen espacios por guiones bajos.
    - Se eliminan caracteres que no sean letras minúsculas, dígitos o guión bajo.

    Args:
        column_name: Nombre original de la columna.

    Returns:
        Nombre de columna formateado y seguro para usar como etiqueta en DataFrame.
    """

    # Normalizar el string para eliminar acentos y tildes
    normalized_name = unicodedata.normalize("NFD", column_name)
    normalized_name = normalized_name.encode("ascii", "ignore").decode("utf-8")

    # Convertir todo a minúsculas
    formatted_name = normalized_name.lower()

    # Reemplazar "ñ" por "n"
    formatted_name = formatted_name.replace("ñ", "n")

    # Reemplazar espacios por "_"
    formatted_name = re.sub(r"\s+", "_", formatted_name)

    # Eliminar caracteres no alfanuméricos ni "_"
    formatted_name = re.sub(r"[^a-z0-9_]", "", formatted_name)

    return formatted_name


class Company:
    name: str
    endpoint: str
    bearer_token: str


class Villacruz(Company):
    name = "villacruz"
    endpoint: str = os.getenv("ENDPOINT_API_SOFTIN_VILLACRUZ")
    bearer_token: str = os.getenv("ACCESS_TOKEN_SOFTIN_VILLACRUZ")


class Castillo(Company):
    name = "castillo"
    endpoint: str = os.getenv("ENDPOINT_API_SOFTIN_CASTILLO")
    bearer_token: str = os.getenv("ACCESS_TOKEN_SOFTIN_CASTILLO")


class Estrella(Company):
    name = "estrella"
    endpoint: str = os.getenv("ENDPOINT_API_SOFTIN_ALQUIVENTAS")
    bearer_token: str = os.getenv("ACCESS_TOKEN_SOFTIN_ALQUIVENTAS")


class Softin:
    url_base = "https://zonaclientes.softinm.com/api/inmuebles/consultar_inmuebles/"

    def __init__(self, company: Company):
        self.company = company

    async def fetch_data(self, quantity_per_page: int = 100, page: int = 1) -> List[Dict[str, Any]]:
        if self.company.bearer_token is None:
            raise ValueError("bearer_token no puede ser nulo")
        headers = {
            "Authorization": f"Bearer {self.company.bearer_token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(headers=headers, timeout=30) as client:
            result = await client.post(self.company.endpoint, json={"cantidadporpagina": quantity_per_page, "pagina": page})
            try:
                result.raise_for_status()

                # Verificar que hay contenido antes de parsear JSON
                if not result.content:
                    logger.info("La respuesta está vacía")
                    return []

                # Verificar el Content-Type
                content_type = result.headers.get("content-type", "")
                if "application/json" not in content_type:
                    logger.info(f"Content-Type inesperado: {content_type}")
                    logger.info(f"Contenido de la respuesta: {result.text[:200]}")
                    return []

                return result.json()

            except httpx.HTTPStatusError as e:
                logger.info(f"Error HTTP {e.response.status_code}: {e.response.text}")
                return []
            except ValueError as e:
                logger.info(f"Error al parsear JSON: {e}")
                logger.info(f"Contenido de la respuesta: {result.text[:200]}")
                return []
            except Exception as e:
                logger.info(f"Error inesperado: {type(e).__name__}: {e}")
                return []

        return []

    async def fetch_full_data(self, quantity_per_page: int = 100, batch_size: int = 3) -> List[Dict[str, Any]]:
        """
        Obtiene todos los inmuebles paginando en lotes concurrentes.

        Args:
            quantity_per_page: Cantidad de registros por página
            batch_size: Número de páginas a solicitar simultáneamente

        Returns:
            Lista con todos los inmuebles
        """
        all_data = []
        page = 1

        logger.info(f"Iniciando paginación para {self.company.name}")

        while True:
            # Crear tareas para el batch actual
            tasks = [self.fetch_data(quantity_per_page=quantity_per_page, page=page + i) for i in range(batch_size)]

            # Ejecutar batch de páginas en paralelo
            results = await asyncio.gather(*tasks)

            # Procesar resultados
            pages_with_data = 0
            for i, data in enumerate(results):
                current_page = page + i

                if not data or len(data) == 0:
                    # Página vacía, terminamos
                    break

                all_data.extend(data)
                pages_with_data += 1
                logger.info(f"Página {current_page}: {len(data)} registros. Total: {len(all_data)}")

                # Si es la última página (menos registros que el límite)
                if len(data) < quantity_per_page:
                    logger.info(f"Última página alcanzada ({current_page})")
                    logger.info(f"Total de inmuebles: {len(all_data)}")
                    return all_data

            # Si ninguna página del batch tuvo datos, terminamos
            if pages_with_data == 0:
                logger.info(f"Paginación completada en página {page - 1}")
                break

            # Si obtuvimos menos páginas con datos que el batch_size, terminamos
            if pages_with_data < batch_size:
                break

            page += batch_size

        logger.info(f"Total de inmuebles obtenidos: {len(all_data)}")
        return all_data


# ======================================================================================
async def get_data_softin_villacruz() -> List[Dict]:
    # Inicializar servicios
    logger.debug("Inicializando servicio para villacruz")
    service_villacruz = Softin(company=Villacruz)

    # Obtener datos de cada servicio
    logger.info("📥 Obteniendo datos de Villacruz...")
    result_villacruz = await service_villacruz.fetch_full_data()
    logger.success(f"✅ Villacruz: {len(result_villacruz)} propiedades obtenidas")

    return result_villacruz


def processing_data_for_villacruz(result_villacruz: List[Dict]) -> pd.DataFrame:
    df_villacruz = pd.DataFrame(result_villacruz)
    if not df_villacruz.empty:
        df_villacruz["source"] = "softin"
        df_villacruz["show_villacruz"] = True
        df_villacruz["show_castillo"] = False
        df_villacruz["show_estrella"] = False
        df_villacruz["consecutivo"] = df_villacruz["consecutivo"].astype(int)
        df_villacruz["id"] = ID_BASE_SOFTIN_VILLACRUZ + df_villacruz["consecutivo"]
        logger.debug(f"Villacruz procesado: {len(df_villacruz)} registros")
    else:
        logger.warning("⚠️ DataFrame de Villacruz está vacío")

    return df_villacruz


# ======================================================================================
async def get_data_softin_castillo() -> List[Dict]:
    logger.debug("Inicializando servicio para castillo")
    service_castillo = Softin(company=Castillo)
    logger.info("📥 Obteniendo datos de Castillo...")
    result_castillo = await service_castillo.fetch_full_data()
    logger.success(f"✅ Castillo: {len(result_castillo)} propiedades obtenidas")
    return result_castillo


def processing_data_for_castillo(result_castillo: List[Dict]) -> pd.DataFrame:
    # Procesar DataFrame Castillo
    logger.info("🔄 Procesando datos de Castillo...")
    df_castillo = pd.DataFrame(result_castillo)
    if not df_castillo.empty:
        df_castillo["source"] = "softin"
        df_castillo["show_castillo"] = True
        df_castillo["show_villacruz"] = False
        df_castillo["show_estrella"] = False
        df_castillo["consecutivo"] = df_castillo["consecutivo"].astype(int)
        df_castillo["id"] = ID_BASE_SOFTIN_CASTILLO + df_castillo["consecutivo"]
        logger.debug(f"Castillo procesado: {len(df_castillo)} registros")
    else:
        logger.warning("⚠️ DataFrame de Castillo está vacío")

    return df_castillo


# ======================================================================================
async def get_data_softin_estrella() -> List[Dict]:
    logger.info("🔄 Procesando datos de Estrella...")
    service_estrella = Softin(company=Estrella)
    logger.info("📥 Obteniendo datos de Estrella...")
    result_estrella = await service_estrella.fetch_full_data()
    logger.success(f"✅ Estrella: {len(result_estrella)} propiedades obtenidas")
    return result_estrella


def processing_data_for_estrella(result_estrella: List[Dict]) -> pd.DataFrame:
    # Procesar DataFrame Estrella
    logger.info("🔄 Procesando datos de Estrella...")
    df_estrella = pd.DataFrame(result_estrella)
    if not df_estrella.empty:
        df_estrella["source"] = "softin"
        df_estrella["show_estrella"] = True
        df_estrella["show_castillo"] = False
        df_estrella["show_villacruz"] = False
        df_estrella["consecutivo"] = df_estrella["consecutivo"].astype(int)
        df_estrella["id"] = ID_BASE_SOFTIN_ESTRELLA + df_estrella["consecutivo"]
        logger.debug(f"Estrella procesado: {len(df_estrella)} registros")
    else:
        logger.warning("⚠️ DataFrame de Estrella está vacío")

    return df_estrella


# ======================================================================================


def concatenate_softin_data_sources(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    # Concatenar DataFrames
    logger.info("🔗 Concatenando DataFrames...")
    df_full = pd.concat(dfs)
    logger.debug(f"DataFrame concatenado: {len(df_full)} registros totales")

    df_full["activo"] = True
    df_full.reset_index(inplace=True)

    df_full["imagenes"] = df_full["imagenes"].astype(str)
    initial_count = len(df_full)
    df_full.drop_duplicates(subset=["id"], inplace=True)
    duplicates_removed = initial_count - len(df_full)
    if duplicates_removed > 0:
        logger.info(f"🧹 Duplicados eliminados: {duplicates_removed}")

    logger.info("📝 Formateando nombres de columnas...")
    df_full.columns = list(map(format_column_name, df_full.columns))

    # Procesar propiedades por tipo de servicio
    logger.info("🏠 Procesando propiedades de Arriendo...")
    lease = df_full[df_full["tipo_servicio"] == "Arriendo"]
    lease.loc[:, "precio"] = lease["precio"]
    logger.debug(f"Propiedades de arriendo: {len(lease)}")

    logger.info("🏘️ Procesando propiedades de Venta...")
    sell = df_full[df_full["tipo_servicio"] == "Venta"]
    sell.loc[:, "precio"] = sell["precio_venta"]
    logger.debug(f"Propiedades de venta: {len(sell)}")

    # Dividir propiedades con tipo de servicio "Ambos"
    logger.info("🔀 Procesando propiedades con tipo 'Ambos'...")
    sell_and_lease = df_full[df_full["tipo_servicio"] == "Ambos"]
    logger.debug(f"Propiedades 'Ambos': {len(sell_and_lease)}")

    if not sell_and_lease.empty:
        # Crear DataFrames para "Venta" y "Arriendo"
        lease_ = sell_and_lease.copy()
        lease_.loc[:, "tipo_servicio"] = "Arriendo"
        lease_.loc[:, "precio"] = lease_["precio"]
        lease_.loc[:, "id"] = MARGIN_FOR_DUPLICATE_CONTROL + lease_["id"]
        logger.debug(f"Propiedades 'Ambos' convertidas a arriendo: {len(lease_)}")

        sell_ = sell_and_lease.copy()
        sell_.loc[:, "tipo_servicio"] = "Venta"
        sell_.loc[:, "precio"] = sell_["precio_venta"]
        logger.debug(f"Propiedades 'Ambos' convertidas a venta: {len(sell_)}")
    else:
        lease_ = pd.DataFrame()
        sell_ = pd.DataFrame()
        logger.debug("No hay propiedades con tipo 'Ambos'")

    logger.info("🔗 Concatenando todos los tipos de servicio...")
    df_full = pd.concat([lease, sell, lease_, sell_])
    logger.debug(f"Total después de separar tipos de servicio: {len(df_full)}")

    # Filtrar por coordenadas válidas
    logger.info("🗺️ Filtrando propiedades con coordenadas válidas...")
    before_filter = len(df_full)
    df_full = df_full[df_full["latitud"].notnull()]
    df_full = df_full[df_full["longitud"].notnull()]
    after_filter = len(df_full)
    removed = before_filter - after_filter
    if removed > 0:
        logger.warning(f"⚠️ Propiedades sin coordenadas eliminadas: {removed}")
    logger.debug(f"Propiedades con coordenadas válidas: {after_filter}")

    # Limpiar columnas innecesarias
    if "index" in df_full.columns:
        df_full.drop("index", axis=1, inplace=True)
        logger.debug("Columna 'index' eliminada")

    # Resumen final
    logger.success("✅ Proceso completado exitosamente")
    logger.info("📊 Resumen final:")
    logger.info(f"   • Total de propiedades: {len(df_full)}")
    logger.info(f"   • Arriendo: {len(df_full[df_full['tipo_servicio'] == 'Arriendo'])}")
    logger.info(f"   • Venta: {len(df_full[df_full['tipo_servicio'] == 'Venta'])}")
    logger.info(f"   • Columnas: {len(df_full.columns)}")

    return df_full


# ======================================================================================


async def get_all_softin() -> pd.DataFrame:
    result_villacruz, result_castillo, result_estrella = await asyncio.gather(
        get_data_softin_villacruz(),
        get_data_softin_castillo(),
        get_data_softin_estrella(),
    )

    df_processed_villacruz = processing_data_for_villacruz(result_villacruz=result_villacruz)

    df_processed_castillo = processing_data_for_castillo(result_castillo=result_castillo)

    df_processed_estrella = processing_data_for_estrella(result_estrella=result_estrella)

    result = concatenate_softin_data_sources([df_processed_villacruz, df_processed_castillo, df_processed_estrella])
    result.drop(columns=["iva_canon"], inplace=True)
    return result


if __name__ == "__main__":
    result = asyncio.run(get_all_softin())
    print(result)
    print(result.shape)
