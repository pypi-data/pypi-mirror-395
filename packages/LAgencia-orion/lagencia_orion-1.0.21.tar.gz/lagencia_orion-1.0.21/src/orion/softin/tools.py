import os
from typing import Dict, List, Literal

import aiohttp
from dotenv import load_dotenv

load_dotenv()


endponit_api = {"villacruz": os.getenv("ENDPOINT_API_SOFTIN_VILLACRUZ"), "castillo": os.getenv("ENDPOINT_API_SOFTIN_CASTILLO"), "estrella": os.getenv("ENDPOINT_API_SOFTIN_ALQUIVENTAS")}

acces_token = {"villacruz": os.getenv("ACCESS_TOKEN_SOFTIN_VILLACRUZ"), "castillo": os.getenv("ACCESS_TOKEN_SOFTIN_CASTILLO"), "estrella": os.getenv("ACCESS_TOKEN_SOFTIN_ALQUIVENTAS")}


class RealState:
    def __init__(self, name: Literal["villacruz", "castillo", "alquiventas", "livin"]):
        self.name = name
        self.token = acces_token.get(name)
        self.endpoint = endponit_api.get(name)
        if self.token is None:
            raise ValueError(f"No access token found for {name}")


async def fetch_api_softin(real_state: RealState, code: int) -> List[Dict]:
    headers = {"Authorization": f"Bearer {real_state.token}", "Content-Type": "application/json"}
    payload = {"codigo": code}
    async with aiohttp.ClientSession() as session:
        async with session.post(real_state.endpoint, json=payload, headers=headers) as response:
            data = await response.json()
            return data
