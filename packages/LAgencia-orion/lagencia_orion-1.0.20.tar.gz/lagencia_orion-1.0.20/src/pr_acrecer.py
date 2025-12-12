from orion import config
from orion.acrecer.acrecer import AcrecerClient, get_all_properties_acrecer_by_city_sync
from orion.acrecer.permmited_cities import CIUDADES


async def main():
    CIUDADES

    # service = AcrecerClient(subject=config.SUBJECT_MLS_ACRECER)
    # result_medellin_sin_tilde = await service.get_all_properties_by_cities(["MEDELLiN"])
    # print(result_medellin_sin_tilde)
    # result_medellin_sin_tilde.to_excel("result_medellin_sin_tilde.xlsx", index=False)

    # service = AcrecerClient(subject=config.SUBJECT_MLS_ACRECER)
    # result_medellin_con_tilde = await service.get_all_properties_by_cities(["Medellín"])
    # print(result_medellin_con_tilde)
    # result_medellin_con_tilde.to_excel("result_medellin_con_tilde.xlsx", index=False)

    # service = AcrecerClient(subject=config.SUBJECT_MLS_ACRECER)
    # result_medellin_1 = await service.get_all_properties_by_cities(["medellin"])
    # print(result_medellin_1)
    # result_medellin_1.to_excel("result_medellin_1.xlsx", index=False)

    # service = AcrecerClient(subject=config.SUBJECT_MLS_ACRECER)
    # result_medellin_2 = await service.get_all_properties_by_cities(["medellín"])
    # print(result_medellin_2)
    # result_medellin_2.to_excel("result_medellin_1.xlsx", index=False)

    # service = AcrecerClient(subject=config.SUBJECT_MLS_ACRECER)
    # result_medellin_2 = await service.get_all_properties_by_cities(["MEDELLÍN", "MEDELLIN"])
    # print(result_medellin_2)
    # result_medellin_2.to_excel("result_medellin_1.xlsx", index=False)

    ...

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

    result_medellin_2= get_all_properties_acrecer_by_city_sync()
    print(result_medellin_2)
    result_medellin_2.to_excel("result_medellin_1.xlsx", index=False)
