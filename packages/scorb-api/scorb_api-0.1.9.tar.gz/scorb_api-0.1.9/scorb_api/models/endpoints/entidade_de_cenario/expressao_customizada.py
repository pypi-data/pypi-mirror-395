from scorb_api.models.endpoint import Endpoint
import asyncio

class ExpressaoCustomizada(Endpoint):
	def __init__(self, header_auth, cenario_code) -> None:
		super().__init__(header_auth=header_auth)
		self.base_url =  f"/api/SCORC/crud/cenario/{cenario_code}/ExpressaoCustomizada"

	def read(self):
		return asyncio.run(self.http_request.request(f"{self.base_url}/read", "post", headers=self.header_auth))