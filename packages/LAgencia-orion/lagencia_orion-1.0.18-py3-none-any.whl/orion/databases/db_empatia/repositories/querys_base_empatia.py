from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete, update

from orion.databases.config_db_empatia import get_session_empatia

# Tipo genérico para los modelos
T = TypeVar("T")


class BaseCRUD(Generic[T]):
    model: Type[T]  # El modelo genérico sobre el que opera la clase

    @classmethod
    def dict_to_obj(cls, items: Union[Dict, List[Dict]]) -> Union[T, List[T]]:
        """Convierte diccionarios en instancias de modelo."""
        if isinstance(items, list):
            return [cls.model(**item) for item in items]
        return cls.model(**items)

    @classmethod
    def insert(cls, item: Union[Dict, T]) -> bool:
        """Inserta un único registro."""
        if isinstance(item, dict):
            item = cls.dict_to_obj(item)

        with get_session_empatia() as session:
            try:
                session.add(item)
                session.commit()
                return True
            except SQLAlchemyError as ex:
                session.rollback()
                print(f"Error al insertar: {ex}")
                return False

    @classmethod
    def insert_all(cls, items: List[Union[Dict, T]]) -> bool:
        """Inserta múltiples registros (menos de 50)."""

        if len(items) == 0:
            print("No hay registros que insertar")
            return False

        if isinstance(items[0], dict):
            items = cls.dict_to_obj(items)

        with get_session_empatia() as session:
            try:
                session.add_all(items)
                session.commit()
                print(f"Registros insertados: {len(items)}")
                return True
            except SQLAlchemyError as ex:
                session.rollback()
                print(f"Error al insertar múltiples registros: {ex}")
                return False

    @classmethod
    def bulk_insert(cls, items: List[Union[Dict, T]]) -> bool:
        """Inserta grandes volúmenes de datos."""
        if len(items) == 0:
            print("No hay registros que insertar")
            return True
        count_records = len(items)
        if isinstance(items[0], dict):
            items = cls.dict_to_obj(items)

        # if count_records < 50:
        #     print(
        #         f"La cantidad de registros es de {count_records}, se recomienda "
        #         "usar el metodo insert_all"
        #     )
        #     return False

        # Rango de 50 a 1,000 registros
        if 0 <= count_records < 1000:
            return cls._bulk_save_objects(items)

        # Rango de 1,000 a 10,000 registros, en lotes de 500
        elif 1000 <= count_records < 10000000:  # +3 ceros
            return cls._bulk_save_in_batches(items, batch_size=500)

        # Más de 10,000 registros
        else:
            print("Para más de 10,000 registros, se recomienda usar técnicas avanzadas como COPY en PostgreSQL o LOAD DATA en MySQL.")
            return False

    @staticmethod
    def _bulk_save_objects(items: List[T]) -> bool:
        """Inserciones masivas de hasta 1,000 registros."""
        with get_session_empatia() as session:
            try:
                session.bulk_save_objects(items)
                session.commit()
                print("Inserción masiva realizada correctamente.")
                return True
            except SQLAlchemyError as ex:
                session.rollback()
                print(f"Error en inserción masiva: {ex}")
                return False

    @staticmethod
    def _bulk_save_in_batches(items: List[T], batch_size: int) -> bool:
        """Inserciones en lotes para grandes volúmenes de datos."""
        print("Inicia inserción masiva con _bulk_save_in_batches.")
        total_items = len(items)
        processed_items = 0

        with get_session_empatia() as session:
            try:
                for i in range(0, total_items, batch_size):
                    batch = items[i : i + batch_size]
                    session.bulk_save_objects(batch)
                    session.flush()
                    processed_items += len(batch)
                    print(f"Inserción de un lote de {len(batch)} registros realizada correctamente. Progreso: {processed_items}/{total_items}")

                session.commit()
                print(f"Proceso completo. Total de registros insertados: {total_items}")
                return True
            except SQLAlchemyError as ex:
                session.rollback()
                print(f"Error al insertar un lote: {ex}")
                return False

    @classmethod
    def select_all(cls) -> List[T]:
        """Selecciona todos los registros del modelo."""
        with get_session_empatia() as session:
            try:
                stmt = select(cls.model)
                return session.scalars(stmt).all()
            except SQLAlchemyError as ex:
                print(f"Error al seleccionar registros: {ex}")
                return []

    @classmethod
    def select_by_filter(cls, filter_condition: Any) -> List[T]:
        """Selecciona registros filtrados por una condición."""
        with get_session_empatia() as session:
            try:
                stmt = select(cls.model).where(filter_condition)
                return session.scalars(stmt).all()
            except SQLAlchemyError as ex:
                print(f"Error al seleccionar con filtro: {ex}")
                return []

    @classmethod
    def update_by_id(cls, item_update: Union[Dict, T], item_id: int) -> bool:
        """Actualiza un registro por ID."""
        if isinstance(item_update, cls.model):
            item_update = {k: v for k, v in vars(item_update).items() if not k.startswith("_")}

        with get_session_empatia() as session:
            try:
                obj = session.get(cls.model, item_id)
                if not obj:
                    print("Registro no encontrado.")
                    return False

                for key, value in item_update.items():
                    setattr(obj, key, value)

                session.commit()
                return True
            except SQLAlchemyError as ex:
                session.rollback()
                print(f"Error al actualizar: {ex}")
                return False

    @classmethod
    def update_all_by_ids(cls, ids: List[int], update_data: Dict) -> bool:
        """
        Actualiza registros masivamente según una lista de IDs.

        Args:
            cls: Modelo de SQLAlchemy.
            ids (List[int]): Lista de IDs para filtrar.
            update_data (Dict): Diccionario con los campos y valores a actualizar.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        with get_session_empatia() as session:
            try:
                # Construir la sentencia de actualización
                update_stmt = (
                    update(cls.model)
                    .where(cls.model.id.in_(ids))  # Condición WHERE id IN (values)
                    .values(**update_data)  # Valores a actualizar
                )
                result = session.execute(update_stmt)
                session.commit()
                print(f"Se actualizaron {result.rowcount} registros.")
                return True
            except SQLAlchemyError as ex:
                session.rollback()
                print(f"Error al actualizar registros: {ex}")
                return False

    @classmethod
    def update_all_by_filter(cls, filter_condition: Any, update_data: Dict) -> bool:
        """Actualiza registros masivamente según una condición."""
        with get_session_empatia() as session:
            try:
                update_stmt = update(cls.model).where(filter_condition).values(**update_data)
                result = session.execute(update_stmt)
                session.commit()
                print(f"Se actualizaron {result.rowcount} registros.")
                return True
            except SQLAlchemyError as ex:
                session.rollback()
                print(f"Error al actualizar registros: {ex}")
                return False

    @classmethod
    def delete_by_id(cls, item_id: int) -> bool:
        """Elimina un registro por ID."""
        with get_session_empatia() as session:
            try:
                obj = session.get(cls.model, item_id)
                if not obj:
                    print("Registro no encontrado.")
                    return False

                session.delete(obj)
                session.commit()
                return True
            except SQLAlchemyError as ex:
                session.rollback()
                print(f"Error al eliminar: {ex}")
                return False

    @classmethod
    def delete_by_filter(cls, filter_condition: Any) -> bool:
        """Elimina registros según una condición."""
        with get_session_empatia() as session:
            try:
                stmt = delete(cls.model).where(filter_condition)
                result = session.execute(stmt)
                session.commit()
                print(f"Se eliminaron {result.rowcount} registros.")
                return True
            except SQLAlchemyError as ex:
                session.rollback()
                print(f"Error al eliminar con filtro: {ex}")
                return False

    @classmethod
    def delete_all(cls) -> bool:
        """Elimina todos los registros de la tabla."""
        with get_session_empatia() as session:
            try:
                stmt = delete(cls.model)
                result = session.execute(stmt)
                session.commit()
                print(f"Se eliminaron {result.rowcount} registros.")
                return True
            except SQLAlchemyError as ex:
                session.rollback()
                print(f"Error al eliminar todos los registros: {ex}")
                return False

    @classmethod
    def upsert(cls, item: Union[Dict, T]) -> bool:
        """
        Inserta o actualiza un registro. Si ya existe, se actualiza; si no, se inserta.
        Utiliza el método `merge` de SQLAlchemy.
        """
        if isinstance(item, dict):
            item = cls.dict_to_obj(item)

        with get_session_empatia() as session:
            try:
                session.merge(item)
                session.commit()
                return True
            except SQLAlchemyError as ex:
                session.rollback()
                print(f"Error al realizar upsert: {ex}")
                return False

    @classmethod
    def upsert_all(cls, items: List[Union[Dict, T]]) -> bool:
        """
        Inserta o actualiza múltiples registros.
        Si ya existen, se actualizan; si no, se insertan.
        Utiliza el método `merge` de SQLAlchemy.
        """
        if len(items) == 0:
            print("No hay registros que insertar o actualizar")
            return True
        if isinstance(items[0], dict):  # Verifica si los elementos son diccionarios
            items = cls.dict_to_obj(items)

        with get_session_empatia() as session:
            try:
                for item in items:
                    print(f"{item=}")
                    session.merge(item)  # Inserta o actualiza cada elemento
                session.commit()
                print(f"Se actualizaron {len(items)} elementos con upsert.")
                return True
            except SQLAlchemyError as ex:
                session.rollback()
                print(f"Error al realizar upsert_all: {ex}")
                return False
