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



    #shipment_match_livin()

    shipment_match_villacruz()


    #result = asyncio.run(shipment_match_castillo())
    # print("*** result: ", result)

    #result = asyncio.run(shipment_match_alquiventas())
    # #print("*** result: ", result)


if __name__ == "__main__":
    main()