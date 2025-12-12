def main():
    from orion.journey.journey_castillo.sends_castillo import case_1, case_2 # noqa: F401
    produccion= False

    REAL_ESTATE = "castillo"
    #case_1(REAL_ESTATE=REAL_ESTATE)
    case_2(REAL_ESTATE=REAL_ESTATE)

    # # from orion.journey.journey_estrella.sends_estrella import case_1, case_2# noqa: F401
    # # REAL_ESTATE = "estrella"
    # # case_1(REAL_ESTATE=REAL_ESTATE)
    # # case_2(REAL_ESTATE=REAL_ESTATE)

    # from orion.journey.journey_livin.sends_livin import case_1, case_2  # noqa: F401
    # REAL_ESTATE = "livin"
    # #case_1(REAL_ESTATE=REAL_ESTATE)
    # case_2(REAL_ESTATE=REAL_ESTATE)

    # from orion.journey.journey_villacruz.sends_villacruz import case_1, case_2  # noqa: F401
    # REAL_ESTATE = "villacruz"
    # #case_1(REAL_ESTATE=REAL_ESTATE)
    # case_2(REAL_ESTATE=REAL_ESTATE)


if __name__ == "__main__":
    main()
