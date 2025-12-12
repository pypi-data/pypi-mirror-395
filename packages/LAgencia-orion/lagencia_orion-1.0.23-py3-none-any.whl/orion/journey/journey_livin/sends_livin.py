import time
from typing import List  # noqa: F401

from sqlalchemy import select
from sqlalchemy.sql.expression import and_

from loguru import logger
from orion.databases.config_db_empatia import get_session_empatia
from orion.databases.db_empatia.repositories.querys_searcher import NewRevenues, Property, Subscriptions
from orion.journey.journey_livin.models import RequestToSendNotifications, AddData
from orion.journey.journey_livin.service import SendMessageByAPIMeta
from orion.journey.journey_livin.templates_x_week_x_range_days import Category, TemplatesForLessThan45Days, TemplatesForMoreThan90Days, TemplatesForRange45AND90Days



def case_1(REAL_ESTATE):
    with get_session_empatia() as session:
        # Realizar la consulta
        result = (
            session.query(Property.id, Property.code, NewRevenues.price, NewRevenues.old_price, Subscriptions.mobile, Subscriptions.token, Subscriptions.week_noti, Subscriptions.option, Subscriptions.email, NewRevenues.type_template)
            .join(NewRevenues, NewRevenues.property_id == Property.id)
            .join(Subscriptions, Subscriptions.id == NewRevenues.subscription_id)
            .where(and_(Subscriptions.website == REAL_ESTATE, Subscriptions.week_noti.isnot(None), Subscriptions.send_noti.is_(True),  NewRevenues.notified.is_(False)))
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
        record = RequestToSendNotifications(code=result[1], phone=result[4], token=result[5], price=result[2], old_price=result[3], week=result[6], option=result[7], recipients=[result[8]])

        print("=======================================")
        # templates = []
        # ! < 45
        if (record.option == Category.LESS_THAN_45) and record.week:
            templates = TemplatesForLessThan45Days.get(record.week).copy()
            print("ENVIO < 45")
            print(templates)
            print(record)

        # ! > 90
        if (record.option == Category.MORE_THAN_90) and record.week:
            templates = TemplatesForMoreThan90Days.get(record.week).copy()
            print("ENVIO > 90")
            print(templates)
            print(record)

        # ! 45 < 90
        if (record.option == Category.BETWEEN_45_AND_90) and record.week:
            print(f"{record.week=}")
            templates = TemplatesForRange45AND90Days.get(record.week).copy()
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





def case_2(REAL_ESTATE, produccion: bool):
    with get_session_empatia() as session:
        # Realizar la consulta
        result = (
            session.query(Subscriptions.id, Property.code, NewRevenues.price, NewRevenues.old_price, Subscriptions.mobile, Subscriptions.token, Subscriptions.week_noti, Subscriptions.option, Subscriptions.email, NewRevenues.type_template, Subscriptions.name, Subscriptions.adviser_name, Subscriptions.adviser_mobile)
            .join(NewRevenues, NewRevenues.property_id == Property.id)
            .join(Subscriptions, Subscriptions.id == NewRevenues.subscription_id)
            .where(and_(Subscriptions.website == REAL_ESTATE, Subscriptions.week_noti.isnot(None), Subscriptions.send_match.is_(True),  NewRevenues.notified.is_(False)))
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
    logger.info(f"Cantidad de clientes para notificar: {len(results)}")

    results_shipment =[]
    for result in results:
        add_data = AddData(customer_name=result[10], customer_phone=result[4], adviser_name=result[11], adviser_phone=result[12])
        record = RequestToSendNotifications(code=result[1], phone=result[4], token=result[5], price=result[2], old_price=result[3], week=result[6], option=result[7], recipients=[result[8]], add_data=add_data)

        print("=======================================")
        # ! < 45
        if (record.option == Category.LESS_THAN_45) and record.week:
            templates = TemplatesForLessThan45Days.get(record.week).copy()
            print("ENVIO < 45")
            print(templates)
            print(record)

        # ! > 90
        if (record.option == Category.MORE_THAN_90) and record.week:
            templates = TemplatesForMoreThan90Days.get(record.week).copy()
            print("ENVIO > 90")
            print(templates)
            print(record)

        # ! 45 < 90
        if (record.option == Category.BETWEEN_45_AND_90) and record.week:
            templates = TemplatesForRange45AND90Days.get(record.week).copy()
            print("ENVIO 45 < 90")
            print(templates)
            print(record)

        templates_= []
        if result[9] in templates:
            templates_.append(result[9])

        if not produccion:
            print(f"{templates_=}")
            if record.phone == "573165241659":
                print(f"---{templates_=}")
                print("Enviando por caso 2")
                service = SendMessageByAPIMeta(templates=templates_, record=record)
                service.send()
                # time.sleep(2)
                print()

                print("++++++++++++++++++++++++++ Haciendo envios")
                print(f"{record=}")
                print(f"{templates_=}")
                record.phone = "573103555742"
                record.add_data.customer_phone = "573103555742"
                record.add_data.adviser_phone = "573103555742"

                service = SendMessageByAPIMeta(templates=templates_, record=record)
                result_shipment = service.send()
                results_shipment.append({"subscriptions_id": result[0], "result": result_shipment})
                print("***result_shipment: ", result_shipment)


        else:

            service = SendMessageByAPIMeta(templates=templates_, record=record)
            result_shipment= service.send()
            results_shipment.append({"subscriptions_id": result[0], "result": result_shipment})


    # Actualizar estado notified en base de datos
    with get_session_empatia() as session:
        for record in results_shipment:
            id_ = record.get("subscriptions_id")
            print(f"{id_=}")
            stmt = select(NewRevenues).where(NewRevenues.subscription_id == id_)
            records: List[NewRevenues] = session.scalars(stmt).all()

            for record_ in records:
                record_.notified = True

            session.commit()

            print(records)
            print(f"{results_shipment=}")
            print(f"{len(records)=}")








if __name__ == "__main__":
    REAL_ESTATE = "livin"

    case_1(REAL_ESTATE)
    case_2(REAL_ESTATE)

