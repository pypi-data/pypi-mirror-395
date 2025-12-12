import httpx
from orion import config
from orion.acrecer.acrecer import AcrecerAuthService, AcrecerClient
from orion.acrecer.permmited_cities import CIUDADES



BASE_URL = "https://mls.mbp.com.co/mobilia-mls/ws/Properties"


# auth_service = AcrecerAuthService(subject=config.SUBJECT_MLS_ACRECER)
# token = auth_service.get_jwt_token()
# print(token)


service = AcrecerClient(subject=config.SUBJECT_MLS_ACRECER)
print(service.get_all_properties_by_cities(CIUDADES))

# city= "Medellín"
# page= "1"
# records_per_page= 20

# jwt_token = jwt_token
# headers = {"Authorization": f"Bearer {jwt_token}", "Accept": "application/json"}
# params = {
#             "operation": "publicPropertiesSearchByCityZone",
#             "cityName": city,
#             "page": str(page),
#             "recordsPerPage": str(records_per_page),
#         }

