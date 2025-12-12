import asyncio
from datetime import datetime
from orion.subscriber_matching.shipments_api import shipment_match_livin, shipment_match_villacruz  # noqa: F401
from orion.subscriber_matching.shipments_by_whabonnet import shipment_match_alquiventas, shipment_match_castillo  # noqa: F401



def main(**kwargs):

    try:
        if asyncio.get_event_loop_policy().__class__.__name__ != "SelectorEventLoop":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except:
        pass



    try:
        shipment_match_livin()
        print("Subscripcion enviada para livin")
    except:
        print("Fallo el envio de la suscripcion de livin")

    try:
        shipment_match_villacruz()
        print("Subscripcion enviada para villacruz")
    except:
        print("Fallo el envio de la suscripcion de villacruz")

    try:
        result = asyncio.run(shipment_match_castillo())
        print("*** result: ", result)
        print("Subscripcion enviada castillo")
    except:
        print("Fallo el envio de la suscripcion de castillo")


    try:
        result = asyncio.run(shipment_match_alquiventas())
        print("*** result: ", result)
        print("Subscripcion enviada para alquiventas")
    except:
        print("Fallo el envio de la suscripcion de alquiventas")

if __name__ == "__main__":
    main()