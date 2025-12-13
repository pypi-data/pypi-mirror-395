import aiohttp
from decouple import config
from urllib.parse import urljoin
from typing import Any, Literal


class HTTPRequest:
    """Class to handle requests to an API"""
    async def request(
        self,
        endpoint: str,
        method: Literal["get", "post", "put", "patch", "delete"],
        headers: dict = None,
        parameters: dict = None,
        data: Any = None,
        json: Any = None,
    ) -> dict:
        request_url = urljoin(base=config("SCORB_BASE_URL"), url=endpoint)
        headers = {**headers} if headers else {}
        response = None

        async with aiohttp.ClientSession() as session:
            if method == "get":
                response = await session.get(
                    url=request_url,
                    headers=headers,
                    params=parameters,
                )

            elif method == "post":
                response = await session.post(
                    url=request_url,
                    headers=headers,
                    params=parameters,
                    data=data,
                    json=json,
                )

            elif method == "put":
                response = await session.put(
                    url=request_url,
                    headers=headers,
                    params=parameters,
                    data=data,
                    json=json,
                )

            elif method == "patch":
                response = await session.patch(
                    url=request_url,
                    headers=headers,
                    params=parameters,
                    data=data,
                    json=json,
                )

            elif method == "delete":
                response = await session.delete(
                    url=request_url,
                    headers=headers,
                    params=parameters,
                    data=data,
                    json=json,
                )
            else:
                raise ValueError("Invalid HTTP method")

            # Check response
            if response.status == 500:
                response_json = await response.json()
                if response_json:
                    raise Exception(f"Internal Server Error: {response_json}")

            response.raise_for_status()
            response_json = await response.json()

            return response_json
