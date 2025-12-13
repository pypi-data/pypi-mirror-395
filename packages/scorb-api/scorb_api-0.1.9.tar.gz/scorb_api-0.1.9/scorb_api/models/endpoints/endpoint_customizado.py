from scorb_api.models.endpoint import Endpoint
from typing import Union
import asyncio

from scorb_api.models.endpoints.task_request import TaskRequest


class EndpointCustomizado(Endpoint):
	def __init__(self, header_auth, cenario_code, custom) -> None:
		super().__init__(header_auth=header_auth)
		self.base_url = f"/api/SCORC/crud/cenario/{cenario_code}/{custom}"

	def read(self):
		return asyncio.run(
			self.http_request.request(
				f"{self.base_url}/read", "post",
				headers=self.header_auth
			)
		)

	def upsert(self, body: Union[dict, list[dict]]) -> TaskRequest:
		"""Method to create or update record in custom entity.

		To use this method, you need the following permissions:
		- Required permission: "Entidade Customizada - Lista"
		- Action: Upsert
		- Action required: Edit

		Args:
			body (Union[dict, list[dict]], mandatory): Body object to send on request
		
		Examples:
			```python
			from scorb_api import ScorbApiClient


			client = ScorbApiClient(company="Company Name", app_name="app_name")
			result = (
				client.entidades_customizadas()
				.entidade_customizada(cenario_code="code", custom="custom entity name")
				.upsert(body={"field_1": "value", "field_2": "value"})
			)
			```
		"""
		result = asyncio.run(
			self.http_request.request(
				f"{self.base_url}/upsert", "post",
				headers=self.header_auth,
				json=body
			)
		)

		return TaskRequest(
			header_auth=self.header_auth,
			token=result.get("token"),
			result=result.get("result")
		)
	
	def update(self, body: Union[dict, list[dict]]) -> TaskRequest:
		"""Method to update existing record in custom entity.

		To use this method, you need the following permissions:
		- Required permission: "Entidade Customizada - Lista"
		- Action: Update
		- Action required: Edit

		Args:
			body (Union[dict, list[dict]], mandatory): Body object to send on request
		
		Examples:
			```python
			from scorb_api import ScorbApiClient


			client = ScorbApiClient(company="Company Name", app_name="app_name")
			result = (
				client.entidades_customizadas()
				.entidade_customizada(cenario_code="code", custom="custom entity name")
				.update(body={"field_1": "value", "field_2": "value"})
			)
			```
		"""
		result = asyncio.run(
			self.http_request.request(
				f"{self.base_url}/update", "post",
				headers=self.header_auth,
				json=body
			)
		)

		return TaskRequest(
			header_auth=self.header_auth,
			token=result.get("token"),
			result=result.get("result")
		)
