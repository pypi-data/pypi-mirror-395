import asyncio
import os
import random
import re
import unicodedata
from typing import Any, Dict, List, Optional

import httpx
import pandas as pd
from loguru import logger
from orion.definition_ids import ID_BASE_SIMI_LIVIN

"""_summary_: Consumo del API simi para livin
"""


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
    """Clase base para empresas."""

    username: str
    password: str


class Livin(Company):
    """Configuración para Livin/Simi."""

    username: str = os.getenv("USERNAME_SIMI")
    password: str = os.getenv("PASSWORD_SIMI")


class Simi:
    """Servicio para interactuar con la API de Simi."""

    BASE_URL = "http://simi-api.com/ApiSimiweb/response"

    def __init__(self, company: Company, max_concurrent_requests: int = 5, timeout: int = 60):
        """
        Inicializa el servicio de Simi.

        Args:
            company: Instancia de Company con credenciales
            max_concurrent_requests: Máximo de peticiones concurrentes
            timeout: Timeout en segundos para las peticiones
        """
        self.company = company
        self.auth = httpx.BasicAuth(username=company.username, password=company.password)
        self.timeout = httpx.Timeout(connect=10.0, read=timeout, write=10.0, pool=10.0)
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)

        logger.info(f"Servicio Simi inicializado con max {max_concurrent_requests} peticiones concurrentes")

    async def _fetch_with_retry(self, client: httpx.AsyncClient, url: str, max_retries: int = 3, base_delay: int = 1) -> Optional[Dict[str, Any]]:
        """
        Realiza una petición HTTP con reintentos y backoff exponencial.

        Args:
            client: Cliente httpx
            url: URL a consultar
            max_retries: Número máximo de reintentos
            base_delay: Delay base en segundos

        Returns:
            Respuesta JSON o None si falla
        """
        for attempt in range(max_retries):
            try:
                async with self.semaphore:
                    response = await client.get(url)

                    if response.status_code == 200:
                        # Verificar que la respuesta no esté vacía
                        if not response.content:
                            logger.warning(f"Respuesta vacía en URL {url}")
                            return None

                        try:
                            return response.json()
                        except Exception as e:
                            logger.error(f"Error decodificando JSON de {url}: {e}")
                            return None
                    else:
                        logger.warning(f"Código de estado no exitoso: {response.status_code} para URL {url}")

                # Backoff exponencial con jitter
                if attempt < max_retries - 1:
                    delay = base_delay * (2**attempt) + random.uniform(0, 0.1)
                    logger.debug(f"Reintentando {url} en {delay:.2f}s (Intento {attempt + 1}/{max_retries})")
                    await asyncio.sleep(delay)

            except (httpx.TimeoutException, httpx.ConnectError) as e:
                logger.warning(f"Error de conexión en {url}: {e}")

                if attempt < max_retries - 1:
                    delay = base_delay * (2**attempt) + random.uniform(0, 0.1)
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Todos los reintentos fallaron para {url}")

            except Exception as e:
                logger.exception(f"Error inesperado en {url}: {e}")
                return None

        return None

    async def get_properties(self, client: httpx.AsyncClient, page: int, per_page: int) -> Dict[str, Any]:
        """
        Obtiene propiedades de una página específica.

        Args:
            client: Cliente httpx
            page: Número de página
            per_page: Propiedades por página

        Returns:
            Diccionario con las propiedades
        """
        url = f"{self.BASE_URL}/v2.1.1/filtroInmueble/limite/{page}/total/{per_page}"
        result = await self._fetch_with_retry(client, url)
        return result if result else {}

    async def get_property_details(self, client: httpx.AsyncClient, property_code: str) -> Dict[str, Any]:
        """
        Obtiene los detalles de una propiedad específica.

        Args:
            client: Cliente httpx
            property_code: Código de la propiedad

        Returns:
            Diccionario con los detalles de la propiedad
        """
        url = f"{self.BASE_URL}/v2/inmueble/codInmueble/{property_code}"
        result = await self._fetch_with_retry(client, url)
        return result if result else {}

    async def fetch_all_properties(self) -> pd.DataFrame:
        """
        Obtiene todas las propiedades con sus detalles.

        Returns:
            DataFrame con todas las propiedades y sus detalles
        """
        logger.info("🚀 Iniciando extracción de propiedades de Simi")

        async with httpx.AsyncClient(auth=self.auth, timeout=self.timeout) as client:
            # Paso 1: Obtener el total de inmuebles
            logger.info("📊 Obteniendo total de inmuebles...")
            first_page = await self.get_properties(client, page=1, per_page=1)

            total_properties = first_page.get("datosGrales", {}).get("totalInmuebles", 0)
            logger.info(f"Total de inmuebles encontrados: {total_properties}")

            if total_properties == 0:
                logger.warning("⚠️ No se encontraron propiedades")
                return pd.DataFrame()

            # Paso 2: Calcular páginas necesarias
            per_page = 20
            total_pages = (total_properties + per_page - 1) // per_page
            logger.info(f"📄 Total de páginas a procesar: {total_pages}")

            # Paso 3: Obtener todas las propiedades
            logger.info("📥 Obteniendo todas las propiedades...")
            tasks = [self.get_properties(client, page=page, per_page=per_page) for page in range(1, total_pages + 1)]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Extraer propiedades de los resultados
            all_properties = []
            for i, result in enumerate(results, start=1):
                if isinstance(result, Exception):
                    logger.error(f"Error en página {i}: {result}")
                    continue

                properties = result.get("Inmuebles", [])
                all_properties.extend(properties)
                logger.debug(f"Página {i}: {len(properties)} propiedades")

            logger.success(f"✅ Total de propiedades obtenidas: {len(all_properties)}")

            # Paso 4: Obtener detalles de cada propiedad
            logger.info("🔍 Obteniendo detalles de las propiedades...")
            property_codes = [prop.get("Codigo_Inmueble") for prop in all_properties if prop.get("Codigo_Inmueble")]

            logger.info(f"📋 Códigos de propiedades a procesar: {len(property_codes)}")

            # Procesar en lotes para mejor control
            batch_size = 10
            all_details = []

            for i in range(0, len(property_codes), batch_size):
                batch_codes = property_codes[i : i + batch_size]
                batch_num = (i // batch_size) + 1
                total_batches = (len(property_codes) + batch_size - 1) // batch_size

                logger.info(f"📦 Procesando lote {batch_num}/{total_batches} ({len(batch_codes)} propiedades)")

                tasks = [self.get_property_details(client, code) for code in batch_codes]

                batch_results = await asyncio.gather(*tasks, return_exceptions=True)

                # Filtrar resultados válidos
                valid_details = [result for result in batch_results if not isinstance(result, Exception) and result]

                all_details.extend(valid_details)
                logger.debug(f"Lote {batch_num}: {len(valid_details)} detalles obtenidos")

                # Pequeña pausa entre lotes
                if i + batch_size < len(property_codes):
                    await asyncio.sleep(0.5)

            logger.success(f"✅ Detalles recuperados: {len(all_details)}")

            # Paso 5: Combinar propiedades con detalles
            logger.info("🔗 Combinando propiedades con detalles...")
            combined_data = self._merge_properties_and_details(all_properties[: len(all_details)], all_details)

            # Paso 6: Crear DataFrame
            logger.info("📊 Creando DataFrame...")
            df = pd.DataFrame(combined_data)

            logger.success(f"🎉 Proceso completado: {len(df)} propiedades con detalles")
            logger.info(f"📋 Columnas: {len(df.columns)}")

            return df

    def _merge_properties_and_details(self, properties: List[Dict], details: List[Dict]) -> List[Dict[str, Any]]:
        """
        Combina las propiedades con sus detalles.

        Args:
            properties: Lista de propiedades básicas
            details: Lista de detalles de propiedades

        Returns:
            Lista de diccionarios combinados
        """
        combined = []

        for property_data, detail_data in zip(properties, details):
            # Convertir keys a minúsculas para consistencia
            property_lower = {k.lower(): v for k, v in property_data.items()}

            detail_lower = {k.lower(): v for k, v in detail_data.items()}

            # Combinar diccionarios
            merged = property_lower.copy()
            merged.update(detail_lower)

            combined.append(merged)

        logger.debug(f"Combinadas {len(combined)} propiedades con sus detalles")

        return combined


async def get_all_simi() -> pd.DataFrame:
    """
    Obtiene y procesa todas las propiedades de Simi/Livin.

    Returns:
        DataFrame con todas las propiedades procesadas
    """
    logger.info("🚀 Iniciando proceso de extracción de Simi/Livin")

    # Inicializar servicio
    logger.debug("Inicializando servicio Simi...")
    livin = Livin()
    simi_service = Simi(company=livin, max_concurrent_requests=5, timeout=60)

    # Obtener propiedades
    logger.info("📥 Obteniendo propiedades de Simi...")
    simi_full = await simi_service.fetch_all_properties()

    if simi_full.empty:
        logger.warning("⚠️ No se obtuvieron propiedades de Simi")
        return pd.DataFrame()

    logger.success(f"✅ Propiedades obtenidas: {len(simi_full)}")

    # Agregar columnas básicas
    logger.info("🔄 Procesando columnas básicas...")
    simi_full["activo"] = True
    simi_full["show_livin"] = True
    simi_full["source"] = "simi_livin"
    logger.debug("Columnas básicas agregadas")

    # Procesar IDs
    logger.info("🔢 Procesando IDs...")
    simi_full["codinm"] = simi_full["codinm"].astype(int)
    simi_full["id"] = ID_BASE_SIMI_LIVIN + simi_full["codinm"]
    logger.debug(f"IDs generados: rango {simi_full['id'].min()} - {simi_full['id'].max()}")

    # Calcular precio
    logger.info("💰 Calculando precios...")
    try:
        simi_full["precio"] = simi_full["valorventa"].astype(float) + simi_full["valorcanon"].astype(float)
        logger.debug(f"Precio promedio: ${simi_full['precio'].mean():,.0f}")
    except Exception as e:
        logger.error(f"Error calculando precios: {e}")
        simi_full["precio"] = 0

    # Convertir campos booleanos
    logger.info("✓ Convirtiendo campos booleanos...")
    boolean_fields = ["amobladoinmueble", "destacado", "amoblado", "admonincluida", "esnuevo"]

    for field in boolean_fields:
        try:
            simi_full[field] = simi_full[field].astype(bool)
            logger.debug(f"Campo '{field}' convertido a booleano")
        except Exception as e:
            logger.warning(f"Error convirtiendo '{field}' a booleano: {e}")
            simi_full[field] = False

    # Procesar estado
    logger.info("📊 Procesando estado de disponibilidad...")
    initial_available = (simi_full["descestado"] == "DISPONIBLE").sum()
    simi_full["descestado"] = simi_full["descestado"].apply(lambda x: True if x == "DISPONIBLE" else False)
    logger.debug(f"Propiedades disponibles: {initial_available} de {len(simi_full)}")

    # Convertir campos a string
    logger.info("📝 Convirtiendo campos a string...")
    string_fields = ["portales", "caracteristicasinternas", "caracteristicasexternas", "caracteristicasalrededores", "asesor", "captador", "othercaracteristicas", "inmobiliaria", "fotos", "fotos360"]

    for field in string_fields:
        try:
            simi_full[field] = simi_full[field].astype(str)
            logger.debug(f"Campo '{field}' convertido a string")
        except Exception as e:
            logger.warning(f"Error convirtiendo '{field}' a string: {e}")
            simi_full[field] = ""

    # Limpiar campos numéricos con comas
    logger.info("🧹 Limpiando campos numéricos...")
    try:
        simi_full["canon"] = simi_full["canon"].astype(str).str.replace(",", "")
        simi_full["valorcanon"] = simi_full["valorcanon"].astype(str).str.replace(",", "")
        logger.debug("Campos numéricos limpiados (comas removidas)")
    except Exception as e:
        logger.error(f"Error limpiando campos numéricos: {e}")

    # Procesar fecha de modificación
    logger.info("📅 Procesando fechas de modificación...")
    try:

        simi_full["fecha_modificacion"] = simi_full[["fecha_modificacion", "fecha_modificacion2"]].max(axis=1)
        simi_full.drop(columns=["fecha_modificacion2"], inplace=True)
        simi_full= simi_full[simi_full["fecha_modificacion"]!= '0000-00-00 00:00:00']
        logger.debug("Fecha de modificación consolidada")
    except Exception as e:
        logger.warning(f"Error procesando fechas: {e}")

    # Formatear nombres de columnas
    logger.info("🔤 Formateando nombres de columnas...")
    original_columns = len(simi_full.columns)
    simi_full.columns = list(map(format_column_name, simi_full.columns))
    logger.debug(f"Columnas formateadas: {original_columns} columnas")

    # Filtrar por coordenadas válidas
    logger.info("🗺️ Filtrando propiedades con coordenadas válidas...")
    before_filter = len(simi_full)
    simi_full = simi_full[simi_full["latitud"].notnull()]
    simi_full = simi_full[simi_full["longitud"].notnull()]
    after_filter = len(simi_full)
    removed = before_filter - after_filter

    if removed > 0:
        logger.warning(f"⚠️ Propiedades sin coordenadas eliminadas: {removed} ({removed / before_filter * 100:.1f}%)")
    else:
        logger.debug("Todas las propiedades tienen coordenadas válidas")

    logger.debug(f"Propiedades con coordenadas válidas: {after_filter}")

    # Eliminar campos innecesarios
    logger.info("🗑️ Eliminando columnas innecesarias...")
    columns_to_drop = []

    if "codinterno" in simi_full.columns:
        columns_to_drop.append("codinterno")

    if columns_to_drop:
        simi_full.drop(columns=columns_to_drop, inplace=True)
        logger.debug(f"Columnas eliminadas: {', '.join(columns_to_drop)}")
    else:
        logger.debug("No hay columnas adicionales para eliminar")

    # Resumen final
    logger.success("✅ Proceso de Simi completado exitosamente")
    logger.info("📊 Resumen final:")
    logger.info(f"   • Total de propiedades: {len(simi_full)}")
    logger.info(f"   • Columnas finales: {len(simi_full.columns)}")

    if len(simi_full) > 0:
        available_count = simi_full["descestado"].sum()
        logger.info(f"   • Propiedades disponibles: {available_count}")
        logger.info(f"   • Propiedades amobladas: {simi_full['amoblado'].sum()}")
        logger.info(f"   • Propiedades destacadas: {simi_full['destacado'].sum()}")

    return simi_full


# Ejemplo de uso
if __name__ == "__main__":
    import asyncio

    try:
        df = asyncio.run(get_all_simi())
        logger.info(f"🎉 Datos de Simi cargados: {df.shape}")
        print("\nPrimeras filas:")
        print(df.head())
    except Exception as e:
        logger.exception(f"❌ Error fatal en el proceso de Simi: {e}")
        raise


if __name__ == "__main__":
    # Ejecutar
    result = asyncio.run(get_all_simi())


# =============================================================================


# username = os.getenv("USERNAME_SIMI")
# password = os.getenv("PASSWORD_SIMI")
# auth = aiohttp.BasicAuth(username, password)


# async def fetch_with_retry(session: aiohttp.ClientSession, url: str, max_retries: int = 3, base_delay: int = 1):
#     for attempt in range(max_retries):
#         try:
#             async with session.get(url) as response:
#                 # Verificar el código de estado
#                 if response.status == 200:
#                     text = await response.text()
#                     if text.strip():
#                         try:
#                             return await response.json(content_type=None)
#                         except json.JSONDecodeError:
#                             print(f"Error de decodificación JSON en URL {url}")
#                     else:
#                         print(f"Respuesta vacía en URL {url}")
#                 else:
#                     print(f"Código de estado no exitoso: {response.status}")

#                 # Esperar antes de reintentar con backoff exponencial
#                 delay = base_delay * (2**attempt) + random.uniform(0, 0.1)
#                 print(f"Reintentando en {delay:.2f} segundos (Intento {attempt + 1})")
#                 await asyncio.sleep(delay)

#         except (aiohttp.ClientError, asyncio.TimeoutError) as e:
#             print(f"Error de conexión: {e}")
#             delay = base_delay * (2**attempt) + random.uniform(0, 0.1)
#             await asyncio.sleep(delay)

#     return None


# async def get_properties(session: aiohttp.ClientSession, url: str) -> List[Dict]:
#     result = await fetch_with_retry(session, url)
#     return result if result else []


# async def get_details_property(session: aiohttp.ClientSession, cod: str) -> List[Dict]:
#     url = f"http://simi-api.com/ApiSimiweb/response/v2/inmueble/codInmueble/{cod}"
#     result = await fetch_with_retry(session, url)
#     return result if result else []


# async def get_properties_simi() -> pd.DataFrame:
#     async with aiohttp.ClientSession(auth=auth, timeout=aiohttp.ClientTimeout(total=60)) as session:
#         url = "http://simi-api.com/ApiSimiweb/response/v2.1.1/filtroInmueble/limite/{}/total/{}"

#         # Obtener el total de inmuebles
#         task = [get_properties(session, url.format(1, 1))]
#         result = await asyncio.gather(*task)

#         totalInmuebles = result[0].get("datosGrales", {}).get("totalInmuebles", 0)
#         print("totalInmuebles: ", totalInmuebles)

#         total = 20  # Inmuebles por página
#         mod = totalInmuebles % total
#         limite = totalInmuebles // total if mod == 0 else (totalInmuebles // total) + 1  # Número de páginas

#         # Crear URLs
#         urls = [url.format(pag, total) for pag in range(1, limite + 1)]

#         # Crear las tareas para consumir múltiples URLs
#         task = [get_properties(session, url) for url in urls]
#         result = await asyncio.gather(*task)

#         # Obtener todas las propiedades de las respuestas
#         properties = [propertie for result_record in result if result_record.get("Inmuebles") for propertie in result_record.get("Inmuebles")]

#         # Obtener detalles de las propiedades con control de concurrencia
#         codes = [propertie.get("Codigo_Inmueble") for propertie in properties]

#         details = []
#         semaphore = asyncio.Semaphore(5)  # Limitar a 5 solicitudes concurrentes

#         async def fetch_detail_with_semaphore(cod):
#             async with semaphore:
#                 return await get_details_property(session, cod)

#         # Procesar en lotes
#         for i in range(0, len(codes), 10):
#             batch_codes = codes[i : i + 10]
#             batch_tasks = [fetch_detail_with_semaphore(cod) for cod in batch_codes]
#             batch_results = await asyncio.gather(*batch_tasks)
#             details.extend([detail for detail in batch_results if detail])

#             # Pequeña pausa entre lotes
#             await asyncio.sleep(1)

#         print(f"Detalles recuperados: {len(details)}")

#         # Combinar propiedades con detalles
#         simi_full = []
#         for propertie, detail in zip(properties[: len(details)], details):
#             # Convertir las keys de propertie a minúsculas
#             propertie_lower = {k.lower(): v for k, v in propertie.items()}

#             # Convertir las keys de detail a minúsculas
#             detail_lower = {k.lower(): v for k, v in detail.items()}

#             # Combinar diccionarios con keys en minúsculas
#             merged = propertie_lower.copy()
#             merged.update(detail_lower)

#             simi_full.append(merged)

#         simi_full_df = pd.DataFrame(simi_full)

#         return simi_full_df


# def get_all_simi():

#     start_time = time.time()
#     simi_full = asyncio.run(get_properties_simi())
#     print(f"Tiempo total de ejecución: {time.time() - start_time:.2f} segundos")

#     simi_full["activo"] = True
#     simi_full["show_livin"] = True
#     simi_full["codinm"] = simi_full["codinm"].astype(int)
#     simi_full["id"] = 4000000 + simi_full["codinm"]
#     simi_full["precio"] = simi_full["valorventa"].astype(float) + simi_full["valorcanon"].astype(float)

#     simi_full["amobladoinmueble"] = simi_full["amobladoinmueble"].astype(bool)
#     simi_full["destacado"] = simi_full["destacado"].astype(bool)
#     simi_full["amoblado"] = simi_full["amoblado"].astype(bool)
#     simi_full["admonincluida"] = simi_full["admonincluida"].astype(bool)
#     simi_full["esnuevo"] = simi_full["esnuevo"].astype(bool)
#     simi_full["descestado"] = simi_full["descestado"].apply(lambda x: True if x == "DISPONIBLE" else False)

#     simi_full["portales"] = simi_full["portales"].astype(str)
#     simi_full["caracteristicasinternas"] = simi_full["caracteristicasinternas"].astype(str)
#     simi_full["caracteristicasexternas"] = simi_full["caracteristicasexternas"].astype(str)
#     simi_full["caracteristicasalrededores"] = simi_full["caracteristicasalrededores"].astype(str)
#     simi_full["asesor"] = simi_full["asesor"].astype(str)
#     simi_full["captador"] = simi_full["captador"].astype(str)
#     simi_full["othercaracteristicas"] = simi_full["othercaracteristicas"].astype(str)
#     simi_full["inmobiliaria"] = simi_full["inmobiliaria"].astype(str)
#     simi_full["fotos"] = simi_full["fotos"].astype(str)
#     simi_full["fotos360"] = simi_full["fotos360"].astype(str)
#     simi_full["canon"] = simi_full["canon"].replace(",", "")
#     simi_full["valorcanon"] = simi_full["valorcanon"].replace(",", "")
#     simi_full["source"] = "simi_livin"

#     simi_full["fecha_modificacion"] = simi_full[["fecha_modificacion", "fecha_modificacion2"]].max(axis=1)
#     simi_full.drop(columns=["fecha_modificacion2"], inplace=True)

#     simi_full.columns = list(map(format_column_name, simi_full.columns))
#     simi_full = simi_full[simi_full["latitud"].notnull()]
#     simi_full = simi_full[simi_full["longitud"].notnull()]

#     # campos añadidos por simi que no requerimos
#     simi_full.drop(columns=["codinterno"], inplace=True)
#     return simi_full


# if __name__ == "__main__":
#     start_time = time.time()
#     asyncio.run(get_properties_simi())
#     print(f"Tiempo total de ejecución: {time.time() - start_time:.2f} segundos")


# async def get_all_simi() -> pd.DataFrame:
#     livin = Livin()
#     simi_service = Simi(company=livin, max_concurrent_requests=5, timeout=60)
#     simi_full = await simi_service.fetch_all_properties()

#     simi_full["activo"] = True
#     simi_full["show_livin"] = True
#     simi_full["codinm"] = simi_full["codinm"].astype(int)
#     simi_full["id"] = 4000000 + simi_full["codinm"]
#     simi_full["precio"] = simi_full["valorventa"].astype(float) + simi_full["valorcanon"].astype(float)

#     simi_full["amobladoinmueble"] = simi_full["amobladoinmueble"].astype(bool)
#     simi_full["destacado"] = simi_full["destacado"].astype(bool)
#     simi_full["amoblado"] = simi_full["amoblado"].astype(bool)
#     simi_full["admonincluida"] = simi_full["admonincluida"].astype(bool)
#     simi_full["esnuevo"] = simi_full["esnuevo"].astype(bool)
#     simi_full["descestado"] = simi_full["descestado"].apply(lambda x: True if x == "DISPONIBLE" else False)

#     simi_full["portales"] = simi_full["portales"].astype(str)
#     simi_full["caracteristicasinternas"] = simi_full["caracteristicasinternas"].astype(str)
#     simi_full["caracteristicasexternas"] = simi_full["caracteristicasexternas"].astype(str)
#     simi_full["caracteristicasalrededores"] = simi_full["caracteristicasalrededores"].astype(str)
#     simi_full["asesor"] = simi_full["asesor"].astype(str)
#     simi_full["captador"] = simi_full["captador"].astype(str)
#     simi_full["othercaracteristicas"] = simi_full["othercaracteristicas"].astype(str)
#     simi_full["inmobiliaria"] = simi_full["inmobiliaria"].astype(str)
#     simi_full["fotos"] = simi_full["fotos"].astype(str)
#     simi_full["fotos360"] = simi_full["fotos360"].astype(str)
#     simi_full["canon"] = simi_full["canon"].replace(",", "")
#     simi_full["valorcanon"] = simi_full["valorcanon"].replace(",", "")
#     simi_full["source"] = "simi_livin"

#     simi_full["fecha_modificacion"] = simi_full[["fecha_modificacion", "fecha_modificacion2"]].max(axis=1)
#     simi_full.drop(columns=["fecha_modificacion2"], inplace=True)

#     simi_full.columns = list(map(format_column_name, simi_full.columns))
#     simi_full = simi_full[simi_full["latitud"].notnull()]
#     simi_full = simi_full[simi_full["longitud"].notnull()]

#     # campos añadidos por simi que no requerimos
#     simi_full.drop(columns=["codinterno"], inplace=True)
#     return simi_full
