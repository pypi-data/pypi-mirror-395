from scorb_api.models.endpoint import Endpoint
import asyncio


class TaskRequest(Endpoint):
    def __init__(self, header_auth, token: str, result: str = None) -> None:
        super().__init__(header_auth)
        self.result = result
        self.token = token
        self.base_url = f"/api/request/{self.token}"

    def status(self) -> dict:
        return asyncio.run(
            self.http_request.request(
                endpoint=self.base_url,
                method="get",
                headers=self.header_auth
            )
        )
