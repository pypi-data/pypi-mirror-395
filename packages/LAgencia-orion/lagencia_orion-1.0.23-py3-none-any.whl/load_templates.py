from pathlib import Path
from typing import Optional
from orion.databases.db_empatia.models.model_searcher import EmailTemplate
from orion.databases.config_db_empatia import get_session_empatia
from sqlalchemy import select


def create_email_template_from_path(file_path: Path, name: Optional[str] = None) -> EmailTemplate:
    """
    Lee un archivo HTML desde `path` y lo guarda en la tabla email_templates.

    :param path: Ruta al archivo HTML.
    :param name: Nombre lógico de la plantilla.
                 Si es None, se usa el nombre del archivo sin extensión.
    :return: La instancia de EmailTemplate creada.
    """

    if not file_path.exists():
        raise FileNotFoundError(f"El archivo no existe: {file_path}")

    # Leer el contenido HTML
    html_body = file_path.read_text(encoding="utf-8")

    # Si no se pasa name, tomamos el nombre del archivo sin extensión
    if name is None:
        name = file_path.stem  # p.ej., "testimonios_vc.html" -> "testimonios_vc"

    template = EmailTemplate(name=name, html_body=html_body)

    with get_session_empatia() as session:
        session.add(template)
        session.flush()  # para que se genere el id antes de salir, si lo necesitas

        # Aquí template.id ya está disponible
        return template



# template_name = "servicio_diferencial.html"
# path_template = Path("src/orion") / "journey" / "journey_villacruz" / "templates_gmail" / template_name
# create_email_template_from_path(path_template, "servicio_diferencial")

# template_name = "esto_dicen_de_nosotros.html"
# path_template = Path("src/orion") / "journey" / "journey_villacruz" / "templates_gmail" / template_name
# create_email_template_from_path(path_template, template_name)


# template_name = "invitacion_seccion_nosotros.html"
# path_template = Path("src/orion") / "journey" / "journey_villacruz" / "templates_gmail" / template_name
# create_email_template_from_path(path_template, template_name)



def select_email_template_table(name: Optional[str] = None) -> EmailTemplate:
    """
    Lee un archivo HTML desde `path` y lo guarda en la tabla email_templates.

    :param path: Ruta al archivo HTML.
    :param name: Nombre lógico de la plantilla.
                 Si es None, se usa el nombre del archivo sin extensión.
    :return: La instancia de EmailTemplate creada.
    """


    with get_session_empatia() as session:
        stmt= select(EmailTemplate).where(EmailTemplate.name == name)
        result = session.scalars(stmt).first()
        return result

# template_name = "invitacion_seccion_nosotros.html"
# print(select_email_template_table(template_name).html_body)