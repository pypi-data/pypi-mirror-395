"""This module handles authorization into Tutto API."""
from decouple import config
from scorb_api.helpers.http import HTTPRequest
import asyncio

class Authorization:
    def __init__(self, company: str, app_name: str) -> None:
        self.__http_client = HTTPRequest()
        self.company = company
        self.app_name = app_name
        self.token = None

    def __get_authentication_body(self) -> dict:
        return {
            "grant_type": "password",
            "username": config("SCORB_USERNAME_API"),
            "password": config("SCORB_PASSWORD_API"),
        }
    
    def __request_token(self) -> dict:
        self.token = asyncio.run(
            self.__http_client.request(
                method="post",
                endpoint="token",
                data=self.__get_authentication_body(),
                parameters={"empresa": self.company, "app": self.app_name},
            )
        ).get("access_token")
    
    def generate_authorization_header(self) -> dict:
        self.__request_token()
        if not self.token:
            raise Exception("The token was not requested yet")
        return {"Authorization": f"Bearer {self.token}"}
