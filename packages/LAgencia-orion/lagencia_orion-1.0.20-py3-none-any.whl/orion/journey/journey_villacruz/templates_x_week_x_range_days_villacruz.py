from typing import List

from orion.databases.db_empatia.repositories.querys_searcher import QuerysSubscriptions, Subscriptions


class Category:
    LESS_THAN_45 = "-45"  # max week 6= 42 days
    BETWEEN_45_AND_90 = "45-90"  # max week 12 = 84 days
    MORE_THAN_90 = "+90"  # max week 13=91 days


class TemplatesForLessThan45Days:
    week_1: List[str] = ["nuevos_ingresos", "modifica_precio"]
    week_2: List[str] = ["nuevos_ingresos", "modifica_precio"]
    week_3: List[str] = ["nuevos_ingresos", "modifica_precio"]
    week_4: List[str] = []
    week_5: List[str] = []
    week_6: List[str] = []
    week_7: List[str] = []

    @classmethod
    def get(cls, week: int) -> List[str]:
        return getattr(cls, f"week_{week}")


class TemplatesForRange45AND90Days:
    week_1: List[str] = ["45a90_dias_semana1", "aviso_novedades"]
    week_2: List[str] = ["aviso_novedades"]
    week_3: List[str] = ["aviso_novedades", "servicio_diferencial"]
    week_4: List[str] = ["aviso_novedades"]
    week_5: List[str] = ["art_est_arrend", "aviso_novedades"]
    week_6: List[str] = ["aviso_novedades"]
    week_7: List[str] = ["nuevos_ingresos", "modifica_precio", "invitacion_seccion_nosotros"]
    week_8: List[str] = ["nuevos_ingresos", "modifica_precio"]
    week_9: List[str] = ["nuevos_ingresos", "modifica_precio", "import_contrato"]
    week_10: List[str] = []
    week_11: List[str] = []
    week_12: List[str] = []

    @classmethod
    def get(cls, week: int) -> List[str]:
        return getattr(cls, f"week_{week}")


class TemplatesForMoreThan90Days:
    week_1: List[str] = ["45a90_dias_semana1", "aviso_novedades"]
    week_2: List[str] = ["aviso_novedades"]
    week_3: List[str] = ["aviso_novedades", "esto_dicen_de_nosotros"]
    week_4: List[str] = ["aviso_novedades"]
    week_5: List[str] = ["art_est_arrend", "aviso_novedades"]
    week_6: List[str] = ["aviso_novedades"]
    week_7: List[str] = ["aviso_novedades", "servicio_diferencial"]
    week_8: List[str] = ["aviso_novedades"]
    week_9: List[str] = ["import_contrato"]
    week_10: List[str] = []
    week_11: List[str] = ["nuevos_ingresos", "modifica_precio", "invitacion_seccion_nosotros"]
    week_12: List[str] = ["nuevos_ingresos", "modifica_precio"]
    week_13: List[str] = ["nuevos_ingresos", "modifica_precio"]
    week_14: List[str] = []
    week_15: List[str] = []
    week_16: List[str] = []
    week_17: List[str] = []
    week_18: List[str] = []
    week_19: List[str] = []
    week_20: List[str] = []

    @classmethod
    def get(cls, week: int) -> List[str]:
        return getattr(cls, f"week_{week}")


if __name__ == "__main__":
    tools = QuerysSubscriptions()
    records = tools.select_by_filter(Subscriptions.send_noti == 0)
    print(records)

    ...
