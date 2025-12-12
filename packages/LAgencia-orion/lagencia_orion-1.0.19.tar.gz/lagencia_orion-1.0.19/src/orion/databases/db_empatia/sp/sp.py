from typing import Literal

from sqlalchemy import text

from orion.databases.config_db_empatia import get_session_empatia
from loguru import logger

# ==================================Funciones para crear los porcedimientos almacenados
def create_sp(tablename: Literal["municipios", "veredas", "corregimientos", "comunas", "barrios"]):
    # PASO 1: Eliminar procedimiento si existe
    drop_sql = "DROP PROCEDURE IF EXISTS sp_update_{tablename}_shows_in_sectors_table".format(tablename=tablename)

    # PASO 2: Crear procedimiento
    create_procedure_sql = """CREATE PROCEDURE sp_update_{tablename}_shows_in_sectors_table()
    BEGIN
        START TRANSACTION;

        UPDATE sectors s
        JOIN (
            SELECT
                s.id AS sector_id,
                MAX(p.show_villacruz) AS show_villacruz,
                MAX(p.show_rent_villacruz) AS show_rent_villacruz,
                MAX(p.show_sale_villacruz) AS show_sale_villacruz,
                MAX(p.show_furnished_villacruz) AS show_furnished_villacruz,
                MAX(p.show_castillo) AS show_castillo,
                MAX(p.show_rent_castillo) AS show_rent_castillo,
                MAX(p.show_sale_castillo) AS show_sale_castillo,
                MAX(p.show_furnished_castillo) AS show_furnished_castillo,
                MAX(p.show_estrella) AS show_estrella,
                MAX(p.show_rent_estrella) AS show_rent_estrella,
                MAX(p.show_sale_estrella) AS show_sale_estrella,
                MAX(p.show_furnished_estrella) AS show_furnished_estrella,
                MAX(p.show_livin) AS show_livin,
                MAX(p.show_rent_livin) AS show_rent_livin,
                MAX(p.show_sale_livin) AS show_sale_livin,
                MAX(p.show_furnished_livin) AS show_furnished_livin
            FROM properties p
            JOIN {tablename} s ON ST_Contains(s.geometry, p.geometry)
            WHERE s.active = 1
            GROUP BY s.id
            LIMIT 1000
        ) AS subquery ON s.id = subquery.sector_id
        SET
            s.show_villacruz = subquery.show_villacruz,
            s.show_rent_villacruz = subquery.show_rent_villacruz,
            s.show_sale_villacruz = subquery.show_sale_villacruz,
            s.show_furnished_villacruz = subquery.show_furnished_villacruz,
            s.show_castillo = subquery.show_castillo,
            s.show_rent_castillo = subquery.show_rent_castillo,
            s.show_sale_castillo = subquery.show_sale_castillo,
            s.show_furnished_castillo = subquery.show_furnished_castillo,
            s.show_estrella = subquery.show_estrella,
            s.show_rent_estrella = subquery.show_rent_estrella,
            s.show_sale_estrella = subquery.show_sale_estrella,
            s.show_furnished_estrella = subquery.show_furnished_estrella,
            s.show_livin = subquery.show_livin,
            s.show_rent_livin = subquery.show_rent_livin,
            s.show_sale_livin = subquery.show_sale_livin,
            s.show_furnished_livin = subquery.show_furnished_livin;

        COMMIT;
    END""".format(tablename=tablename)

    # Ejecutar por separado
    with get_session_empatia() as session:
        try:
            # Eliminar procedimiento
            session.execute(text(drop_sql))
            session.commit()

            # Crear procedimiento
            session.execute(text(create_procedure_sql))
            session.commit()

            logger.info("Procedimiento almacenado creado exitosamente")

        except Exception as e:
            session.rollback()
            logger.info(f"Error creando procedimiento: {e}")
            raise


def create_sp_update_municipios_shows_in_sectors_table():
    create_sp(tablename="municipios")


def create_sp_update_corregimientos_shows_in_sectors_table():
    create_sp(tablename="corregimientos")


def create_sp_update_veredas_shows_in_sectors_table():
    create_sp(tablename="veredas")


def create_sp_update_comunas_shows_in_sectors_table():
    create_sp(tablename="comunas")


def create_sp_update_barrios_shows_in_sectors_table():
    create_sp(tablename="barrios")


def create_sp_update_lugares_shows_in_sectors_table():
    drop_sql = "DROP PROCEDURE IF EXISTS sp_update_lugares_shows_in_sectors_table"

    sql = """CREATE PROCEDURE sp_update_lugares_shows_in_sectors_table()
BEGIN
    DECLARE affected_rows INT DEFAULT 0;
    DECLARE start_time DATETIME;

    -- Registrar inicio
    SET start_time = NOW();

    -- Realizar el UPDATE
    UPDATE sectors s
    JOIN (
        SELECT
            s.id AS sect_id,
            MAX(p.show_villacruz) AS show_villacruz,
            MAX(p.show_rent_villacruz) AS show_rent_villacruz,
            MAX(p.show_sale_villacruz) AS show_sale_villacruz,
            MAX(p.show_furnished_villacruz) AS show_furnished_villacruz,
            MAX(p.show_castillo) AS show_castillo,
            MAX(p.show_rent_castillo) AS show_rent_castillo,
            MAX(p.show_sale_castillo) AS show_sale_castillo,
            MAX(p.show_furnished_castillo) AS show_furnished_castillo,
            MAX(p.show_estrella) AS show_estrella,
            MAX(p.show_rent_estrella) AS show_rent_estrella,
            MAX(p.show_sale_estrella) AS show_sale_estrella,
            MAX(p.show_furnished_estrella) AS show_furnished_estrella,
            MAX(p.show_livin) AS show_livin,
            MAX(p.show_rent_livin) AS show_rent_livin,
            MAX(p.show_sale_livin) AS show_sale_livin,
            MAX(p.show_furnished_livin) AS show_furnished_livin
        FROM sectors AS s
        LEFT JOIN properties AS p
          ON p.geometry IS NOT NULL
          AND ST_Distance_Sphere(
                ST_PointOnSurface(p.geometry),
                ST_PointOnSurface(s.geometry)
              ) <= 500
        WHERE s.type = 'Lugar'
          AND s.geometry IS NOT NULL
        GROUP BY s.id
    ) AS agg ON s.id = agg.sect_id
    SET
        s.show_villacruz = COALESCE(agg.show_villacruz, 0),
        s.show_rent_villacruz = COALESCE(agg.show_rent_villacruz, 0),
        s.show_sale_villacruz = COALESCE(agg.show_sale_villacruz, 0),
        s.show_furnished_villacruz = COALESCE(agg.show_furnished_villacruz, 0),
        s.show_castillo = COALESCE(agg.show_castillo, 0),
        s.show_rent_castillo = COALESCE(agg.show_rent_castillo, 0),
        s.show_sale_castillo = COALESCE(agg.show_sale_castillo, 0),
        s.show_furnished_castillo = COALESCE(agg.show_furnished_castillo, 0),
        s.show_estrella = COALESCE(agg.show_estrella, 0),
        s.show_rent_estrella = COALESCE(agg.show_rent_estrella, 0),
        s.show_sale_estrella = COALESCE(agg.show_sale_estrella, 0),
        s.show_furnished_estrella = COALESCE(agg.show_furnished_estrella, 0),
        s.show_livin = COALESCE(agg.show_livin, 0),
        s.show_rent_livin = COALESCE(agg.show_rent_livin, 0),
        s.show_sale_livin = COALESCE(agg.show_sale_livin, 0),
        s.show_furnished_livin = COALESCE(agg.show_furnished_livin, 0);

    -- Obtener filas afectadas
    SET affected_rows = ROW_COUNT();

    -- Mostrar resultado
    SELECT
        affected_rows AS sectors_updated,
        start_time AS started_at,
        NOW() AS finished_at,
        TIMESTAMPDIFF(SECOND, start_time, NOW()) AS duration_seconds;

END"""

    with get_session_empatia() as session:
        try:
            # Eliminar procedimiento si existe
            session.execute(text(drop_sql))
            session.commit()

            # Crear procedimiento nuevo
            session.execute(text(sql))
            session.commit()

            logger.info("Procedimiento almacenado creado exitosamente")

        except Exception as e:
            session.rollback()
            logger.info(f"Error creando procedimiento: {e}")
            raise

# ==================================Funciones para ejecutar los porcedimientos almacenados
def execute_sp(sp_name: str):
    with get_session_empatia() as session:
        try:
            session.execute(text(f"CALL {sp_name}()"))
            session.commit()
            logger.info(f"✓ Procedimiento {sp_name} ejecutado exitosamente")
        except Exception as e:
            session.rollback()
            logger.info(f"✗ Error ejecutando {sp_name}: {e}")
            raise

def execute_sp_update_municipios_shows_in_sectors_table():
    execute_sp(sp_name="sp_update_municipios_shows_in_sectors_table")


def execute_sp_update_corregimientos_shows_in_sectors_table():
    execute_sp(sp_name="sp_update_corregimientos_shows_in_sectors_table")


def execute_sp_update_veredas_shows_in_sectors_table():
    execute_sp(sp_name="sp_update_veredas_shows_in_sectors_table")


def execute_sp_update_comunas_shows_in_sectors_table():
    execute_sp(sp_name="sp_update_comunas_shows_in_sectors_table")


def execute_sp_update_barrios_shows_in_sectors_table():
    execute_sp(sp_name="sp_update_barrios_shows_in_sectors_table")


def execute_sp_update_lugares_shows_in_sectors_table():
    execute_sp(sp_name="sp_update_lugares_shows_in_sectors_table")


# ========================== Funcion para crear los trigers
def create_trigger(tablename: Literal["municipios", "veredas", "corregimientos", "comunas", "barrios", "lugares"]) -> bool:
    """
    Crea un triger sobre una tabla fuente que actualiza los campos <name> y <geometry> de la tabla properties

    Args:
        tablename (str): Nombre de la tabla sobre la que se desea aplicar el trigger.

    Returns:
        bool: True si el trigger se creo exitosamente, False en caso contrario.
    """

    # PASO 1: Eliminar el trigger si existe
    drop_sql = "DROP TRIGGER IF EXISTS after_{tablename}_update;".format(tablename=tablename)

    # Crear el trigger
    create_trigger_sql = """
        CREATE TRIGGER after_{tablename}_update
        AFTER UPDATE ON {tablename}
        FOR EACH ROW
        BEGIN
            IF NEW.active = 0 THEN
                DELETE FROM sectors WHERE id = NEW.id;

            ELSE
                UPDATE sectors
                SET name = NEW.name,
                    geometry = NEW.geometry
                WHERE id = NEW.id;
            END IF;
        END
        """.format(tablename=tablename)

    # Ejecutar por separado
    with get_session_empatia() as session:
        try:
            # Eliminar trigger
            session.execute(text(drop_sql))
            session.commit()

            # Crear trigger
            session.execute(text(create_trigger_sql))
            session.commit()

            logger.info("trigger creado exitosamente")
            return True

        except Exception as e:
            session.rollback()
            logger.info(f"Error creando trigger: {e}")
            return False


# ==================================IMPLEMENTAACIONES GENERALES
def create_sp_and_trigers_from_sectors_control():
    tables = ["municipios", "veredas", "corregimientos", "comunas", "barrios", "lugares"]

    for table in tables:
        create_trigger(tablename=table)

    create_sp_update_municipios_shows_in_sectors_table()
    create_sp_update_corregimientos_shows_in_sectors_table()
    create_sp_update_veredas_shows_in_sectors_table()
    create_sp_update_comunas_shows_in_sectors_table()
    create_sp_update_barrios_shows_in_sectors_table()
    create_sp_update_lugares_shows_in_sectors_table()

def execute_all_sp():
    execute_sp_update_municipios_shows_in_sectors_table()
    execute_sp_update_corregimientos_shows_in_sectors_table()
    execute_sp_update_veredas_shows_in_sectors_table()
    execute_sp_update_comunas_shows_in_sectors_table()
    execute_sp_update_barrios_shows_in_sectors_table()
    execute_sp_update_lugares_shows_in_sectors_table()
