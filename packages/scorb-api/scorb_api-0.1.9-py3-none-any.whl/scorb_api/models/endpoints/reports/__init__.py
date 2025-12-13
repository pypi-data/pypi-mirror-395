from scorb_api.models.endpoint import Endpoint
import asyncio
from time import sleep

class Report(Endpoint):
    def __init__(self, header_auth, report_name) -> None:
        super().__init__(header_auth=header_auth)
        self.base_url = f"/api/SCORC/crud/{report_name}"

    def read(self, output_format="2"):
        response = self.__request_report_generation(output_format=output_format)
        report_status_url = response["jobStatusUrl"]
        report_result_url = response["jobResultUrl"]
        is_report_completed = False
        while not is_report_completed:
            report_status = asyncio.run(self.http_request.request(
                report_status_url, "get", headers=self.header_auth,
            ))
            sleep(10)
            is_report_completed = report_status["Completed"]
        report_data = asyncio.run(self.http_request.request(
            report_result_url, "get", headers=self.header_auth,
        ))
        return report_data["Items"]
        

    def __request_report_generation(self, output_format="2"):
        return asyncio.run(
            self.http_request.request(
                f"{self.base_url}/read-async", "post", headers=self.header_auth,
                json={"outputFormat": output_format}
                
            )
        )
