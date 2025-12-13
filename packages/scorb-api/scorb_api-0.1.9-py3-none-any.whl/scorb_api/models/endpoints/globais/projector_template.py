from scorb_api.models.endpoint import Endpoint
import asyncio

class ProjectorTemplate(Endpoint):
    def __init__(self, header_auth) -> None:
        super().__init__(header_auth=header_auth)
        self.base_url = "/api/SCORC/crud/ProjectorTemplate"
         

    def read(self):
        return asyncio.run(self.http_request.request(f"{self.base_url}/read", "post", headers=self.header_auth))  

