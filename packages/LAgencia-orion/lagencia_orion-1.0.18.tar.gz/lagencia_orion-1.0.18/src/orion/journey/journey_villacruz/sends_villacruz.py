import time  # noqa: F401

from sqlalchemy.sql.expression import and_

from orion.databases.config_db_empatia import get_session_empatia
from orion.databases.db_empatia.repositories.querys_searcher import NewRevenues, Property, Subscriptions
from orion.journey.journey_villacruz.templates_x_week_x_range_days_villacruz import Category, TemplatesForLessThan45DaysVillacruz, TemplatesForMoreThan90DaysVillacruz, TemplatesForRange45AND90DaysVillacruz  # noqa: F401
from orion.journey.journey_villacruz.shipments_by_template_for_meta import RequestAPIMeta, SendMessageByAPIMeta  # noqa: F401


def case_0(REAL_ESTATE):
    REAL_ESTATE = "livin"

    # with get_session_empatia() as session:
    #     # Realizar la consulta
    #     # result = (
    #     #     session.query(Property.id, Property.code, NewRevenues.price, NewRevenues.old_price, Subscriptions.mobile, Subscriptions.token, Subscriptions.week_noti, Subscriptions.option, Subscriptions.email, NewRevenues.type_template)
    #     #     .join(NewRevenues, NewRevenues.property_id == Property.id)
    #     #     .join(Subscriptions, Subscriptions.id == NewRevenues.subscription_id)
    #     #     .where(and_(Subscriptions.website == REAL_ESTATE, Subscriptions.week_noti.isnot(None)))
    #     #     .all()
    #     # )

    #     result = (
    #         session.query(Property.id, Property.code, NewRevenues.price, NewRevenues.old_price, Subscriptions.mobile, Subscriptions.token, Subscriptions.week_noti, Subscriptions.option, Subscriptions.email, NewRevenues.type_template)
    #         .join(NewRevenues, NewRevenues.property_id == Property.id)
    #         .join(Subscriptions, Subscriptions.id == NewRevenues.subscription_id)
    #         .where(and_(Subscriptions.website == REAL_ESTATE, Subscriptions.send_noti.is_(True)))
    #         .all()
    #     )

    # for record in result:
    #     print(record)

    # telefonos_vistos = set()
    # filtrado = []
    # for fila in result:
    #     telefono = fila[4]  # posición 4
    #     if telefono not in telefonos_vistos:
    #         telefonos_vistos.add(telefono)
    #         filtrado.append(fila)

    # result = filtrado.copy()
    # for row in result:
    #     print(row)

    # records = [RequestAPIMeta(code=record[1], phone=record[4], token=record[5], price=record[2], old_price=record[3], week=record[6], option=record[7], recipients=[record[8]]) for record in result]

    # # debe ir aca la logica para determinar cambio de precio o nuevo ingreso
    # # logica para diferenciar entre gmail y whatsapp

    # for record in records:
    #     print("=======================================")
    #     #templates = []
    #     # ! < 45
    #     if (record.option == Category.LESS_THAN_45) and record.week:
    #         templates = TemplatesForLessThan45Days.get(record.week).copy()
    #         print("ENVIO < 45")
    #         print(templates)
    #         print(record)

    #     # ! > 90
    #     if (record.option == Category.MORE_THAN_90) and record.week:
    #         templates = TemplatesForMoreThan90Days.get(record.week).copy()
    #         print("ENVIO > 90")
    #         print(templates)
    #         print(record)

    #     # ! 45 < 90
    #     if (record.option == Category.BETWEEN_45_AND_90) and record.week:
    #         templates = TemplatesForRange45AND90Days.get(record.week).copy()
    #         print("ENVIO 45 < 90")
    #         print(f"{record.week=}, {record.option=}")
    #         print("original: ", templates)
    #         print(record)

    #         if templates:
    #             print(f"***{templates=}")
    #             print("precios: ",  record.old_price, record.price)
    #             if record.old_price != record.price and "nuevos_ingresos" in templates:
    #                 templates.remove("nuevos_ingresos")
    #             elif (record.old_price == record.price or record.old_price is None) and "modifica_precio" in templates:
    #                 templates.remove("modifica_precio")

    #     # if record.phone == '573103555742':
    #     #     print(f"---{templates=}")
    #     #     service = SendMessageByAPIMeta(templates=templates, record=record)
    #     #     service.send()
    #     #     # time.sleep(2)
    #     #     print()


def case_1(REAL_ESTATE):
    with get_session_empatia() as session:
        # Realizar la consulta
        result = (
            session.query(Property.id, Property.code, NewRevenues.price, NewRevenues.old_price, Subscriptions.mobile, Subscriptions.token, Subscriptions.week_noti, Subscriptions.option, Subscriptions.email, NewRevenues.type_template)
            .join(NewRevenues, NewRevenues.property_id == Property.id)
            .join(Subscriptions, Subscriptions.id == NewRevenues.subscription_id)
            .where(and_(Subscriptions.website == REAL_ESTATE, Subscriptions.week_noti.isnot(None), Subscriptions.send_noti.is_(True)))
            .all()
        )

    telefonos_vistos = set()
    filtrado = []
    for fila in result:
        telefono = fila[4]
        if telefono not in telefonos_vistos:
            telefonos_vistos.add(telefono)
            filtrado.append(fila)

    results = filtrado.copy()

    for result in results:
        record = RequestAPIMeta(code=result[1], phone=result[4], token=result[5], price=result[2], old_price=result[3], week=result[6], option=result[7], recipients=[result[8]])

        print("=======================================")
        # templates = []
        # ! < 45
        if (record.option == Category.LESS_THAN_45) and record.week:
            templates = TemplatesForLessThan45DaysVillacruz.get(record.week).copy()
            print("ENVIO < 45")
            print(templates)
            print(record)

        # ! > 90
        if (record.option == Category.MORE_THAN_90) and record.week:
            templates = TemplatesForMoreThan90DaysVillacruz.get(record.week).copy()
            print("ENVIO > 90")
            print(templates)
            print(record)

        # ! 45 < 90
        if (record.option == Category.BETWEEN_45_AND_90) and record.week:
            print(f"{record.week=}")
            templates = TemplatesForRange45AND90DaysVillacruz.get(record.week).copy()
            print("ENVIO 45 < 90")
            print(templates)
            print(record)


        if templates:
            if "nuevos_ingresos" in templates:
                templates.remove("nuevos_ingresos")
            if "modifica_precio" in templates:
                templates.remove("modifica_precio")
            if "aviso_novedades" in templates:
                templates.remove("aviso_novedades")



        print(f"{templates=}")
        if record.phone == "573103555742":
            print("Enviando por caso 1")
            print(f"---{templates=}")
            service = SendMessageByAPIMeta(templates=templates, record=record)
            service.send()
            # time.sleep(2)
            print()


def case_2(REAL_ESTATE):
    with get_session_empatia() as session:
        # Realizar la consulta
        result = (
            session.query(Property.id, Property.code, NewRevenues.price, NewRevenues.old_price, Subscriptions.mobile, Subscriptions.token, Subscriptions.week_noti, Subscriptions.option, Subscriptions.email, NewRevenues.type_template)
            .join(NewRevenues, NewRevenues.property_id == Property.id)
            .join(Subscriptions, Subscriptions.id == NewRevenues.subscription_id)
            .where(and_(Subscriptions.website == REAL_ESTATE, Subscriptions.week_noti.isnot(None), Subscriptions.send_match.is_(True)))
            .all()
        )

    telefonos_vistos = set()
    filtrado = []
    for fila in result:
        telefono = fila[4]  # posición 4
        if telefono not in telefonos_vistos:
            telefonos_vistos.add(telefono)
            filtrado.append(fila)

    results = filtrado.copy()

    for result in results:
        record = RequestAPIMeta(code=result[1], phone=result[4], token=result[5], price=result[2], old_price=result[3], week=result[6], option=result[7], recipients=[result[8]])

        print("=======================================")
        # templates = []
        # ! < 45
        if (record.option == Category.LESS_THAN_45) and record.week:
            templates = TemplatesForLessThan45DaysVillacruz.get(record.week).copy()
            print("ENVIO < 45")
            print(templates)
            print(record)

        # ! > 90
        if (record.option == Category.MORE_THAN_90) and record.week:
            templates = TemplatesForMoreThan90DaysVillacruz.get(record.week).copy()
            print("ENVIO > 90")
            print(templates)
            print(record)

        # ! 45 < 90
        if (record.option == Category.BETWEEN_45_AND_90) and record.week:
            templates = TemplatesForRange45AND90DaysVillacruz.get(record.week).copy()
            print("ENVIO 45 < 90")
            print(templates)
            print(record)

        templates_= []
        # if result[9] == "aviso_novedades":
        #     templates_.append("aviso_novedades")
        #     if "nuevos_ingresos" in templates:
        #         templates.remove("nuevos_ingresos")
        #     if "modifica_precio" in templates:
        #         templates.remove("modifica_precio")
        #     templates = list(set(templates))

        # elif result[9] == "nuevos_ingresos":
        #     templates_.append("nuevos_ingresos")
        #     if "aviso_novedades" in templates:
        #         templates.remove("aviso_novedades")
        #     if "modifica_precio" in templates:
        #         templates.remove("modifica_precio")
        #     templates = list(set(templates))

        # elif result[9] == "modifica_precio":
        #     templates_.append("modifica_precio")
        #     if "aviso_novedades" in templates:
        #         templates.remove("aviso_novedades")
        #     if "nuevos_ingresos" in templates:
        #         templates.remove("nuevos_ingresos")
        #     templates = list(set(templates))

        if result[9] in templates:
            templates_.append(result[9])



        print(f"{templates_=}")
        if record.phone == "573103555742":
            print(f"---{templates_=}")
            print("Enviando por caso 2")
            service = SendMessageByAPIMeta(templates=templates_, record=record)
            service.send()
            # time.sleep(2)
            print()



if __name__ == "__main__":
    REAL_ESTATE = "villacruz"

    case_1(REAL_ESTATE)
    case_2(REAL_ESTATE)

