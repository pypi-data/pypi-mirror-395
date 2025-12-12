from contextlib import contextmanager
from typing import Generator

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, scoped_session, sessionmaker

from orion import config

DATABASE_URL: str = config.URL_DB_EMPATIA


logger.debug("Configurando engine de base de datos Empatia")
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,  # Número máximo de conexiones activas
    max_overflow=5,  # Conexiones adicionales que se pueden crear temporalmente
    pool_recycle=3600,  # Tiempo en segundos antes de reciclar una conexión
    pool_pre_ping=True,  # 🔥 Revisa la conexión antes de usarla
    future=True,  # ✅ Compatibilidad con SQLAlchemy 2.0
)
logger.info("Engine de base de datos Empatia configurado exitosamente")

SessionLocalEmpatia = scoped_session(
    sessionmaker(
        bind=engine,
        autoflush=False,  # autoflush=False → no sincroniza los objetos con la base en cada query (mejor rendimiento).
        autocommit=False,  # autocommit=False → requiere llamar commit() manualmente
        expire_on_commit=False,  # expire_on_commit=False → evita que los objetos pierdan su estado tras el commit
        future=True,  # ✅ Compatibilidad con SQLAlchemy 2.0
    )
)

BaseEmpatia = declarative_base()


@contextmanager
def get_session_empatia() -> Generator[Session, None, None]:
    """Crea una sesión y la libera automáticamente al salir del contexto."""
    # logger.debug("Iniciando nueva sesión de base de datos")
    session: Session = SessionLocalEmpatia()
    session_id = id(session)
    logger.info(f"Sesión creada con ID: {session_id}")
    try:
        yield session
        session.commit()
        # logger.info(f"Commit exitoso para la sesión {session_id}")
    except Exception as e:  # noqa: F841
        # logger.error(f"Error en la sesión {session_id}: {str(e)}")
        session.rollback()
        # logger.warning(f"Rollback ejecutado para la sesión {session_id}")
        raise
    finally:
        # Con scoped_session, remove() es lo correcto para limpiar el contexto/hilo
        SessionLocalEmpatia.remove()
        # logger.debug(f"Sesión {session_id} liberada")
